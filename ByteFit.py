"""
╔══════════════════════════════════════════════════════════════╗
║                    🏋️  ByteFIT System  🏋️                    ║
║              Sistema de Gestão para Academia                  ║
╚══════════════════════════════════════════════════════════════╝
"""
 
import os
import json
import datetime
 
# ─────────────────────────────────────────────────────────────
# DADOS DO SISTEMA (em memória — substitua por banco de dados)
# ─────────────────────────────────────────────────────────────
 
PLANOS = {
    "1": {"nome": "Basic",    "valor": 89.90,  "descricao": "Acesso à musculação"},
    "2": {"nome": "Plus",     "valor": 129.90, "descricao": "Musculação + Aulas coletivas"},
    "3": {"nome": "Premium",  "valor": 189.90, "descricao": "Acesso completo + Personal"},
}
 
ADICIONAIS = {
    "1": {"nome": "Aula de Spinning",    "valor": 30.00},
    "2": {"nome": "Aula de Yoga",        "valor": 25.00},
    "3": {"nome": "Avaliação Física",    "valor": 50.00},
    "4": {"nome": "Armário Mensal",      "valor": 20.00},
    "5": {"nome": "Shake Pós-Treino",    "valor": 15.00},
}
 
EXERCICIOS_POR_GRUPO = {
    "Peito":    ["Supino Reto", "Supino Inclinado", "Crucifixo", "Flexão"],
    "Costas":   ["Puxada Frontal", "Remada Curvada", "Remada Unilateral", "Pulldown"],
    "Pernas":   ["Agachamento", "Leg Press", "Cadeira Extensora", "Mesa Flexora", "Panturrilha"],
    "Ombro":    ["Desenvolvimento", "Elevação Lateral", "Elevação Frontal", "Remada Alta"],
    "Bíceps":   ["Rosca Direta", "Rosca Alternada", "Rosca Concentrada"],
    "Tríceps":  ["Tríceps Pulley", "Tríceps Testa", "Mergulho no Banco"],
    "Abdômen":  ["Abdominal Supra", "Plank", "Bicicleta", "Abdominal Oblíquo"],
    "Cardio":   ["Esteira 20min", "Bike 20min", "Elíptico 20min", "Corda 10min"],
}
 
DIVISOES_TREINO = {
    2: ["Peito+Tríceps+Ombro", "Costas+Bíceps+Pernas"],
    3: ["Peito+Tríceps",       "Costas+Bíceps",        "Pernas+Ombro"],
    4: ["Peito+Ombro",         "Costas+Bíceps",        "Pernas",          "Tríceps+Abdômen"],
    5: ["Peito",               "Costas",                "Pernas",          "Ombro",     "Bíceps+Tríceps"],
    6: ["Peito",               "Costas",                "Pernas",          "Ombro",     "Bíceps", "Tríceps+Abdômen"],
}
 
cadastros = []   # lista de clientes cadastrados
 
# ─────────────────────────────────────────────────────────────
# UTILITÁRIOS
# ─────────────────────────────────────────────────────────────
 
def limpar():
    os.system("cls" if os.name == "nt" else "clear")
 
def linha(char="─", n=62):
    print(char * n)
 
def titulo(texto):
    limpar()
    linha("═")
    print(f"  🏋️  ByteFIT  │  {texto}")
    linha("═")
    print()
 
def pausar():
    print()
    input("  Pressione ENTER para continuar...")
 
def validar_telefone(tel):
    digits = "".join(filter(str.isdigit, tel))
    return len(digits) >= 10
 
def calcular_imc(peso, altura):
    return peso / (altura ** 2)
 
def classificar_imc(imc):
    if imc < 18.5:   return "Abaixo do peso"
    elif imc < 25:   return "Peso normal ✅"
    elif imc < 30:   return "Sobrepeso"
    elif imc < 35:   return "Obesidade Grau I"
    elif imc < 40:   return "Obesidade Grau II"
    else:            return "Obesidade Grau III"
 
def calcular_calorias(peso, altura_cm, idade, sexo, nivel):
    """Harris-Benedict + fator atividade"""
    if sexo == "M":
        tmb = 88.36 + (13.4 * peso) + (4.8 * altura_cm) - (5.7 * idade)
    else:
        tmb = 447.6 + (9.25 * peso) + (3.1 * altura_cm) - (4.33 * idade)
    fatores = [1.2, 1.375, 1.55, 1.725, 1.9]
    return round(tmb * fatores[nivel - 1])
 
