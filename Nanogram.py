import sys
from pysat.solvers import Glucose3
from SETTINGS import SETTINGS
from itertools import combinations

class Nanogram:
    def __init__(self, name):
        aux = SETTINGS[name]
        self.name = aux
        self.quant_linhas = aux["size"]["row"]
        self.quant_colunas = aux["size"]["column"]
        self.regras_linhas = aux["rules"]["rows"]
        self.regras_colunas = aux["rules"]["columns"]
        
    def gerar_proposicoes(self):
        regras_colunas = self.regras_colunas
        regras_linhas = self.regras_linhas
        quant_colunas = self.quant_colunas
        quant_linhas = self.quant_linhas
        
        prop_linhas = []
        prop_colunas = []
        prop_grid = []

        for c in range(1, quant_colunas + 1):
            for r, tam_bloco in enumerate(regras_colunas[c], 1):
                for b in range(1, tam_bloco + 1):
                    for p in range(1, quant_linhas + 1):
                        prop_colunas.append(f"C_{c}_{r}_{b}_{p}")

        for l in range(1, quant_linhas + 1):
            for r, tam_bloco in enumerate(regras_linhas[l], 1):
                for b in range(1, tam_bloco + 1):
                    for p in range(1, quant_colunas + 1):
                        prop_linhas.append(f"L_{l}_{r}_{b}_{p}")
        
        for l in range(1, quant_linhas + 1):
            for c in range(1, quant_colunas + 1):
                prop_grid.append(f"G_{l}_{c}")

        self.prop_linhas = prop_linhas
        self.prop_colunas = prop_colunas
        self.prop_grid = prop_grid


    def create_mapping(self):
        prop_linhas = self.prop_linhas
        prop_colunas = self.prop_colunas
        prop_grid = self.prop_grid
        mapping_to_str = {}
        mapping_to_int = {}
        cont = 1
        
        for p in prop_grid:
            mapping_to_str[p] = cont
            mapping_to_int[cont] = p
            cont += 1
        for p in prop_colunas:
            mapping_to_str[p] = cont
            mapping_to_int[cont] = p
            cont += 1
        for p in prop_linhas:
            mapping_to_str[p] = cont
            mapping_to_int[cont] = p
            cont += 1

        self.map_str_to_int = mapping_to_str
        self.map_int_to_str = mapping_to_int

    def regra_unicidade(self):
        map_str_to_int = self.map_str_to_int
        clausulas_unicidade = []
        grupos = {}

        for prop_str, prop_int in map_str_to_int.items():
            if prop_str.startswith(("C_")):
                C, c, r, b, p = prop_str.split("_")
                chave = (str(C), int(c), int(r), int(b))
                if chave not in grupos: 
                    grupos[chave] = []
                grupos[chave].append(prop_int)
            if prop_str.startswith(("L_")):
                L, l, r, b, p = prop_str.split("_")
                chave = (str(L), int(l), int(r), int(b))
                if chave not in grupos: 
                    grupos[chave] = []
                grupos[chave].append(prop_int)

        for lista in grupos.values():
            clausulas_unicidade.append(lista) 
            for c1, c2 in combinations(lista, 2):
                clausulas_unicidade.append([-c1, -c2]) 
        self.clausulas_unicidade = clausulas_unicidade

    def regra_continuidade(self):
        map_str_to_int = self.map_str_to_int
        regras_colunas = self.regras_colunas
        regras_linhas = self.regras_linhas
        clausulas_continuidade = []

        for l in range(1, len(regras_linhas) + 1):
            for r, tam in enumerate(regras_linhas[l], 1):
                for b in range(1, tam):
                    for p in range(1, len(regras_colunas) + 1):
                        x = map_str_to_int.get(f"L_{l}_{r}_{b}_{p}")
                        y = map_str_to_int.get(f"L_{l}_{r}_{b+1}_{p+1}")
                        if x:
                            if y: 
                                clausulas_continuidade.append([-x, y])
                            else: 
                                clausulas_continuidade.append([-x])
        
        for c in range(1, len(regras_colunas) + 1):
            for r, tam in enumerate(regras_colunas[c], 1):
                for b in range(1, tam):
                    for p in range(1, len(regras_linhas) + 1):
                        x = map_str_to_int.get(f"C_{c}_{r}_{b}_{p}")
                        y = map_str_to_int.get(f"C_{c}_{r}_{b+1}_{p+1}")
                        if x:
                            if y: 
                                clausulas_continuidade.append([-x, y])
                            else: 
                                clausulas_continuidade.append([-x])

        self.clausulas_continuidade = clausulas_continuidade

    def regra_ordem_e_espacamento(self):
        map_str_to_int = self.map_str_to_int
        regras_colunas = self.regras_colunas
        regras_linhas = self.regras_linhas
        quant_colunas = self.quant_colunas
        quant_linhas = self.quant_linhas
        clausulas_ordem = []
        
        for l in range(1, quant_linhas + 1):
            for r in range(1, len(regras_linhas[l])):
                tam = regras_linhas[l][r-1]
                for pos_1 in range(1, quant_colunas + 1):
                    x = map_str_to_int.get(f"L_{l}_{r}_{tam}_{pos_1}")
                    for pos_2 in range(1, quant_colunas + 1):
                        if pos_2 <= pos_1 + 1:
                            y = map_str_to_int.get(f"L_{l}_{r+1}_1_{pos_2}")
                            if x and y: 
                                clausulas_ordem.append([-x, -y])
        
        for c in range(1, quant_colunas + 1):
            for r in range(1, len(regras_colunas[c])):
                tam = regras_colunas[c][r-1]
                for pos_1 in range(1, quant_linhas + 1):
                    x = map_str_to_int.get(f"C_{c}_{r}_{tam}_{pos_1}")
                    for pos_2 in range(1, quant_linhas + 1):
                        if pos_2 <= pos_1 + 1:
                            y = map_str_to_int.get(f"C_{c}_{r+1}_1_{pos_2}")
                            if x and y: 
                                clausulas_ordem.append([-x, -y])

        self.clausulas_ordem = clausulas_ordem


    def regra_interconectividade(self):
        map_str_to_int = self.map_str_to_int
        regras_colunas = self.regras_colunas
        regras_linhas = self.regras_linhas
        quant_colunas = self.quant_colunas
        quant_linhas = self.quant_linhas
        clausulas_interconectividade = []
        for l in range(1, quant_linhas + 1):
            for c in range(1, quant_colunas + 1):
                grid_int = map_str_to_int[f"G_{l}_{c}"]
                prop_linhas = []
                for r, tam in enumerate(regras_linhas[l], 1):
                    for b in range(1, tam + 1):
                        prop_linhas.append(map_str_to_int[f"L_{l}_{r}_{b}_{c}"])
                prop_colunas = []
                for r, tam in enumerate(regras_colunas[c], 1):
                    for b in range(1, tam + 1):
                        prop_colunas.append(map_str_to_int[f"C_{c}_{r}_{b}_{l}"])
                for p in prop_linhas + prop_colunas:
                    clausulas_interconectividade.append([-p, grid_int])
                clausulas_interconectividade.append([-grid_int] + prop_linhas)
                clausulas_interconectividade.append([-grid_int] + prop_colunas)
                
        self.clausulas_interconectividade = clausulas_interconectividade

