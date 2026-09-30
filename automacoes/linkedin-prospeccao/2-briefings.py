#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PASSO 2 - Gera uma ficha por lead para a analise de conteudo.

Como usar:
    python3 2-briefings.py            # 15 leads da prioridade A
    python3 2-briefings.py 25         # 25 leads
    python3 2-briefings.py 10 B       # 10 leads da prioridade B

Cada ficha e um arquivo .md em saida/briefings/. Voce abre o perfil da
pessoa, copia os ultimos posts, cola na ficha e manda a ficha pro Claude.
Quem escreve a mensagem e o Claude - a ficha e a materia-prima dele.

Leads que ja tem algo na coluna "status" do CSV sao pulados.
"""
import csv
import os
import re
import sys
import unicodedata
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import regras  # noqa: E402

BASE = os.path.dirname(os.path.abspath(__file__))
SAIDA = os.path.join(BASE, "saida")
BRIEFINGS = os.path.join(SAIDA, "briefings")

FICHA = """# Ficha de abordagem - {nome}

> Preencha a PARTE 1 olhando o perfil. Depois mande este arquivo inteiro
> pro Claude com a frase: **"escreve a mensagem desta ficha"**.

## Dados da conexao

| Campo | Valor |
|---|---|
| Nome | {nome} |
| Cargo | {cargo} |
| Empresa | {empresa} |
| Perfil | {url} |
| Faixa | {faixa} (nota {nota}) |
| Conectados ha | {meses} meses |
| Por que entrou na lista | {por_que} |

---

# PARTE 1 - O que voce preenche (5 a 8 minutos no perfil)

## 1.1 Frequencia de publicacao

Abra o perfil > aba "Publicacoes" > veja as datas.

- [ ] **Ativo** - posta toda semana ou mais
- [ ] **Ocasional** - posta 1 ou 2 vezes por mes
- [ ] **Raro** - postou poucas vezes no ano
- [ ] **Silencioso** - nao posta, so curte e comenta
- [ ] **Fantasma** - perfil parado, sem atividade nenhuma

Data do post mais recente: `__/__/____`
Quantos posts nos ultimos 90 dias: `___`

## 1.2 Os ultimos posts (cole aqui, do mais novo pro mais antigo)

Cole o texto mesmo, nao resuma. Se tiver imagem ou carrossel, descreva
em uma linha. Anote curtidas e comentarios - mostra o que engajou.

### Post 1 - data __/__/____ - ___ curtidas, ___ comentarios
```
(cole aqui)
```

### Post 2 - data __/__/____ - ___ curtidas, ___ comentarios
```
(cole aqui)
```

### Post 3 - data __/__/____ - ___ curtidas, ___ comentarios
```
(cole aqui)
```

### Post 4 - data __/__/____ - ___ curtidas, ___ comentarios
```
(cole aqui)
```

### Post 5 - data __/__/____ - ___ curtidas, ___ comentarios
```
(cole aqui)
```

## 1.3 Sinais do momento de vida e do negocio

Marque o que voce viu. Cada X aqui vira uma pergunta melhor na mensagem.

**No negocio**
- [ ] Contratando / vaga aberta / time crescendo
- [ ] Inaugurou unidade, filial ou nova sede
- [ ] Lancou produto, servico ou linha nova
- [ ] Comemorou aniversario da empresa ou marco de faturamento
- [ ] Recebeu premio, certificacao ou selo
- [ ] Falou de exportacao, importacao ou expansao regional
- [ ] Falou de safra, colheita, obra entregue ou contrato fechado
- [ ] Reclamou de imposto, custo, juros, banco ou fluxo de caixa
- [ ] Mencionou socio saindo, entrando ou sucessao familiar
- [ ] Falou de venda da empresa, fusao ou aporte recebido

**Na vida**
- [ ] Mudou de cidade ou de pais
- [ ] Casamento, filho, formatura na familia
- [ ] Pos-graduacao, MBA ou curso longo
- [ ] Viagem, hobby caro, carro, imovel
- [ ] Falou de tempo, cansaco, rotina puxada ou saude

**Sobre dinheiro (ouro puro se tiver)**
- [ ] Ja falou de investimento, poupanca, CDB, acoes, cripto
- [ ] Ja falou de aposentadoria ou futuro dos filhos
- [ ] Ja reclamou de banco, tarifa ou rendimento baixo
- [ ] Ja falou de reforma tributaria ou holding familiar
- [ ] Nunca tocou no assunto financeiro

## 1.4 Tem historia em comum?

