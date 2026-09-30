# O prompt do Claude para Chrome

Este é o arquivo que faz a semi-automação acontecer de verdade: o Claude lê o
perfil aberto na sua frente, analisa o conteúdo público, e **escreve a mensagem
dentro da caixa de conversa do LinkedIn sem enviar.** Você lê, ajusta se quiser,
e aperta enter.

---

## Setup (uma vez só, 5 minutos)

1. Instale a extensão **Claude para Chrome** na Chrome Web Store
2. Faça login com a sua conta Claude
3. Abra o LinkedIn normalmente, já logado
4. Abra o painel do Claude na lateral direita do Chrome

Pronto. A extensão enxerga a aba que está na sua frente, inclusive páginas atrás
de login — porque é o **seu** navegador e a **sua** sessão. Não tem robô logando
de fora, não tem credencial guardada em lugar nenhum, não tem IP de datacenter.
É por isso que este caminho funciona e o outro não.

---

## Como usar no dia a dia

1. Abra `saida/1-prioridade-A.csv` e pegue o próximo da fila
2. Abra o perfil da pessoa no LinkedIn
3. No painel do Claude, cole o **PROMPT 1** abaixo
4. Leia a análise que ele devolve
5. Se aprovar, mande o **PROMPT 2**
6. Confira a mensagem na caixa, ajuste o que quiser, **envie você**
7. Marque `enviado` na coluna `status` do CSV

Tempo por lead: **cerca de 1 minuto.** Era 5 a 8 minutos preenchendo ficha na mão.

---

# PROMPT 1 — análise do perfil

> Copie daqui até o fim do bloco e cole no painel do Claude, com o perfil aberto.

```
Você está me ajudando a prospectar no LinkedIn. Eu sou o Victor Hugo, assessor
de investimentos vinculado à Valor Investimentos, atendimento remoto em todo o
Brasil, sem aporte mínimo.

Analise o perfil que está aberto nesta aba e me devolva, nesta ordem:

## 1. CHECAGEM DE DESCARTE (faça primeiro, é eliminatória)
Esta pessoa é do mercado financeiro — assessor, agente autônomo, planejador,
private banker, gerente de banco, analista de investimentos, gestor, corretor
de seguros, consórcio — ou trabalha na Valor Investimentos?

- Se SIM: responda apenas "DESCARTAR: [motivo]" e pare aqui. Não analise, não
  escreva mensagem.
- Atenção: quem trabalha EM banco ou fintech mas na área de tecnologia, produto,
  design, dados ou RH NÃO é concorrente. Essa pessoa segue como lead.
- Se NÃO: siga para o item 2.

## 2. QUEM É
- Cargo atual e há quanto tempo
- É dono/sócio do negócio ou é contratado?
- Experiências anteriores (o que a trajetória diz sobre ela)
- Formação, se for relevante
- Porte e setor da empresa atual

## 3. O QUE ELA PUBLICA
Abra a aba "Publicações" do perfil e olhe os últimos posts.
- Frequência: ativo (semanal), ocasional (mensal), raro, ou silencioso
- Data do post mais recente
- Os 5 temas principais que ela toca
- Quais posts engajaram mais (curtidas e comentários)
- O tom dela: técnico, pessoal, institucional, opinativo?

## 4. SINAIS DE MOMENTO
Procure e liste o que encontrar:
- Negócio: contratando, inaugurou, lançou, premiou, expandiu, reclamou de
  imposto/custo/juros/banco, sucessão, fusão, aporte
- Vida: mudança, família, formação, viagem, cansaço, rotina
- Dinheiro: já falou de investimento, aposentadoria, banco, tributária, holding

## 5. HIPÓTESE DA SITUAÇÃO FINANCEIRA
O que provavelmente acontece com o dinheiro dessa pessoa hoje.
**Marque cada afirmação como [VI NO PERFIL] ou [CHUTE MEU].** Não misture as
duas coisas, eu preciso saber no que confiar.

## 6. O MELHOR GANCHO
Qual post ou fato específico eu uso pra abrir a conversa, e por quê.

Seja direto. Se o perfil for pobre em informação, diga isso em vez de inventar.
```