# ─────────────────────────────────────────────────────────────
# MÓDULO: PRÉ-CADASTRO
# ─────────────────────────────────────────────────────────────
 
def pre_cadastro():
    titulo("Pré-Cadastro")
    print("  Preencha os dados iniciais para começar.\n")
 
    nome = input("  Nome completo: ").strip()
    if not nome:
        print("\n  ❌ Nome não pode ser vazio.")
        pausar(); return None
 
    while True:
        telefone = input("  Telefone (com DDD): ").strip()
        if validar_telefone(telefone):
            break
        print("  ❌ Telefone inválido. Mínimo 10 dígitos.")
 
    cliente = {"nome": nome, "telefone": telefone}
    print(f"\n  ✅ Pré-cadastro salvo para {nome}!")
    pausar()
    return cliente
 
# ─────────────────────────────────────────────────────────────
# MÓDULO: EXIBIR PLANOS
# ─────────────────────────────────────────────────────────────
 
def exibir_planos():
    titulo("Planos Disponíveis")
    print(f"  {'ID':<4} {'Plano':<12} {'Valor/mês':<14} Descrição")
    linha()
    for k, p in PLANOS.items():
        print(f"  [{k}]  {p['nome']:<12} R$ {p['valor']:<11.2f} {p['descricao']}")
    linha()
 
def selecionar_plano(cliente):
    exibir_planos()
    print()
    escolha = input("  Escolha o número do plano: ").strip()
    if escolha not in PLANOS:
        print("  ❌ Plano inválido.")
        pausar(); return
 
    plano = PLANOS[escolha]
    cliente["plano"] = plano.copy()
    cliente["adicionais"] = []
    total = plano["valor"]
 
    # Adicionais
    print(f"\n  ✅ Plano {plano['nome']} selecionado (R$ {plano['valor']:.2f}/mês)")
    print("\n  ── Adicionais disponíveis ──")
    print(f"  {'ID':<4} {'Adicional':<26} Valor")
    linha("-", 50)
    for k, a in ADICIONAIS.items():
        print(f"  [{k}]  {a['nome']:<26} R$ {a['valor']:.2f}/mês")
    linha("-", 50)
    print("  [0]  Nenhum adicional")
 
    print("\n  Digite os IDs dos adicionais desejados separados por vírgula")
    print("  Exemplo: 1,3  ou  0 para nenhum")
    adic_input = input("  Adicionais: ").strip()
 
    if adic_input != "0":
        ids = [x.strip() for x in adic_input.split(",")]
        for aid in ids:
            if aid in ADICIONAIS:
                cliente["adicionais"].append(ADICIONAIS[aid].copy())
                total += ADICIONAIS[aid]["valor"]
            else:
                print(f"  ⚠️  ID '{aid}' inválido, ignorado.")
 
    cliente["total_mensal"] = total
    print(f"\n  💰 Total mensal: R$ {total:.2f}")
    pausar()
 
# ─────────────────────────────────────────────────────────────
# MÓDULO: CADASTRO COMPLETO
# ─────────────────────────────────────────────────────────────
 
def cadastro_completo(cliente):
    titulo("Cadastro Completo")
 
    if "plano" not in cliente:
        print("  ⚠️  Selecione um plano antes do cadastro completo.")
        pausar(); return
 
    print("  Dados de endereço\n")
    cliente["rua"]        = input("  Rua e número: ").strip()
    cliente["bairro"]     = input("  Bairro: ").strip()
    cliente["cidade"]     = input("  Cidade: ").strip()
    cliente["cep"]        = input("  CEP: ").strip()
 
    print("\n  Face ID")
    print("  (Em produção: integrar com câmera/SDK de reconhecimento facial)")
    face_sim = input("  Simular captura de Face ID? (s/n): ").strip().lower()
    cliente["face_id"] = "✅ Capturado" if face_sim == "s" else "⏳ Pendente"
 
    cliente["data_cadastro"] = datetime.date.today().isoformat()
    cliente["status"] = "Ativo"
 
    cadastros.append(cliente)
 
    print("\n  ════════════════════════════════════════")
    print("  ✅  CADASTRO REALIZADO COM SUCESSO!")
    print("  ════════════════════════════════════════")
    print(f"  Nome:       {cliente['nome']}")
    print(f"  Telefone:   {cliente['telefone']}")
    print(f"  Endereço:   {cliente['rua']}, {cliente['bairro']}")
    print(f"  Cidade:     {cliente['cidade']}  CEP: {cliente['cep']}")
    print(f"  Plano:      {cliente['plano']['nome']}  R$ {cliente['plano']['valor']:.2f}/mês")
    if cliente["adicionais"]:
        for a in cliente["adicionais"]:
            print(f"  Adicional:  {a['nome']}  R$ {a['valor']:.2f}/mês")
    print(f"  Total:      R$ {cliente['total_mensal']:.2f}/mês")
    print(f"  Face ID:    {cliente['face_id']}")
    print(f"  Desde:      {cliente['data_cadastro']}")
    pausar()
 
