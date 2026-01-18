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
                        bloco_atual = map_str_to_int.get(f"L_{l}_{r}_{b}_{p}")
                        bloco_prox = map_str_to_int.get(f"L_{l}_{r}_{b+1}_{p+1}")
                        if bloco_atual:
                            if bloco_prox: 
                                clausulas_continuidade.append([-bloco_atual, bloco_prox])
                            else: 
                                clausulas_continuidade.append([-bloco_atual])
        
        for c in range(1, len(regras_colunas) + 1):
            for r, tam in enumerate(regras_colunas[c], 1):
                for b in range(1, tam):
                    for p in range(1, len(regras_linhas) + 1):
                        bloco_atual = map_str_to_int.get(f"C_{c}_{r}_{b}_{p}")
                        bloco_prox = map_str_to_int.get(f"C_{c}_{r}_{b+1}_{p+1}")
                        if bloco_atual:
                            if bloco_prox: 
                                clausulas_continuidade.append([-bloco_atual, bloco_prox])
                            else: 
                                clausulas_continuidade.append([-bloco_atual])

        self.clausulas_continuidade = clausulas_continuidade

    def regra_ordem_e_espacamento(self):
        map_str_to_int = self.map_str_to_int
        regras_colunas = self.regras_colunas
        regras_linhas = self.regras_linhas
        quant_colunas = self.quant_colunas
        quant_linhas = self.quant_linhas
        clausulas_ordem = []
        
        for l in range(1, quant_linhas + 1):
            num_blocos = len(regras_linhas[l])
            for r in range(1, num_blocos):
                tam_atual = regras_linhas[l][r-1]
                for pos_1 in range(1, quant_colunas + 1):
                    bloco_atual = map_str_to_int.get(f"L_{l}_{r}_{tam_atual }_{pos_1}")
                    for pos_2 in range(1, quant_colunas + 1):
                        if pos_2 <= pos_1 + 1:
                            bloco_prox = map_str_to_int.get(f"L_{l}_{r+1}_1_{pos_2}")
                            if bloco_atual and bloco_prox: 
                                clausulas_ordem.append([-bloco_atual, -bloco_prox])
        
        for c in range(1, quant_colunas + 1):
            num_blocos = len(regras_colunas[c])
            for r in range(1, num_blocos):
                tam_atual = regras_colunas[c][r-1]
                for pos_1 in range(1, quant_linhas + 1):
                    bloco_atual = map_str_to_int.get(f"C_{c}_{r}_{tam_atual}_{pos_1}")
                    for pos_2 in range(1, quant_linhas + 1):
                        if pos_2 <= pos_1 + 1:
                            bloco_prox = map_str_to_int.get(f"C_{c}_{r+1}_1_{pos_2}")
                            if bloco_atual and bloco_prox: 
                                clausulas_ordem.append([-bloco_atual, -bloco_prox])

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
                for prop_int in prop_linhas + prop_colunas:
                    clausulas_interconectividade.append([-prop_int, grid_int])
                clausulas_interconectividade.append([-grid_int] + prop_linhas)
                clausulas_interconectividade.append([-grid_int] + prop_colunas)
                
        self.clausulas_interconectividade = clausulas_interconectividade

def main():
    if len(sys.argv) < 2:
        print("Digite o nome do Nanogram no terminal para imprimir a imagem.")
        return
    
    nome = sys.argv[1]
    
    if nome not in SETTINGS:
        print(f"O nanogram {nome} não existe.")
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
        print("O nanogram não possui solução.")
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

if __name__ == "__main__":
    main()