# -*- coding: utf-8 -*-
"""
Dicionarios de classificacao das conexoes do LinkedIn.

Este e o unico arquivo que voce precisa editar quando quiser
afinar o filtro (ex.: incluir um setor novo, excluir um concorrente).
Tudo aqui e comparado em minusculo e sem acento.
"""

# ---------------------------------------------------------------------------
# 1. EXCLUSOES DURAS - quem NUNCA vira lead
# ---------------------------------------------------------------------------
# 1a) CARGO do mercado financeiro -> exclusao DURA, nao importa a empresa.
EXCLUIR_CARGO_FINANCEIRO = [
    "assessor de investimentos", "assessora de investimentos",
    "assessor financeiro", "agente autonomo", "agente autonoma",
    "agente autonomo de investimentos", "aai",
    "consultor de investimentos", "consultora de investimentos",
    "planejador financeiro", "planejadora financeira",
    "especialista de investimentos", "especialista em investimentos",
    "private banker", "private banking", "banker",
    "gerente de relacionamento", "gerente de contas", "gerente pj",
    "gerente de agencia", "bancario", "bancaria",
    "analista de investimentos", "gestor de fundos", "gestora de fundos",
    "trader", "day trader", "operador de mesa", "mesa de operacoes",
    "economista chefe", "research", "analista cnpi", "cnpi",
    "cfp", "cea ", "ancord", "cpa-20", "cpa 20", "cvm",
    "corretor de seguros", "corretora de seguros", "consorcio",
    "previdencia privada", "cambio", "credito consignado",
    "wealth management", "wealth manager", "family office",
    "asset management", "gestor de patrimonio", "gestora de patrimonio",
    "fund manager", "investment advisor", "financial advisor",
]

# 1b) EMPRESA do mercado financeiro -> exclusao CONDICIONAL.
# So exclui se o cargo tambem for da area comercial/financeira.
# Um engenheiro de software do Nubank NAO e concorrente: e uma boa lead.
EXCLUIR_EMPRESA_FINANCEIRA = [
    # a propria casa (essa sim exclui sempre - sao colegas)
    "xp investimentos", "xp inc", "btg pactual", "rico investimentos",
    "clear corretora", "nubank", "inter ", "banco inter", "c6 bank",
    "itau", "itau unibanco", "bradesco", "santander", "banco do brasil",
    "caixa economica", "safra", "banrisul", "sicredi", "sicoob",
    "avenue securities", "genial investimentos", "orama", "modalmais",
    "warren", "toro investimentos", "empiricus", "suno research",
    "nord research", "levante", "guide investimentos", "necton",
    "ativa investimentos", "terra investimentos", "mirae asset",
    "blackrock", "jp morgan", "goldman sachs", "morgan stanley",
    "credit suisse", "ubs ", "julius baer", "vitreo", "spiti",
    "monetus", "faz capital", "eqi investimentos", "messem",
    "blue3", "manchester investimentos", "acqua vero", "svn investimentos",
    "the hill capital", "one investimentos", "lifetime investimentos",
]

# 1c) A propria casa: colega e colega, seja da TI ou da mesa. Exclui sempre.
EXCLUIR_EMPRESA_SEMPRE = [
    "valor investimentos", "valorinvestimentos",
]

# 1d) Cargos que RESGATAM alguem de uma empresa financeira.
# Sao funcoes de apoio: nao concorrem com voce e costumam ter boa renda
# (muitas vezes com stock options pra alocar).
CARGOS_RESGATE_NAO_CONCORRENTE = [
    "engenheiro de software", "engenheira de software", "desenvolvedor",
    "desenvolvedora", "software engineer", "backend", "back-end",
    "frontend", "front-end", "full stack", "fullstack", "mobile",
    "devops", "sre", "seguranca da informacao", "infraestrutura",
    "dados", "data engineer", "data scientist", "cientista de dados",
    "machine learning", "qa ", "quality assurance", "tech lead",
    "arquiteto de software", "staff engineer", "principal engineer",
    "designer", "ux", "ui ", "product designer",
    "produto", "product manager", "product owner",
    "recursos humanos", "people", "rh ", "recrutamento",
    "juridico", "compliance interno", "facilities", "suprimentos",
]

# Perfis sem capacidade de aporte hoje (nao sao concorrentes, so nao sao
# o publico agora). Vao para a lista "fora do radar".
EXCLUIR_SEM_POTENCIAL = [
    "estudante", "estagiario", "estagiaria", "estagio", "student", "intern",
    "trainee", "aprendiz", "jovem aprendiz", "menor aprendiz",
    "bolsista", "iniciacao cientifica", "graduando", "graduanda",
    "em busca de", "em transicao", "open to work", "buscando oportunidade",
    "desempregado", "desempregada", "aberto a oportunidades",
    "aposentado pelo inss", "voluntario", "voluntaria",
]

# ---------------------------------------------------------------------------
# 2. CARGOS - quanto mais alto o peso, maior a prioridade
# ---------------------------------------------------------------------------
# TIER A: dono do proprio negocio. Decide sozinho sobre o dinheiro.
CARGOS_DONO = {
    "ceo": 50, "founder": 50, "co-founder": 50, "cofounder": 50,
    "fundador": 50, "fundadora": 50, "cofundador": 50, "cofundadora": 50,
    "socio": 50, "socia": 50, "socio-proprietario": 50, "socio fundador": 50,
    "socio diretor": 50, "managing partner": 50, "partner": 45,
    "proprietario": 50, "proprietaria": 50, "dono": 50, "dona": 48,
    "empresario": 50, "empresaria": 50, "owner": 50, "business owner": 50,
    "presidente": 48, "president": 45, "chairman": 45,
    "diretor executivo": 45, "diretora executiva": 45,
    "diretor presidente": 48, "administrador socio": 45,
    "franqueado": 42, "franqueada": 42, "investidor anjo": 45,
    "empreendedor": 42, "empreendedora": 42,
}