def main():
    if len(sys.argv) < 2:
        print("Digite: py Nanogram.py (nome do Nanogram)")
        return
    
    nome = sys.argv[1]
    
    if nome not in SETTINGS:
        print(f"O nanogram {nome} não existe")
        return

    try:
        nanogram = Nanogram(nome)
    except ValueError as e:
        print(e)
        return

    nanogram.gerar_proposicoes()
    nanogram.create_mapping()
    nanogram.regra_unicidade()
    nanogram.regra_continuidade()
    nanogram.regra_interconectividade()
    nanogram.regra_ordem_e_espacamento()

    g = Glucose3()

    for clausula in nanogram.clausulas_unicidade:
        g.add_clause(clausula)
    for clausula in nanogram.clausulas_continuidade:
        g.add_clause(clausula)
    for clausula in nanogram.clausulas_interconectividade:
        g.add_clause(clausula)
    for clausula in nanogram.clausulas_ordem:
        g.add_clause(clausula)

    if not g.solve():
        print("O nanogram não possui solução")
        return

    modelo = g.get_model()
    quadrados_pintados = []

    for prop in modelo:
        if prop > 0:
            prop_str = nanogram.map_int_to_str.get(prop)
            if prop_str and prop_str.startswith("G_"):
                g, coluna, linha = prop_str.split("_")
                quadrados_pintados.append((int(coluna), int(linha)))

    quant_linhas = nanogram.quant_linhas
    quant_colunas = nanogram.quant_colunas
    matriz_nanogram = []

    for l in range(quant_linhas):
        linha = []
        for c in range(quant_colunas):
            linha.append(False)
        matriz_nanogram.append(linha)

    for l, c in quadrados_pintados:
        if 1 <= l <= quant_linhas and 1 <= c <= quant_colunas:
            matriz_nanogram[l-1][c-1] = True

    for l in range(quant_linhas):
        for c in range(quant_colunas):
            if matriz_nanogram[l][c]:
                print("██", end="")
            else:
                print("  ", end="")
        print()

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

    for l in range(1, quant_linhas + 1):
        num_blocos = len(regras_linhas[l])
        for r in range(1, num_blocos):
            tamanho_atual = regras_linhas[l][r-1]
            for p1 in range(1, quant_colunas + 1):
                bloco_atual = f"L_{l}_{r}_{tamanho_atual}_{p1}"
                if bloco_atual in map_str_to_int:
                    id_atual = map_str_to_int[bloco_atual]
                    for p2 in range(1, quant_colunas + 1):
                        if p2 <= p1 + 1:
                            bloco_proximo = f"L_{l}_{r+1}_1_{p2}"
                            if bloco_proximo in map_str_to_int:
                                id_proximo = map_str_to_int[bloco_proximo]
                                clausulas_ordem.append([-id_atual, -id_proximo])

    for c in range(1, quant_colunas + 1):
        num_blocos = len(regras_colunas[c])
        for r in range(1, num_blocos):
            tamanho_atual = regras_colunas[c][r-1]
            for p1 in range(1, quant_linhas + 1):
                bloco_atual = f"C_{c}_{r}_{tamanho_atual}_{p1}"
                if bloco_atual in map_str_to_int:
                    id_atual = map_str_to_int[bloco_atual]
                    for p2 in range(1, quant_linhas + 1):
                        if p2 <= p1 + 1:
                            bloco_proximo = f"C_{c}_{r+1}_1_{p2}"
                            if bloco_proximo in map_str_to_int:
                                id_proximo = map_str_to_int[bloco_proximo]
                                clausulas_ordem.append([-id_atual, -id_proximo])

    return clausulas_ordem

