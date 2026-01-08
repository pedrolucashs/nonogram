from pysat.solvers import Glucose3
from SETTINGS import SETTINGS
from itertools import combinations

#Não é uma regra de resolução do Nanogram, é uma função que gera as regras das linhas, colunas e o grid
def gerar_proposicoes(SETTINGS):
    regras_colunas = SETTINGS["example"]["rules"]["columns"]
    regras_linhas = SETTINGS["example"]["rules"]["rows"]
    quant_colunas = SETTINGS["example"]["size"]["column"]
    quant_linhas = SETTINGS["example"]["size"]["row"]
    quant_regras_linhas = {linha: len(regras) for linha, regras in regras_linhas.items()}
    quant_regras_colunas = {coluna: len(regras) for coluna, regras in regras_colunas.items()}
    prop_linhas = []
    prop_colunas = []
    prop_grid = []

    #Proposições das regras das colunas
    for c in range(1, quant_colunas + 1):
        for r in range(1, quant_regras_colunas[c]+1):
            tam_bloco = regras_colunas[c][r-1]
            for b in range(1, tam_bloco+1):
                for p in range(1, quant_colunas + 1):
                    prop_colunas.append(f"C_{c}_{r}_{b}_{p}")

    #Proposições das regras das linhas
    for l in range(1, quant_linhas + 1):
        for r in range(1, quant_regras_linhas[l]+1):
            tam_bloco = regras_linhas[l][r-1]
            for b in range(1, tam_bloco+1):
                for p in range(1, quant_linhas + 1):
                    prop_linhas.append(f"L_{l}_{r}_{b}_{p}")
    
    #Proposições do Grid
    for l in range(1, quant_linhas+1):
        for c in range(1, quant_colunas+1):
            prop_grid.append(f"G_{l}_{c}")

    return prop_linhas, prop_colunas, prop_grid


proposicoes_linhas, proposicoes_colunas, proposicoes_grid = gerar_proposicoes(SETTINGS)

"""
#Teste
print("Proposições linhas: ", proposicoes_linhas)
print("Proposições colunas: ", proposicoes_colunas)
print("Proposições grid: ", proposicoes_grid)
"""

def create_mapping(proposicoes_linhas, proposicoes_colunas, proposicoes_grid):
    mapping_to_str = {}
    mapping_to_int = {}
    cont = 1
   
    for p in proposicoes_grid:
        mapping_to_str[p] = cont
        mapping_to_int[cont] = p
        cont += 1
    for p in proposicoes_colunas:
        mapping_to_str[p] = cont
        mapping_to_int[cont] = p
        cont += 1
    for p in proposicoes_linhas:
        mapping_to_str[p] = cont
        mapping_to_int[cont] = p
        cont += 1
    return mapping_to_str, mapping_to_int

map_str_to_int, map_int_to_str = create_mapping(proposicoes_linhas, proposicoes_colunas, proposicoes_grid)

def regra_unicidade(map_str_to_int):
    prop_colunas = {}
    prop_colunas_str = {}
    prop_linhas = {}
    prop_linhas_str = {}
    clausulas = []

    for prop_str, prop_int in map_str_to_int.items():
        if prop_str.startswith("C_"):
            coluna, c, r, b, pos = prop_str.split("_")
            chave = (int(c), int(r), int(b))
            if chave not in prop_colunas:
                prop_colunas[chave] = []
                prop_colunas_str[chave] = []
            prop_colunas[chave].append(prop_int)
            prop_colunas_str[chave].append(prop_str)
        elif prop_str.startswith("L_"):
            linha, l, r, b, pos = prop_str.split("_")
            chave = (int(l), int(r), int(b))
            if chave not in prop_linhas:
                prop_linhas[chave] = []
                prop_linhas_str[chave] = []
            prop_linhas[chave].append(prop_int)
            prop_linhas_str[chave].append(prop_str)
    for lista_posicoes in prop_colunas.values():
        for c1, c2 in combinations(lista_posicoes, 2):
            clausulas.append([-c1, -c2])
    for lista_posicoes in prop_linhas.values():
        for c1, c2 in combinations(lista_posicoes, 2):
            clausulas.append([-c1, -c2])
    return clausulas, prop_colunas, prop_linhas, prop_colunas_str, prop_linhas_str

clausulas, prop_colunas, prop_linhas, p_col_str, p_lin_str  = regra_unicidade(map_str_to_int)

#Adiciona as cláusulas no solver, quando for adicionar as demais cláusulas das outras regras, uso a variável 's'
s = Glucose3()
for c in clausulas:
    s.add_clause(c)

""""
#Teste
for m, i in map_str_to_int.items():
    print(f"Mapping str {m} to int {i}")
print("")
print("Regras por bloco das colunas: ", prop_colunas)
print("")
print("Regras por blocos dad linhas: ", prop_linhas)
print("")
print("Claúsulas: ", clausulas)
print("")
print("Regras str do bloco da coluna: ", p_col_str)
print("")
print("Regras str do bloco da linha: ", p_lin_str)
"""