# TIER B: alta renda, decide sobre o proprio dinheiro, mas nao e dono.
CARGOS_ALTA_RENDA = {
    # c-level contratado
    "cfo": 40, "coo": 38, "cto": 38, "cmo": 36, "chro": 34, "cro": 36,
    "chief": 36, "vice presidente": 40, "vp ": 38, "vice-presidente": 40,
    "diretor": 36, "diretora": 36, "director": 34,
    "head de": 30, "head of": 30, "superintendente": 34,
    # liberais de alta renda
    "medico": 40, "medica": 40, "cirurgiao": 44, "cirurgia": 40,
    "cardiologista": 42, "ortopedista": 42, "dermatologista": 42,
    "oftalmologista": 42, "anestesista": 44, "anestesiologista": 44,
    "ginecologista": 40, "pediatra": 36, "psiquiatra": 40,
    "radiologista": 42, "urologista": 42, "neurocirurgiao": 46,
    "dentista": 32, "odontologia": 30, "implantodontista": 36,
    "ortodontista": 36, "cirurgiao dentista": 34,
    "advogado": 32, "advogada": 32, "juiz": 42, "juiza": 42,
    "desembargador": 46, "promotor de justica": 42, "procurador": 40,
    "delegado": 34, "defensor publico": 36, "auditor fiscal": 42,
    "notario": 40, "tabeliao": 42, "registrador": 40,
    "veterinario": 28, "veterinaria": 28, "nutricionista": 22,
    "fisioterapeuta": 22, "psicologo": 22, "psicologa": 22,
    "arquiteto": 26, "arquiteta": 26, "engenheiro civil": 28,
    "piloto": 38, "comandante": 38, "primeiro oficial": 30,
    # carreira corporativa senior
    "gerente geral": 30, "gerente senior": 26, "gerente nacional": 30,
    "gerente regional": 28, "gerente comercial": 26, "gerente industrial": 28,
    "coordenador": 18, "coordenadora": 18, "supervisor": 14,
    "especialista senior": 22, "consultor senior": 22,
    "engenheiro de software senior": 30, "tech lead": 28,
    "arquiteto de software": 30, "staff engineer": 32, "principal engineer": 34,
    "professor titular": 24, "professor universitario": 20,
    "produtor rural": 40, "pecuarista": 42, "agropecuarista": 42,
    "agronomo": 26, "engenheiro agronomo": 28,
}

# Penalidade: junior/pleno explicitos derrubam a nota.
CARGOS_PENALIDADE = {
    "junior": -35, "jr.": -30, "jr ": -30, "assistente": -30,
    "auxiliar": -35, "analista junior": -35, "analista pleno": -18,
    "operador": -20, "atendente": -30, "recepcionista": -30,
    "vendedor": -12, "motorista": -25, "tecnico": -12,
    "analista": -8, "freelancer": -10, "autonomo": -5,
}

# ---------------------------------------------------------------------------
# 3. SETORES DA EMPRESA - bonus por capacidade de geracao de caixa
# ---------------------------------------------------------------------------
SETORES_BONUS = {
    # saude
    "clinica": 14, "hospital": 12, "odontologia": 12, "laboratorio": 12,
    "odontologica": 12, "consultorio": 12, "instituto": 8, "centro medico": 14,
    "medicina": 12, "saude": 8, "estetica": 10, "farmacia": 10,
    # agro
    "agro": 16, "fazenda": 16, "agronegocio": 18, "agropecuaria": 16,
    "agricola": 14, "graos": 14, "soja": 14, "pecuaria": 14, "laticinios": 12,
    "cooperativa": 10, "sementes": 12, "frigorifico": 14,
    # industria e construcao
    "industria": 12, "metalurgica": 12, "usinagem": 10, "fabrica": 12,
    "construtora": 16, "construcoes": 16, "construcao": 14,
    "incorporadora": 18, "incorporacoes": 18, "empreiteira": 14,
    "engenharia": 10, "reformas": 10, "empreendimentos imobiliarios": 18,
    "imobiliaria": 12, "loteadora": 14,
    # servicos de alto ticket
    "advocacia": 12, "advogados associados": 12, "contabilidade": 10,
    "consultoria": 8, "tecnologia": 8, "software": 8, "saas": 10,
    "startup": 6, "logistica": 10, "transportadora": 12,
    "distribuidora": 12, "atacado": 12, "importadora": 12,
    "exportadora": 14, "comercio exterior": 12,
    "holding": 20, "participacoes": 18, "empreendimentos": 14,
    "grupo": 10, "concessionaria": 14, "revenda": 8,
    "energia solar": 12, "energia": 10, "franquia": 10,
    "e-commerce": 8, "ecommerce": 8, "marketing": 6, "agencia": 6,
    "ltda": 4, "me ": 2, "eireli": 4, "s.a": 8, "s/a": 8,
}

# ---------------------------------------------------------------------------
# 4. CORTES - onde cada faixa comeca
# ---------------------------------------------------------------------------
CORTE_PRIORIDADE_A = 45   # falar essa semana
CORTE_PRIORIDADE_B = 25   # falar neste mes
# abaixo disso: baixa prioridade (nutrir com conteudo, sem abordagem 1:1)

# Quantas conexoes trabalhar por semana (o gerador de briefing respeita isso)
META_SEMANAL = 15