- [ ] Evento que os dois foram
- [ ] Conhecido em comum (quem: ___________)
- [ ] Mesma cidade ou regiao
- [ ] Mesma faculdade
- [ ] Ja trocamos mensagem antes (quando: ___________)
- [ ] Ja comentei em post dele(a)
- [ ] Nada em comum, foi conexao fria

## 1.5 Observacao livre

```
(qualquer coisa que te chamou atencao e nao coube acima)
```

---

# PARTE 2 - O que o Claude devolve

Nao preencha. Quando voce mandar a ficha, volta assim:

1. **Leitura do perfil** - o que os posts dizem sobre a pessoa e o negocio
2. **Hipotese de situacao financeira** - o que provavelmente acontece com o
   dinheiro dela hoje, e o quanto disso e chute (declarado)
3. **Mensagem 1** - apresentacao + pergunta de SITUACAO, curta, sem venda
4. **Plano dos proximos 3 turnos** - Problema, Implicacao, Necessidade
5. **O que NAO dizer** - as armadilhas desse perfil especifico

---

## Controle

- Mensagem enviada em: `__/__/____`
- Respondeu? [ ] sim [ ] nao [ ] ainda nao
- Como respondeu:
```

```
- Proximo passo:
"""


def normalizar_nome(nome):
    texto = unicodedata.normalize("NFKD", nome)
    texto = "".join(c for c in texto if not unicodedata.combining(c))
    texto = re.sub(r"[^a-zA-Z0-9]+", "-", texto).strip("-").lower()
    return texto or "sem-nome"


def main():
    quantidade = regras.META_SEMANAL
    faixa = "A"
    if len(sys.argv) > 1:
        quantidade = int(sys.argv[1])
    if len(sys.argv) > 2:
        faixa = sys.argv[2].upper()

    arquivo = os.path.join(
        SAIDA, "1-prioridade-A.csv" if faixa == "A" else "2-prioridade-B.csv"
    )
    if not os.path.exists(arquivo):
        raise SystemExit(
            f"Nao achei {arquivo}.\nRode antes: python3 1-classificar.py entrada/Connections.csv"
        )

    os.makedirs(BRIEFINGS, exist_ok=True)

    with open(arquivo, encoding="utf-8-sig", newline="") as fh:
        leads = list(csv.DictReader(fh))

    pendentes = [l for l in leads if not (l.get("status") or "").strip()]
    escolhidos = pendentes[:quantidade]

    if not escolhidos:
        print("\n  Todos os leads dessa faixa ja tem status preenchido.")
        print("  Limpe a coluna 'status' no CSV ou use a outra faixa.\n")
        return

    criados, pulados = 0, 0
    for i, lead in enumerate(escolhidos, 1):
        slug = f"{i:02d}-{normalizar_nome(lead['nome'])}.md"
        destino = os.path.join(BRIEFINGS, slug)
        if os.path.exists(destino):
            pulados += 1
            continue
        meses = lead.get("meses_conexao") or "?"
        with open(destino, "w", encoding="utf-8") as fh:
            fh.write(FICHA.format(
                nome=lead["nome"],
                cargo=lead.get("cargo") or "-",
                empresa=lead.get("empresa") or "-",
                url=lead.get("url") or "-",
                faixa=faixa,
                nota=lead.get("nota") or "-",
                meses=meses,
                por_que=lead.get("por_que") or "-",
            ))
        criados += 1

    print(f"\n  {criados} fichas criadas em saida/briefings/")
    if pulados:
        print(f"  {pulados} ja existiam e foram preservadas (nao sobrescrevo seu trabalho)")
    print(f"\n  Ritmo sugerido: {regras.META_SEMANAL} por semana, 3 por dia.")
    print("  Abra a primeira ficha e preencha a PARTE 1.\n")

    indice = [
        f"# Fila de abordagem - prioridade {faixa}",
        f"\nGerada em {datetime.now().strftime('%d/%m/%Y')}\n",
        "| # | Lead | Cargo | Ficha | Preenchida | Enviada |",
        "|---|---|---|---|---|---|",
    ]
    for i, lead in enumerate(escolhidos, 1):
        slug = f"{i:02d}-{normalizar_nome(lead['nome'])}.md"
        indice.append(
            f"| {i} | {lead['nome']} | {lead.get('cargo','')[:35]} | "
            f"[abrir](briefings/{slug}) | [ ] | [ ] |"
        )
    with open(os.path.join(SAIDA, "fila.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(indice) + "\n")


if __name__ == "__main__":
    main()
