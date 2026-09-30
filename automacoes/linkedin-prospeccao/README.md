# Prospecção no LinkedIn — passo a passo

Sistema pra transformar suas conexões paradas em conversas reais, usando SPIN
selling e análise do que a pessoa já publica.

**Divisão do trabalho:** a máquina filtra, analisa e escreve. **Você olha o
perfil e aperta enviar.** O envio é manual de propósito — robô de DM derruba
conta de assessor, e a sua vale mais que o tempo economizado.

---

## Antes de tudo: o que você precisa

Só isso:

- Seu arquivo de conexões do LinkedIn (te ensino a pegar no passo 1)
- Python instalado (já vem no Mac e no Linux; no Windows baixe em python.org)
- 40 minutos na segunda-feira + 20 minutos por dia

---

## PASSO 1 — Baixar suas conexões (5 minutos, você faz uma vez)

1. Abra o LinkedIn no **computador** (no celular não tem essa opção)
2. Clique na sua foto → **Configurações e privacidade**
3. No menu da esquerda: **Privacidade de dados**
4. Clique em **Obter uma cópia dos seus dados**
5. Marque **"Quero alguns dos seus dados"** e selecione só **Conexões**
6. Clique em **Solicitar arquivo**
7. O LinkedIn manda um e-mail em **10 a 30 minutos** com o link
8. Baixe o `.zip`, abra, e dentro tem o **`Connections.csv`**

Coloque esse arquivo na pasta `entrada/`:

```
automacoes/linkedin-prospeccao/entrada/Connections.csv
```

> **Por que assim e não um robô lendo o LinkedIn?** Porque esse arquivo é seu, o
> LinkedIn te entrega de bom grado, e não infringe nada. Robô que lê perfil em
> massa é violação de contrato e derruba conta. Ver `compliance.md`.

---

## PASSO 2 — Filtrar quem vale a pena (10 segundos)

Abra o terminal na pasta do projeto e rode:

```bash
cd automacoes/linkedin-prospeccao
python3 1-classificar.py entrada/Connections.csv
```

Vai aparecer assim:

```
  1.847 conexoes lidas

  PRIORIDADE A (donos de negocio) ....   214
  PRIORIDADE B (alta renda) ..........   389
  Baixa prioridade ...................   901
  Excluidos (financeiro/sem fit) .....   343
```

**O que cada faixa quer dizer:**

| Faixa | Quem é | O que fazer |
|---|---|---|
| **A** | Dono, sócio, CEO, fundador, proprietário | Abordar primeiro. Decide sozinho sobre o dinheiro. |
| **B** | CFO, diretor, médico, advogado, dev sênior | Abordar depois. Alta renda, mas não é dono. |
| **Baixa** | Júnior, assistente, sem fit de aporte hoje | Não abordar 1:1. Só recebe seu conteúdo. |
| **Excluídos** | Mercado financeiro, colegas da Valor, estudantes | Não abordar. São concorrentes ou não são público. |

Agora **abra `saida/resumo.md`** e bata o olho. Se tiver alguém na lista errada,
é só me avisar que eu ajusto as regras.

---

## PASSO 3 — Gerar as fichas da semana (5 segundos)

```bash
python3 2-briefings.py
```

Isso cria **15 fichas** em `saida/briefings/`, uma por lead, já em ordem de
prioridade. Quer mais ou menos?

```bash
python3 2-briefings.py 25      # 25 fichas
python3 2-briefings.py 10 B    # 10 fichas da prioridade B
```

---

## PASSO 4 — Preencher a ficha (5 a 8 minutos por lead)

**Esta é a única parte que dá trabalho. E é ela que faz a coisa funcionar.**

1. Abra a ficha (ex.: `saida/briefings/01-marcelo-andrade.md`)
2. Abra o perfil da pessoa no LinkedIn (o link está na ficha)
3. Vá na aba **Publicações** do perfil
4. Preencha a **PARTE 1**:
   - Com que frequência ela posta
   - **Cole os últimos 5 posts** (o texto mesmo, não resuma)
   - Marque os sinais que você viu (contratação, obra, reclamação de imposto...)
   - Anote se vocês têm alguma história em comum

> **Dica que economiza tempo:** faça 3 fichas de uma vez, seguidas. Você entra
> num ritmo e cai pra uns 4 minutos cada.

