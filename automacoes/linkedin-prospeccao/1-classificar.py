#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PASSO 1 - Classifica as conexoes do LinkedIn em faixas de prioridade.

Como usar:
    python3 1-classificar.py entrada/Connections.csv

Gera dentro de saida/:
    1-prioridade-A.csv      donos de negocio -> abordar primeiro
    2-prioridade-B.csv      alta renda / decisores -> abordar depois
    3-baixa-prioridade.csv  sem fit agora -> nutrir com conteudo
    0-excluidos.csv         mercado financeiro, colegas e sem potencial
    resumo.md              o panorama em texto, pra voce bater o olho
"""
import csv
import os
import re
import sys
import unicodedata
from collections import Counter
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import regras  # noqa: E402

BASE = os.path.dirname(os.path.abspath(__file__))
SAIDA = os.path.join(BASE, "saida")

# LinkedIn exporta o CSV em ingles ou portugues dependendo do idioma da conta.
COLUNAS = {
    "nome":     ["first name", "nome"],
    "sobrenome": ["last name", "sobrenome"],
    "url":      ["url", "perfil"],
    "email":    ["email address", "endereco de e-mail", "e-mail"],
    "empresa":  ["company", "empresa"],
    "cargo":    ["position", "cargo", "posicao"],
    "conectado": ["connected on", "conectado em", "data da conexao"],
}

# O LinkedIn traz o cargo no genero da pessoa ("Engenheira", "Diretora").
# Os dicionarios ficam so no masculino e a gente converte antes de comparar,
# senao metade das mulheres da base escapa do filtro.
GENERO = {
    "engenheira": "engenheiro", "diretora": "diretor", "socia": "socio",
    "medica": "medico", "advogada": "advogado", "fundadora": "fundador",
    "cofundadora": "cofundador", "proprietaria": "proprietario",
    "empresaria": "empresario", "empreendedora": "empreendedor",
    "dona": "dono", "presidenta": "presidente", "gerenta": "gerente",
    "coordenadora": "coordenadora", "supervisora": "supervisor",
    "consultora": "consultor", "analista": "analista", "gestora": "gestor",
    "administradora": "administrador", "arquiteta": "arquiteta",
    "contadora": "contador", "auditora": "auditor", "juiza": "juiz",
    "promotora": "promotor", "procuradora": "procurador",
    "delegada": "delegado", "veterinaria": "veterinario",
    "psicologa": "psicologo", "nutricionista": "nutricionista",
    "dentista": "dentista", "cirurgia": "cirurgiao", "cirurgia": "cirurgiao",
    "franqueada": "franqueado", "produtora": "produtor",
    "pecuarista": "pecuarista", "comandante": "comandante",
    "desenvolvedora": "desenvolvedor", "programadora": "programador",
    "cientista": "cientista", "especialista": "especialista",
    "assessora": "assessor", "bancaria": "bancario", "operadora": "operador",
    "assistente": "assistente", "tecnica": "tecnico", "vendedora": "vendedor",
    "estagiaria": "estagiario", "aposentada": "aposentado",
    "professora": "professor", "senhora": "senhor",
}

MESES = {
    "jan": 1, "feb": 2, "fev": 2, "mar": 3, "apr": 4, "abr": 4, "may": 5,
    "mai": 5, "jun": 6, "jul": 7, "aug": 8, "ago": 8, "sep": 9, "set": 9,
    "oct": 10, "out": 10, "nov": 11, "dec": 12, "dez": 12,
}


def normalizar(texto):
    """minusculo, sem acento, espacos limpos - pra comparar sem susto."""
    if not texto:
        return ""
    texto = unicodedata.normalize("NFKD", str(texto))
    texto = "".join(c for c in texto if not unicodedata.combining(c))
    texto = texto.lower()
    # separadores que o pessoal usa no titulo: "CEO @ Acme | Founder - Socio"
    for sep in ("|", "/", "@", "•", "·", "—", "–", "»", ">", "+", "&"):
        texto = texto.replace(sep, " ")
    # emoji e simbolos soltos so atrapalham a comparacao
    texto = "".join(c for c in texto if c.isalnum() or c in " .,-")
    texto = re.sub(r"\s+", " ", texto).strip()
    return texto


def masculinizar(texto):
    """'Engenheira de Software Senior' -> 'engenheiro de software senior'."""
    return " ".join(GENERO.get(p, p) for p in texto.split())


def abrir_csv(caminho):
    """Pula o cabecalho de avisos que o LinkedIn coloca no topo do arquivo."""
    with open(caminho, encoding="utf-8-sig", newline="") as fh:
        linhas = fh.read().splitlines()

    inicio = 0
    for i, linha in enumerate(linhas[:15]):
        campos = [normalizar(c) for c in linha.split(",")]
        if any(c in COLUNAS["nome"] for c in campos):
            inicio = i
            break

    leitor = csv.DictReader(linhas[inicio:])
    mapa = {}
    for chave, apelidos in COLUNAS.items():
        for campo in leitor.fieldnames or []:
            if normalizar(campo) in apelidos:
                mapa[chave] = campo
                break

    if "nome" not in mapa:
        raise SystemExit(
            "Nao achei a coluna de nome no CSV.\n"
            "Confere se o arquivo e mesmo o Connections.csv do LinkedIn."
        )

    for linha in leitor:
        yield {k: (linha.get(col) or "").strip() for k, col in mapa.items()}


def achar(termos, texto):
    """Devolve os termos do dicionario/lista que aparecem no texto."""
    if isinstance(termos, dict):
        return [t for t in termos if t in texto]
    return [t for t in termos if t in texto]


def meses_de_conexao(valor):
    """'15 Mar 2024' -> quantos meses faz que voces conectaram."""
    if not valor:
        return None
    partes = normalizar(valor).replace(",", " ").split()
    try:
        if len(partes) >= 3:
            dia, mes_txt, ano = int(partes[0]), partes[1][:3], int(partes[2])
            mes = MESES.get(mes_txt)
            if not mes:
                return None
            data = datetime(ano, mes, dia)
        else:
            data = datetime.strptime(partes[0], "%d/%m/%Y")
    except (ValueError, IndexError):
        return None
    hoje = datetime.now()
    return (hoje.year - data.year) * 12 + (hoje.month - data.month)


def classificar(pessoa):
    """Devolve (faixa, nota, motivos) para uma conexao."""
    cargo = normalizar(pessoa.get("cargo"))
    empresa = normalizar(pessoa.get("empresa"))
    # compara contra as duas formas: como veio e no masculino
    cargo_m = masculinizar(cargo)
    if cargo_m != cargo:
        cargo = f"{cargo} {cargo_m}"
    tudo = f"{cargo} {empresa}".strip()
    motivos = []

    if not tudo:
        return "BAIXA", 0, ["sem cargo e sem empresa no export"]

    # --- exclusoes -------------------------------------------------------
    # colegas da propria casa saem sempre, seja da mesa ou da TI
    batidas = achar(regras.EXCLUIR_EMPRESA_SEMPRE, empresa)
    if batidas:
        return "EXCLUIDO", -100, ["colega de casa: " + batidas[0]]

    # cargo do mercado financeiro = concorrente, nao importa onde trabalhe
    batidas = achar(regras.EXCLUIR_CARGO_FINANCEIRO, cargo)
    if batidas:
        return "EXCLUIDO", -100, ["concorrente (cargo): " + ", ".join(batidas[:3])]

    # empresa financeira so exclui se o cargo tambem for da area.
    # quem faz tecnologia, produto, design ou RH num banco nao concorre
    # com voce - e costuma ser uma lead muito boa.
    batidas = achar(regras.EXCLUIR_EMPRESA_FINANCEIRA, empresa)
    if batidas:
        resgate = achar(regras.CARGOS_RESGATE_NAO_CONCORRENTE, cargo)
        if resgate:
            motivos.append(
                f"trabalha em {batidas[0]} mas na area de {resgate[0].strip()} "
                "- nao e concorrente"
            )
        else:
            return "EXCLUIDO", -100, ["concorrente (empresa): " + batidas[0]]

    batidas = achar(regras.EXCLUIR_SEM_POTENCIAL, tudo)
    if batidas:
        return "EXCLUIDO", -50, ["sem potencial de aporte hoje: " + ", ".join(batidas[:3])]

    # --- pontuacao ------------------------------------------------------
    nota = 0
    eh_dono = False

    achados = achar(regras.CARGOS_DONO, cargo)
    if achados:
        melhor = max(achados, key=lambda t: regras.CARGOS_DONO[t])
        nota += regras.CARGOS_DONO[melhor]
        motivos.append(f"dono/decisor: {melhor}")
        eh_dono = True

    achados = achar(regras.CARGOS_ALTA_RENDA, cargo)
    if achados:
        melhor = max(achados, key=lambda t: regras.CARGOS_ALTA_RENDA[t])
        peso = regras.CARGOS_ALTA_RENDA[melhor]
        nota += peso if not eh_dono else peso // 3
        motivos.append(f"alta renda: {melhor}")

    achados = achar(regras.CARGOS_PENALIDADE, cargo)
    if achados and not eh_dono:
        pior = min(achados, key=lambda t: regras.CARGOS_PENALIDADE[t])
        nota += regras.CARGOS_PENALIDADE[pior]
        motivos.append(f"senioridade baixa: {pior}")

    achados = achar(regras.SETORES_BONUS, empresa)
    if achados:
        melhor = max(achados, key=lambda t: regras.SETORES_BONUS[t])
        nota += regras.SETORES_BONUS[melhor]
        motivos.append(f"setor: {melhor}")

    # conexao antiga e sem conversa = bom gancho pra reabrir
    meses = meses_de_conexao(pessoa.get("conectado"))
    if meses is not None and meses >= 6:
        nota += 5
        motivos.append(f"conectados ha {meses} meses (gancho pra reabrir)")

    if nota >= regras.CORTE_PRIORIDADE_A:
        return "A", nota, motivos
    if nota >= regras.CORTE_PRIORIDADE_B:
        return "B", nota, motivos
    return "BAIXA", nota, motivos


def main():
    if len(sys.argv) < 2:
        raise SystemExit("Uso: python3 1-classificar.py entrada/Connections.csv")

    caminho = sys.argv[1]
    if not os.path.exists(caminho):
        raise SystemExit(f"Arquivo nao encontrado: {caminho}")

    os.makedirs(SAIDA, exist_ok=True)
    baldes = {"A": [], "B": [], "BAIXA": [], "EXCLUIDO": []}
    vistos = set()
    total = 0

    for pessoa in abrir_csv(caminho):
        nome = f"{pessoa.get('nome','')} {pessoa.get('sobrenome','')}".strip()
        if not nome:
            continue
        chave = normalizar(nome) + "|" + normalizar(pessoa.get("empresa"))
        if chave in vistos:
            continue
        vistos.add(chave)
        total += 1

        faixa, nota, motivos = classificar(pessoa)
        meses = meses_de_conexao(pessoa.get("conectado"))
        baldes[faixa].append({
            "nome": nome,
            "cargo": pessoa.get("cargo", ""),
            "empresa": pessoa.get("empresa", ""),
            "url": pessoa.get("url", ""),
            "nota": nota,
            "meses_conexao": "" if meses is None else meses,
            "por_que": "; ".join(motivos),
            "status": "",        # voce preenche: enviado / respondeu / reuniao
            "data_contato": "",
        })

    arquivos = {
        "A": "1-prioridade-A.csv",
        "B": "2-prioridade-B.csv",
        "BAIXA": "3-baixa-prioridade.csv",
        "EXCLUIDO": "0-excluidos.csv",
    }
    campos = ["nome", "cargo", "empresa", "url", "nota", "meses_conexao",
              "por_que", "status", "data_contato"]

    for faixa, arquivo in arquivos.items():
        lista = sorted(baldes[faixa], key=lambda p: -p["nota"])
        destino = os.path.join(SAIDA, arquivo)
        with open(destino, "w", encoding="utf-8-sig", newline="") as fh:
            escritor = csv.DictWriter(fh, fieldnames=campos)
            escritor.writeheader()
            escritor.writerows(lista)

    escrever_resumo(baldes, total)

    print(f"\n  {total} conexoes lidas\n")
    print(f"  PRIORIDADE A (donos de negocio) .... {len(baldes['A']):>5}")
    print(f"  PRIORIDADE B (alta renda) .......... {len(baldes['B']):>5}")
    print(f"  Baixa prioridade ................... {len(baldes['BAIXA']):>5}")
    print(f"  Excluidos (financeiro/sem fit) ..... {len(baldes['EXCLUIDO']):>5}")
    print(f"\n  Tudo salvo em: {SAIDA}")
    print("  Abra saida/resumo.md pra ver o panorama.\n")


def escrever_resumo(baldes, total):
    hoje = datetime.now().strftime("%d/%m/%Y")
    linhas = [
        "# Resumo da base de conexoes",
        f"\nGerado em {hoje} - {total} conexoes unicas lidas.\n",
        "| Faixa | Quem e | Quantos | O que fazer |",
        "|---|---|---|---|",
        f"| **A** | Donos, socios, CEOs, fundadores | {len(baldes['A'])} | Abordagem 1:1 esta semana |",
        f"| **B** | Alta renda, C-level contratado, liberais | {len(baldes['B'])} | Abordagem 1:1 neste mes |",
        f"| Baixa | Sem fit de aporte agora | {len(baldes['BAIXA'])} | So conteudo, sem 1:1 |",
        f"| Fora | Mercado financeiro e colegas | {len(baldes['EXCLUIDO'])} | Nao abordar |",
    ]

    for faixa, titulo in (("A", "Prioridade A"), ("B", "Prioridade B")):
        lista = sorted(baldes[faixa], key=lambda p: -p["nota"])[:20]
        if not lista:
            continue
        linhas.append(f"\n## Top 20 - {titulo}\n")
        linhas.append("| # | Nome | Cargo | Empresa | Nota |")
        linhas.append("|---|---|---|---|---|")
        for i, p in enumerate(lista, 1):
            linhas.append(
                f"| {i} | {p['nome']} | {p['cargo'][:45]} | {p['empresa'][:35]} | {p['nota']} |"
            )

    setores = Counter()
    for p in baldes["A"] + baldes["B"]:
        for parte in p["por_que"].split(";"):
            if "setor:" in parte:
                setores[parte.split("setor:")[1].strip()] += 1
    if setores:
        linhas.append("\n## Setores mais presentes na sua base quente\n")
        linhas.append("Use isso pra decidir sobre o que voce posta.\n")
        for setor, qtd in setores.most_common(12):
            linhas.append(f"- **{setor}** - {qtd} conexoes")

    sem_dados = [p for p in baldes["BAIXA"]
                 if "sem cargo e sem empresa" in p["por_que"]]
    if sem_dados:
        linhas.append("\n## Perfis sem informacao no export\n")
        linhas.append(
            f"**{len(sem_dados)} conexoes** vieram sem cargo e sem empresa - o "
            "LinkedIn nao exporta esses campos quando a pessoa restringe o perfil.\n"
        )
        linhas.append(
            "Elas cairam em baixa prioridade por falta de dado, **nao porque nao "
            "servem**. Pode ter empresario bom escondido ai. Vale bater o olho na "
            "lista de vez em quando: estao em `3-baixa-prioridade.csv` com o "
            "motivo \"sem cargo e sem empresa no export\".\n"
        )

    motivos_fora = Counter()
    for p in baldes["EXCLUIDO"]:
        por_que = p["por_que"]
        if "colega de casa" in por_que:
            rotulo = "colegas da Valor"
        elif "concorrente" in por_que:
            rotulo = "mercado financeiro (concorrentes)"
        else:
            rotulo = "sem potencial de aporte hoje"
        motivos_fora[rotulo] += 1
    if motivos_fora:
        linhas.append("\n## Por que sairam da lista\n")
        for motivo, qtd in motivos_fora.most_common():
            linhas.append(f"- {motivo}: {qtd}")

    linhas.append(
        "\n---\n\n**Proximo passo:** rode `python3 2-briefings.py` "
        "para gerar as fichas de analise dos primeiros leads.\n"
    )

    with open(os.path.join(SAIDA, "resumo.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(linhas))


if __name__ == "__main__":
    main()
