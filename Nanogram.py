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

def regra_continuidade(map_str_to_int, SETTINGS):
    regras_colunas = SETTINGS["example"]["rules"]["columns"]
    regras_linhas = SETTINGS["example"]["rules"]["rows"]
    quant_colunas = SETTINGS["example"]["size"]["column"]
    quant_linhas = SETTINGS["example"]["size"]["row"]
    prop_colunas = {}
    prop_colunas_str = {}
    prop_linhas = {}
    prop_linhas_str = {}
    clausulas2 = []

    for prop_str, prop_int in map_str_to_int.items():
        if prop_str.startswith("C_"):
            coluna, c, r, b, pos = prop_str.split("_")
            chave = (int(c), int(r), int(b))
            if chave not in prop_colunas:
                prop_colunas[chave] = []
                prop_colunas_str[chave] = []
            prop_colunas[chave].append((int(pos), prop_int))
            prop_colunas_str[chave].append((int(pos), prop_str))
        elif prop_str.startswith("L_"):
            linha, l, r, b, pos = prop_str.split("_")
            chave = (int(l), int(r), int(b))
            if chave not in prop_linhas:
                prop_linhas[chave] = []
                prop_linhas_str[chave] = []
            prop_linhas[chave].append((int(pos), prop_int))
            prop_linhas_str[chave].append((int(pos), prop_str))

    for (c, r, b), lista_prop in prop_colunas.items():
        if b != 1:
            continue
        tam_regra = regras_colunas[c][r-1]
        if tam_regra <= 1:
            continue
        for pos, prop in lista_prop:
            if (tam_regra + pos - 1) > quant_linhas:
                clausulas2.append([-prop])
                continue
            for cont in range (1, tam_regra):
                bloco_sucessor = b + cont
                posic_sucessora = pos + cont
                chave_sucessora = (c, r, bloco_sucessor)           
                if chave_sucessora in prop_colunas:
                    for prox_pos, prox_prop in prop_colunas[chave_sucessora]:
                        if posic_sucessora == prox_pos:
                            clausulas2.append([-prop, prox_prop])
                            break

    for (l, r, b), lista_prop in prop_linhas.items():
        if b != 1:
            continue
        tam_regra = regras_linhas[l][r-1]
        if tam_regra <= 1:
            continue
        for pos, prop in lista_prop:
            if (tam_regra + pos - 1) > quant_colunas:
                clausulas2.append([-prop])
                continue
            for cont in range (1, tam_regra):
                bloco_sucessor = b + cont
                posic_sucessora = pos + cont
                chave_sucessora = (l, r, bloco_sucessor)           
                if chave_sucessora in prop_linhas:
                    for prox_pos, prox_prop in prop_linhas[chave_sucessora]:
                        if posic_sucessora == prox_pos:
                            clausulas2.append([-prop, prox_prop])
                            break

    return prop_colunas, prop_linhas, prop_colunas_str, prop_linhas_str, clausulas2

p_col, p_lin, p_c_s, p_l_s, c = regra_continuidade(map_str_to_int, SETTINGS)


def regra_ordem_e_espacamento(map_str_to_int, quant_linhas, quant_colunas, regras_linhas, regras_colunas):
    clausulas_ordem = []

    # BLOCO 1: TRATANDO AS LINHAS (Conforme o monitor explicou)
    for l in range(1, quant_linhas + 1):
        num_blocos = len(regras_linhas[l])
        # Precisamos de pelo menos 2 blocos para ter uma ordem entre eles
        for r in range(1, num_blocos):
            tam_bloco_atual = regras_linhas[l][r-1]
            
            # FOR 1: Vê onde o bloco ATUAL (r) termina
            for p1 in range(1, quant_colunas + 1):
                # Pegamos o ID do último quadradinho (b = tamanho do bloco) do bloco r
                var_fim_bloco_r = map_str_to_int.get(f"L_{l}_{r}_{tam_bloco_atual}_{p1}")
                
                if var_fim_bloco_r:
                    # FOR 2: Vê onde o PRÓXIMO bloco (r+1) começa
                    for p2 in range(1, quant_colunas + 1):
                        # Se a posição de início do próximo (p2) for menor ou igual 
                        # à posição de fim do atual (p1) + 1, gera conflito.
                        # O "+ 1" é o espaço em branco obrigatório do Nanograma.
                        if p2 <= p1 + 1:
                            # Pegamos o ID do primeiro quadradinho (b=1) do bloco r+1
                            var_ini_bloco_prox = map_str_to_int.get(f"L_{l}_{r+1}_1_{p2}")
                            
                            if var_ini_bloco_prox:
                                # Se os dois forem verdadeiros ao mesmo tempo, quebra a regra
                                clausulas_ordem.append([-var_fim_bloco_r, -var_ini_bloco_prox])

    # BLOCO 2: TRATANDO AS COLUNAS (Repete a mesma lógica do monitor)
    for c in range(1, quant_colunas + 1):
        num_blocos = len(regras_colunas[c])
        for r in range(1, num_blocos):
            tam_bloco_atual = regras_colunas[c][r-1]
            
            for p1 in range(1, quant_linhas + 1):
                var_fim_bloco_r = map_str_to_int.get(f"C_{c}_{r}_{tam_bloco_atual}_{p1}")
                
                if var_fim_bloco_r:
                    for p2 in range(1, quant_linhas + 1):
                        if p2 <= p1 + 1:
                            var_ini_bloco_prox = map_str_to_int.get(f"C_{c}_{r+1}_1_{p2}")
                            if var_ini_bloco_prox:
                                clausulas_ordem.append([-var_fim_bloco_r, -var_ini_bloco_prox])

    return clausulas_ordem

clausulas_ordem = regra_ordem_e_espacamento(map_str_to_int, SETTINGS["example"]["size"]["row"], SETTINGS["example"]["size"]["column"], SETTINGS["example"]["rules"]["rows"], SETTINGS["example"]["rules"]["columns"])
s = Glucose3()
for c in clausulas + clausulas_ordem:
    s.add_clause(c)

#print(clausulas_ordem)

def regra_quadrado_verdadeiro(p_col, p_lin):
    dict_col = {}
    dict_lin = {}
    clausulas6 = []
    
    for chave, itens in p_col.items():
        for tupla in itens:
            item2 = tupla[1]
            if not chave in dict_col:
                dict_col[chave] = []
            dict_col[chave].append(item2)
    for chave, itens in p_lin.items():
        for tupla in itens:
            item2 = tupla[1]
            if not chave in dict_lin:
                dict_lin[chave] = []
            dict_lin[chave].append(item2)
    for itens in dict_col.values():
        clausulas6.append(itens)
    for itens in dict_lin.values():
        clausulas6.append(itens)
    
    return dict_col, dict_lin, clausulas6

c, l, clau = regra_quadrado_verdadeiro(p_col, p_lin)