# ─────────────────────────────────────────────────────────────
# MÓDULO: TREINO
# ─────────────────────────────────────────────────────────────
 
def gerar_treino(grupos_dia, dias_semana):
    """Retorna lista de dicionários {dia, grupo, exercicios}"""
    dias_nomes = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]
    treino = []
    for i, grupo_str in enumerate(grupos_dia):
        grupos = [g.strip() for g in grupo_str.split("+")]
        exercicios = []
        for g in grupos:
            if g in EXERCICIOS_POR_GRUPO:
                exercicios.extend([(g, ex) for ex in EXERCICIOS_POR_GRUPO[g]])
        treino.append({
            "dia": dias_nomes[i % 7],
            "grupo": grupo_str,
            "exercicios": exercicios,
        })
    return treino
 
def gerar_texto_treino(dados):
    """Gera o conteúdo da ficha de treino como string para salvar em arquivo."""
    sep  = "-" * 62
    sep2 = "=" * 62
    nome     = dados.get("nome", "Aluno")
    peso     = dados.get("peso_atual")
    meta     = dados.get("meta_peso")
    imc      = dados.get("imc")
    clas     = dados.get("classificacao_imc")
    calorias = dados.get("calorias_dia")
    treino   = dados.get("treino", [])
    dias     = dados.get("dias_semana")

    linhas = []
    linhas.append("")
    linhas.append(sep2)
    linhas.append("  ByteFIT  -  FICHA DE TREINO PERSONALIZADA")
    linhas.append(sep2)
    linhas.append(f"  Aluno:     {nome}")
    linhas.append(f"  Data:      {datetime.date.today().strftime('%d/%m/%Y')}")
    linhas.append(f"  Objetivo:  {'Emagrecimento' if meta < peso else 'Ganho de massa'}")
    linhas.append(sep)
    linhas.append(f"  Peso atual:   {peso:.1f} kg    |   Meta: {meta:.1f} kg")
    diff = abs(peso - meta)
    direcao = "perder" if meta < peso else "ganhar"
    linhas.append(f"  Diferenca:    {diff:.1f} kg a {direcao}")
    linhas.append(f"  IMC:          {imc:.1f}  -  {clas}")
    linhas.append(f"  Calorias/dia: ~{calorias} kcal")
    linhas.append(sep)
    linhas.append(f"  Frequencia:   {dias}x por semana")
    linhas.append(sep)

    for bloco in treino:
        linhas.append(f"\n  {bloco['dia'].upper()}  -  {bloco['grupo']}")
        linhas.append("-" * 62)
        linhas.append(f"  {'Grupo':<14} {'Exercicio':<30} {'Series':<8} {'Reps'}")
        linhas.append("-" * 62)
        for (grupo, ex) in bloco["exercicios"]:
            series = "4x" if "Cardio" not in grupo else "1x"
            reps   = "20min" if "Cardio" in grupo else "12"
            linhas.append(f"  {grupo:<14} {ex:<30} {series:<8} {reps}")

    linhas.append(sep2)
    linhas.append("  Treino gerado pelo ByteFIT  |  Bons resultados!")
    linhas.append(sep2)
    linhas.append("")
    return "\n".join(linhas)


