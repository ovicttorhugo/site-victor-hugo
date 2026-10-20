# Projeto: Site do Victor Hugo (Valor Investimentos)

Site de divulgação do Victor Hugo, assessor de investimentos. Objetivo: captar
clientes e divulgar conteúdo. Idioma do site: português (pt-BR).

## Stack
Site **estático**, sem framework: HTML + CSS + JavaScript puro. Não há build,
não há node_modules, não há backend ainda. Hospedagem pretendida: **Vercel**.

## Mapa dos arquivos (onde mexer)
- `site/index.html` — a página principal (uma página só). É aqui que fica quase tudo.
- `site/style.css` — todo o estilo do site.
- `site/main.js` — o JavaScript do site.
- `site/img/` — imagens. `site/img/portfolio/` tem as artes dos carrosséis/conteúdo.
- `site/artigos/*.html` — artigos publicados (HTML).
- `artigos/*.md` — rascunhos dos artigos em markdown (fonte antes de virar HTML).

## Convenções
- Manter tudo em pt-BR.
- CSS: seguir o padrão já existente em `style.css` (não introduzir framework).
- Não adicionar dependências nem ferramentas de build sem o Victor pedir.

## Back-end planejado (ainda não implementado)
Formulário de contato → e-mail (via **Resend**) + guardar leads (via **Supabase**).
Skills de apoio já instaladas em `.claude/skills/`.

## Skills disponíveis neste repo (.claude/skills/)
- `frontend-design` — direção visual (cores, tipografia, layout).
- `theme-factory` — 10 temas prontos de cor/fonte.
- `webapp-testing` — testar o site no navegador (Playwright).
- `resend` + `email-best-practices` — envio de e-mail do formulário.

## Preferências do Victor
Tem 19 anos, prefere explicações diretas, com exemplos e praticidade. Seja
objetivo e sempre termine dizendo o próximo passo concreto. O CRM dele é um
sistema À PARTE (app local na máquina dele), NÃO faz parte deste repositório.
