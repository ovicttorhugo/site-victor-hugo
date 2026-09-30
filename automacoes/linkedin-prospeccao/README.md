# Prospecção no LinkedIn — passo a passo

Sistema pra transformar suas conexões paradas em conversas reais, usando SPIN
selling e análise do que a pessoa já publica.

**Divisão do trabalho:** os scripts daqui decidem **com quem falar**. O Claude
para Chrome lê o perfil, analisa o conteúdo e **escreve a mensagem dentro da
caixa de conversa do LinkedIn**. Você lê e aperta enviar.

O envio fica com você de propósito: extensão enviando sozinha vira disparo em
massa, e é isso que o LinkedIn detecta e pune. Sua conta vale mais que os 3
segundos economizados.

---

## Antes de tudo: o que você precisa

Só isso:

- Seu arquivo de conexões do LinkedIn (te ensino a pegar no passo 1)
- Python instalado (já vem no Mac e no Linux; no Windows baixe em python.org)
- A extensão **Claude para Chrome** instalada (é ela que faz o trabalho pesado)
- Cerca de 20 minutos por dia

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

## PASSO 3 — O Claude analisa e escreve (1 minuto por lead)

**É aqui que o tempo é economizado de verdade.**

1. Abra `saida/1-prioridade-A.csv` e pegue o próximo da fila
2. Abra o perfil da pessoa no LinkedIn, no Chrome
3. Abra o painel do Claude na lateral direita
4. Cole o **PROMPT 1** do arquivo `prompt-claude-chrome.md`

Ele devolve: quem é a pessoa, experiências anteriores, o que publica e com que
frequência, sinais de momento, hipótese da situação financeira (separando o que
ele viu do que é chute) e o melhor gancho pra abrir a conversa.

5. Se aprovar a análise, cole o **PROMPT 2**

Ele abre a conversa e **escreve a mensagem na caixa, sem enviar.**

> **Por que a extensão consegue e este chat aqui não:** ela roda dentro do seu
> navegador, na sua sessão já logada. Não tem robô logando de fora nem
> credencial guardada em lugar nenhum. Já este ambiente na nuvem não tem
> navegador seu, e o LinkedIn está bloqueado no proxy de rede dele.

---

## PASSO 4 — Você lê e envia

1. Leia a mensagem que ficou escrita na caixa
2. **Confira se o gancho está certo** — o Claude às vezes cita post errado ou
   entende a empresa errada. Em 1 de cada 10 você vai corrigir algo, e é
   justamente isso que faz a mensagem não parecer automática.
3. Ajuste o que quiser e **envie você**
4. Marque `status` = `enviado` na linha da pessoa no CSV

> Marcar o status importa: o gerador de fichas **pula** quem já tem status
> preenchido, então você nunca manda duas vezes pra mesma pessoa.

**Quando a pessoa responder**, use o **PROMPT 3**. Ele escreve o próximo turno
do SPIN em cima do que ela disse.

---

## Plano B — a ficha manual

Se a extensão travar, se o perfil não abrir, ou se você preferir trabalhar sem
Chrome, o caminho manual continua valendo:

```bash
python3 2-briefings.py        # gera 15 fichas em saida/briefings/
python3 2-briefings.py 25     # ou 25 fichas
python3 2-briefings.py 10 B   # ou 10 da prioridade B
```

Você abre a ficha, olha o perfil, cola os últimos posts e marca os sinais.
Depois manda o arquivo pro Claude com **"escreve a mensagem desta ficha"**.

Leva 5 a 8 minutos por lead em vez de 1. Mas funciona em qualquer navegador,
sem depender de extensão nenhuma.

**Quando a pessoa responder**, me mande a resposta dela. Eu escrevo o próximo
turno do SPIN em cima do que ela disse.

---

## A rotina da semana

| Quando | O quê | Tempo |
|---|---|---|
| **Segunda de manhã** | Rodar o classificador e abrir a fila da semana | 10 min |
| **Todo dia** | 3 leads pela extensão: analisar, ler, enviar | 10 min/dia |
| **Todo dia** | Responder quem respondeu (PROMPT 3) | 10 min |
| **Sexta à tarde** | Atualizar o CSV e ver o que funcionou | 15 min |

**Total: menos de 2 horas por semana.** Dá 15 abordagens boas, que viram umas
5 respostas e 1 reunião. Toda semana, acumulando.

> **Teto de segurança: no máximo ~20 por dia.** Acima disso o padrão fica
> visível mesmo com mensagens diferentes, e o LinkedIn limita a conta. As 15
> por semana do playbook estão muito abaixo disso de propósito.

---

## Os arquivos

```
linkedin-prospeccao/
├── README.md               ← você está aqui
├── prompt-claude-chrome.md ← os 3 prompts da extensão          ⭐⭐ o principal
├── playbook-spin.md        ← as mensagens prontas e o SPIN      ⭐ leia
├── compliance.md           ← o que você não pode escrever       ⭐ leia
├── regras.py               ← os filtros (edite pra afinar)
├── 1-classificar.py        ← passo 2
├── 2-briefings.py          ← plano B (ficha manual)
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