def imprimir_treino(dados):
    """Imprime o treino formatado como 'print do treino feito em Python'"""
    nome   = dados.get("nome", "Aluno")
    peso   = dados.get("peso_atual")
    meta   = dados.get("meta_peso")
    imc    = dados.get("imc")
    clas   = dados.get("classificacao_imc")
    calorias = dados.get("calorias_dia")
    treino = dados.get("treino", [])
    dias   = dados.get("dias_semana")
 
    print()
    linha("═")
    print("  🏋️  ByteFIT  ─  FICHA DE TREINO PERSONALIZADA")
    linha("═")
    print(f"  Aluno:     {nome}")
    print(f"  Data:      {datetime.date.today().strftime('%d/%m/%Y')}")
    print(f"  Objetivo:  {'Emagrecimento' if meta < peso else 'Ganho de massa'}")
    linha()
    print(f"  Peso atual:   {peso:.1f} kg    │   Meta: {meta:.1f} kg")
    diff = abs(peso - meta)
    direcao = "perder" if meta < peso else "ganhar"
    print(f"  Diferença:    {diff:.1f} kg a {direcao}")
    print(f"  IMC:          {imc:.1f}  —  {clas}")
    print(f"  Calorias/dia: ~{calorias} kcal")
    linha()
    print(f"  Frequência:   {dias}x por semana")
    linha()
 
    for bloco in treino:
        print(f"\n  📅  {bloco['dia'].upper()}  —  {bloco['grupo']}")
        linha("-", 62)
        print(f"  {'Grupo':<14} {'Exercício':<30} {'Séries':<8} {'Reps'}")
        linha("-", 62)
        for (grupo, ex) in bloco["exercicios"]:
            series = "4x" if "Cardio" not in grupo else "1x"
            reps   = "20min" if "Cardio" in grupo else "12"
            print(f"  {grupo:<14} {ex:<30} {series:<8} {reps}")
 
    linha("═")
    print("  ✅ Treino gerado pelo ByteFIT  |  Bons resultados! 💪")
    linha("═")
    print()
 
def modulo_treino():
    titulo("Módulo de Treino")
 
    nome = input("  Seu nome: ").strip() or "Aluno"
 
    # Peso e meta
    print()
    while True:
        try:
            peso_atual = float(input("  Peso atual (kg): ").replace(",", "."))
            break
        except ValueError:
            print("  ❌ Digite um número válido.")
 
    while True:
        try:
            meta_peso = float(input("  Meta de peso (kg): ").replace(",", "."))
            break
        except ValueError:
            print("  ❌ Digite um número válido.")
 
    while True:
        try:
            altura = float(input("  Altura (ex: 1.75): ").replace(",", "."))
            if 1.0 < altura < 2.5:
                break
            print("  ❌ Altura deve estar entre 1.0 e 2.5 m.")
        except ValueError:
            print("  ❌ Digite um número válido.")
 
    while True:
        try:
            idade = int(input("  Idade: "))
            break
        except ValueError:
            print("  ❌ Digite um número inteiro.")
 
    sexo = ""
    while sexo not in ("M", "F"):
        sexo = input("  Sexo (M/F): ").strip().upper()
 
    # Nível de atividade
    print("\n  Nível de atividade atual:")
    print("  [1] Sedentário")
    print("  [2] Levemente ativo (1-3 dias/semana)")
    print("  [3] Moderadamente ativo (3-5 dias/semana)")
    print("  [4] Muito ativo (6-7 dias/semana)")
    print("  [5] Extremamente ativo")
    while True:
        try:
            nivel = int(input("  Escolha (1-5): "))
            if 1 <= nivel <= 5:
                break
        except ValueError:
            pass
        print("  ❌ Opção inválida.")
 
    # Dias disponíveis
    print("\n  Quantos dias por semana você pode treinar? (2 a 6)")
    while True:
        try:
            dias = int(input("  Dias: "))
            if 2 <= dias <= 6:
                break
            print("  ❌ Entre 2 e 6 dias.")
        except ValueError:
            print("  ❌ Digite um número inteiro.")
 
    # Calcular métricas
    imc       = calcular_imc(peso_atual, altura)
    classif   = classificar_imc(imc)
    calorias  = calcular_calorias(peso_atual, altura * 100, idade, sexo, nivel)
 
    # Ajuste calórico por objetivo
    if meta_peso < peso_atual:
        calorias_meta = calorias - 400
        obs = "déficit calórico para emagrecimento"
    elif meta_peso > peso_atual:
        calorias_meta = calorias + 300
        obs = "superávit calórico para ganho de massa"
    else:
        calorias_meta = calorias
        obs = "manutenção de peso"
 
    # Divisão de treino
    grupos_dia = DIVISOES_TREINO.get(dias, DIVISOES_TREINO[4])
    treino = gerar_treino(grupos_dia, dias)
 
    dados_treino = {
        "nome":             nome,
        "peso_atual":       peso_atual,
        "meta_peso":        meta_peso,
        "imc":              imc,
        "classificacao_imc": classif,
        "calorias_dia":     calorias_meta,
        "obs_calorias":     obs,
        "dias_semana":      dias,
        "treino":           treino,
    }
 
    imprimir_treino(dados_treino)
 
    # Salvar em arquivo
    salvar = input("  Deseja salvar a ficha em arquivo .txt? (s/n): ").strip().lower()
    if salvar == "s":
        nome_arq = f"ficha_treino_{nome.replace(' ', '_')}_{datetime.date.today()}.txt"
        conteudo = gerar_texto_treino(dados_treino)
        with open(nome_arq, "w", encoding="utf-8") as f:
            f.write(conteudo)
        print(f"\n  ✅ Ficha salva em: {nome_arq}")
 
    pausar()
 
