from pysat.solvers import Glucose3
from SETTINGS import SETTINGS

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


#Teste
proposicoes_linhas, proposicoes_colunas, proposicoes_grid = gerar_proposicoes(SETTINGS)
print("Proposições linhas: ", proposicoes_linhas)
print("Proposições colunas: ", proposicoes_colunas)
print("Proposições grid: ", proposicoes_grid)


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
    print(mapping_to_str, mapping_to_int)

# teste
create_mapping(proposicoes_linhas, proposicoes_colunas, proposicoes_grid)
