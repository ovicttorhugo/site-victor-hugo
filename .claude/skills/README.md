# Skills do Claude Code

Skills instaladas neste projeto. Elas ativam automaticamente quando o Claude
percebe que a tarefa combina com a descrição de cada uma.

| Skill | Pra que serve | Licença |
|---|---|---|
| **frontend-design** | Direção visual do site: paleta de cores, tipografia e layout com identidade própria (sem cara de template) | Apache 2.0 |
| **webapp-testing** | Testa o site num navegador de verdade (Playwright): confere se funciona, tira prints e lê erros | Apache 2.0 |
| **theme-factory** | 10 temas prontos (cores + fontes) pra aplicar no site, slides ou landing pages | Apache 2.0 |

## Back-end (formulário de contato + e-mail + leads)

Hospedagem escolhida: **Vercel**.

| Skill | Pra que serve | Licença |
|---|---|---|
| **resend** | Envia e-mail pelo Resend: quando alguém preenche o formulário do site, o lead cai no seu e-mail automaticamente | MIT |
| **email-best-practices** | Evita cair no spam: configura SPF/DKIM/DMARC, captura de e-mail, conformidade (LGPD/CAN-SPAM) e acessibilidade | MIT |

**Banco de dados dos leads:** recomendado **Supabase** (tem painel visual pra ver
os contatos numa tabela, sem precisar de SQL). Ainda não instalado porque depende
de você criar uma conta gratuita em supabase.com primeiro. Quando criar, me avise
que eu configuro a tabela de leads e conecto no formulário.

## Slides / Apresentações

Pra criar PowerPoint (`.pptx`) o Claude já tem a skill oficial embutida na
sessão (`pptx`), não precisa instalar aqui. Pra carrossel de Instagram, use o
**CarrosseIA** (já conectado na sua conta).

## Onde achar mais skills

- https://github.com/anthropics/skills (oficiais da Anthropic)
- https://github.com/VoltAgent/awesome-agent-skills (comunidade, +1000)
- https://github.com/hesreallyhim/awesome-claude-code (lista geral)