> **Se a pessoa não posta nada:** preencha assim mesmo, marque "Silencioso" e
> siga. Tem exemplo de mensagem pra esse caso no playbook (exemplo 7).

---

## PASSO 5 — Eu escrevo a mensagem

Abra o Claude e mande:

> **"escreve a mensagem desta ficha"** + cole o conteúdo inteiro do arquivo

Eu devolvo:

1. **Leitura do perfil** — o que os posts revelam sobre a pessoa e o negócio
2. **Hipótese da situação financeira** — e o quanto disso é chute (eu declaro)
3. **A mensagem 1** pronta pra copiar e colar
4. **O plano dos próximos 3 turnos** — Problema, Implicação, Necessidade
5. **O que não dizer** com aquele perfil específico

---

## PASSO 6 — Enviar e anotar

1. Copie a mensagem, cole na DM do LinkedIn, **leia uma vez em voz alta**
   (se soar estranho falando, soa estranho lendo)
2. Envie
3. Volte na ficha e preencha o bloco **Controle** no final
4. Marque `status` = `enviado` na linha da pessoa em `saida/1-prioridade-A.csv`

> Marcar o status importa: o gerador **pula** quem já tem status preenchido,
> então você nunca manda duas vezes pra mesma pessoa.

**Quando a pessoa responder**, me mande a resposta dela. Eu escrevo o próximo
turno do SPIN em cima do que ela disse.

---

## A rotina da semana

| Quando | O quê | Tempo |
|---|---|---|
| **Segunda de manhã** | Rodar o passo 3 e preencher 5 fichas | 40 min |
| **Terça a sexta** | Preencher 2~3 fichas + enviar | 20 min/dia |
| **Todo dia** | Responder quem respondeu | 10 min |
| **Sexta à tarde** | Atualizar o CSV e ver o que funcionou | 15 min |

**Total: menos de 3 horas por semana.** Dá 15 abordagens boas, que viram umas
5 respostas e 1 reunião. Toda semana, acumulando.

---

## Os arquivos

```
linkedin-prospeccao/
├── README.md              ← você está aqui
├── playbook-spin.md       ← as mensagens prontas e o método SPIN  ⭐ leia
├── compliance.md          ← o que você não pode escrever          ⭐ leia
├── regras.py              ← os filtros (edite pra afinar)
├── 1-classificar.py       ← passo 2
├── 2-briefings.py         ← passo 3
├── entrada/               ← ponha o Connections.csv aqui
├── exemplos/              ← um CSV de exemplo pra testar antes
└── saida/                 ← tudo que os scripts geram
    ├── resumo.md          ← o panorama da sua base
    ├── fila.md            ← a lista da semana
    ├── 1-prioridade-A.csv ← seus melhores leads
    ├── 2-prioridade-B.csv
    ├── 3-baixa-prioridade.csv
    ├── 0-excluidos.csv    ← confira de vez em quando se sobrou alguém bom
    └── briefings/         ← as fichas
```

---

## Quer testar antes de baixar seus dados?

```bash
python3 1-classificar.py exemplos/Connections-exemplo.csv
python3 2-briefings.py 5
```

Roda com 30 conexões fictícias e você vê exatamente o que sai.

---

## Ajustar o filtro

Tudo que decide quem entra e quem sai está em **`regras.py`**, comentado em
português. Exemplos do que dá pra mudar:

- Excluir mais uma corretora → adicione em `EXCLUIR_EMPRESA_FINANCEIRA`
- Priorizar um setor (ex.: agro) → aumente o peso em `SETORES_BONUS`
- Receber mais ou menos gente na faixa A → mexa em `CORTE_PRIORIDADE_A`
- Mudar a meta semanal → `META_SEMANAL`

Se preferir, só me fala o que quer mudar que eu mexo.

---

## Onde isso pode ir depois

Quando a rotina estiver rodando, dá pra evoluir:

- **Conteúdo puxado pelo filtro** — o `resumo.md` mostra os setores mais fortes
  da sua base. Se der construtora e agro, seu carrossel da semana fala com eles.
- **Painel de acompanhamento** — taxa de resposta por setor, pra saber onde
  você converte melhor.
- **Integração com o n8n** — o servidor n8n está configurado aqui mas falhou ao
  conectar nesta sessão (erro 404). Quando você reativar, dá pra automatizar o
  lembrete diário e o controle de follow-up.