# ─────────────────────────────────────────────────────────────
# MÓDULO: LISTAR CADASTROS
# ─────────────────────────────────────────────────────────────
 
def listar_cadastros():
    titulo("Clientes Cadastrados")
    if not cadastros:
        print("  Nenhum cliente cadastrado nesta sessão.")
        pausar(); return
 
    for i, c in enumerate(cadastros, 1):
        linha()
        print(f"  [{i}] {c['nome']}  │  {c['telefone']}")
        print(f"      Plano: {c.get('plano', {}).get('nome', '—')}  │  "
              f"Total: R$ {c.get('total_mensal', 0):.2f}/mês")
        print(f"      Status: {c.get('status', '—')}  │  "
              f"Face ID: {c.get('face_id', '—')}")
    linha()
    pausar()
 
# ─────────────────────────────────────────────────────────────
# MENU PAINEL
# ─────────────────────────────────────────────────────────────
 
def menu_painel():
    cliente_temp = None
 
    while True:
        titulo("Painel  —  Cadastro de Clientes")
        print("  [1]  Pré-Cadastro (nome e telefone)")
        print("  [2]  Ver Planos Disponíveis")
        print("  [3]  Selecionar Plano e Adicionais")
        print("  [4]  Cadastro Completo")
        print("  [5]  Listar Clientes")
        print("  [0]  Voltar ao Menu Principal")
        print()
        op = input("  Escolha: ").strip()
 
        if op == "1":
            cliente_temp = pre_cadastro()
        elif op == "2":
            exibir_planos()
            pausar()
        elif op == "3":
            if not cliente_temp:
                print("\n  ⚠️  Faça o pré-cadastro primeiro (opção 1).")
                pausar()
            else:
                selecionar_plano(cliente_temp)
        elif op == "4":
            if not cliente_temp:
                print("\n  ⚠️  Faça o pré-cadastro primeiro (opção 1).")
                pausar()
            else:
                cadastro_completo(cliente_temp)
                cliente_temp = None
        elif op == "5":
            listar_cadastros()
        elif op == "0":
            break
        else:
            print("  ❌ Opção inválida.")
            pausar()
 
# ─────────────────────────────────────────────────────────────
# MENU PRINCIPAL
# ─────────────────────────────────────────────────────────────
 
def menu_principal():
    while True:
        limpar()
        linha("═")
        print("  ██████╗ ██╗   ██╗████████╗███████╗███████╗██╗████████╗")
        print("  ██╔══██╗╚██╗ ██╔╝╚══██╔══╝██╔════╝██╔════╝██║╚══██╔══╝")
        print("  ██████╔╝ ╚████╔╝    ██║   █████╗  █████╗  ██║   ██║   ")
        print("  ██╔══██╗  ╚██╔╝     ██║   ██╔══╝  ██╔══╝  ██║   ██║   ")
        print("  ██████╔╝   ██║      ██║   ███████╗██║     ██║   ██║   ")
        print("  ╚═════╝    ╚═╝      ╚═╝   ╚══════╝╚═╝     ╚═╝   ╚═╝   ")
        linha("═")
        print("         Sistema de Gestão para Academia  💪")
        linha("═")
        print()
        print("  [1]  📋  Painel  (Cadastros e Planos)")
        print("  [2]  🏋️   Treino  (Ficha Personalizada)")
        print("  [0]  🚪  Sair")
        print()
        linha()
        op = input("  Escolha uma opção: ").strip()
 
        if op == "1":
            menu_painel()
        elif op == "2":
            modulo_treino()
        elif op == "0":
            limpar()
            print("\n  👋  Até logo! ByteFIT — Seu progresso, nossa missão.\n")
            break
        else:
            print("  ❌ Opção inválida.")
            pausar()
 
# ─────────────────────────────────────────────────────────────
# ENTRY POINT
# ─────────────────────────────────────────────────────────────
 
if __name__ == "__main__":
    menu_principal()