---

# PROMPT 2 — escrever a mensagem na caixa

> Só mande depois de ler e aprovar a análise.

```
Aprovado. Agora:

1. Abra a conversa do LinkedIn com esta pessoa (botão "Mensagem" no perfil)
2. Escreva a mensagem na caixa de texto
3. **NÃO ENVIE.** Deixe escrita. Quem envia sou eu.

Regras da mensagem (todas obrigatórias):

ESTRUTURA — três partes, nesta ordem:
1. Gancho real: "conectamos há X e nunca puxei assunto" ou "vi seu post sobre Y"
2. Apresentação em UMA linha: sou assessor de investimentos + âncora de SETOR
   (ex.: "atendo bastante gente do agro"). Nunca âncora de cidade, eu sou remoto.
3. UMA pergunta de SITUAÇÃO, curiosa, sobre o NEGÓCIO dela — nunca sobre dinheiro

LIMITES:
- Máximo 90 palavras. Se passou, corte.
- Uma pergunta só. Duas viram formulário.
- A pergunta tem que nascer de algo real que você viu no perfil.
- Português brasileiro, formal mas natural. Como eu falaria, não como folheto.
- Sem despedida, sem "fico à disposição", sem assinatura.

PROIBIDO (isso me cria problema com a CVM, não é frescura):
- Qualquer promessa ou número de rentabilidade
- Nome de produto ou ativo específico
- "Sem risco", "garantido", "oportunidade fechando"
- Recomendação de investimento de qualquer tipo
- Link, PDF, anexo
- Pedir reunião, call ou "15 minutinhos"
- Me chamar de consultor, planejador ou gestor. Sou ASSESSOR de investimentos.

Depois de escrever na caixa, me mostre aqui no chat:
- O texto exato que você deixou escrito
- A contagem de palavras
- O plano dos próximos 3 turnos do SPIN (Problema, Implicação, Necessidade),
  caso ela responda
```

---

# PROMPT 3 — quando ela responder

```
A pessoa respondeu isto:

"[cole a resposta dela aqui]"

Escreva o próximo turno na caixa de conversa, sem enviar.

Onde estamos no SPIN: [S / P / I / N]

Regras:
- Devolva algo do que ela disse antes de perguntar (mostra que você leu)
- Avance UMA letra do SPIN, não duas
- Mais curto que a mensagem anterior
- Só convide pra conversar se já estivermos no N
- As mesmas proibições de compliance continuam valendo

Se ela perguntou o que eu vendo ou o que eu faço: responda direto e simples,
sem rodeio. Ela abriu a porta, não precisa mais de SPIN.
```

---

## Os três limites que eu peço que você mantenha

Não é a extensão que impõe, sou eu que recomendo — e o motivo é prático:

| Limite | Por quê |
|---|---|
| **Você aperta enviar, sempre** | Deixar a extensão enviar sozinha transforma isso em disparo em massa. É o que o LinkedIn detecta e pune. |
| **Máximo ~20 por dia** | Acima disso o padrão fica visível mesmo com mensagens diferentes. As 15/semana do playbook estão muito abaixo. |
| **Leia antes de enviar** | O Claude erra. Vai citar post errado, entender empresa errada. Em 1 de cada 10 você vai corrigir algo — e é justamente isso que faz a mensagem não parecer automática. |

---

## Se a extensão travar ou o perfil não abrir

Plano B, que sempre funciona: copie o perfil inteiro (Ctrl+A, Ctrl+C na página),
cole aqui no Claude Code junto com o PROMPT 1. A análise sai igual. Só a parte
de escrever na caixa você faz na mão.