clausulas_ordem = regra_ordem_e_espacamento(map_str_to_int, SETTINGS["example"]["size"]["row"], SETTINGS["example"]["size"]["column"], SETTINGS["example"]["rules"]["rows"], SETTINGS["example"]["rules"]["columns"])
s = Glucose3()
for c in clausulas + clausulas_ordem:
    s.add_clause(c)

#print(clausulas_ordem)

def regra_interconectividade(map_str_to_int):
    clausulas5 = []

    for prop_str, prop_int in map_str_to_int.items():
        if prop_str.startswith("C_"):
            coluna, c, r, b, pos = prop_str.split("_")
            grid = f"G_{c}_{pos}"
            if grid in map_str_to_int:
                grid_int = map_str_to_int[grid]
                clausulas5.append([-prop_int, grid_int])
        if prop_str.startswith("L_"):
            linha, l, r, b, pos = prop_str.split("_")
            grid = f"G_{l}_{pos}"
            if grid in map_str_to_int:
                grid_int = map_str_to_int[grid]
                clausulas5.append([-prop_int, grid_int])

    return clausulas5

clausulas5 = regra_interconectividade(map_str_to_int)
for c in clausulas5:
    s.add_clause(c)


def regra_interconectividade_dois(map_str_to_int):
    clausulas6 = []
    cobertura = {}

    for prop_str, prop_int in map_str_to_int.items():
        if prop_str.startswith("C_"):
            parts = prop_str.split("_")
            c, r, b, pos = parts[1], parts[2], parts[3], parts[4]
            grid_nome = f"G_{pos}_{c}"
            if grid_nome not in cobertura:
                cobertura[grid_nome] = []
            cobertura[grid_nome].append(prop_int)

        elif prop_str.startswith("L_"):
            parts = prop_str.split("_")
            l, r, b, pos = parts[1], parts[2], parts[3], parts[4]
            grid_nome = f"G_{l}_{pos}"
            if grid_nome not in cobertura:
                cobertura[grid_nome] = []
            cobertura[grid_nome].append(prop_int)

    for grid_nome, lista_blocos in cobertura.items():
        if grid_nome in map_str_to_int:
            grid_int = map_str_to_int[grid_nome]
            clausula = [-grid_int] + lista_blocos
            clausulas6.append(clausula)

    return clausulas6

clausulas6 = regra_interconectividade_dois(map_str_to_int)
for c in clausulas6:
    s.add_clause(c)

#print(clausulas6)

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
if __name__ == "__main__":
    main()
