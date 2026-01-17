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
        quant_regras_linhas = {linha: len(regras) for linha, regras in regras_linhas.items()}
        quant_regras_colunas = {coluna: len(regras) for coluna, regras in regras_colunas.items()}
        prop_linhas = []
        prop_colunas = []
        prop_grid = []

        for c in range(1, quant_colunas + 1):
            for r in range(1, quant_regras_colunas[c]+1):
                tam_bloco = regras_colunas[c][r-1]
                for b in range(1, tam_bloco+1):
                    for p in range(1, quant_colunas + 1):
                        prop_colunas.append(f"C_{c}_{r}_{b}_{p}")

        for l in range(1, quant_linhas + 1):
            for r in range(1, quant_regras_linhas[l]+1):
                tam_bloco = regras_linhas[l][r-1]
                for b in range(1, tam_bloco+1):
                    for p in range(1, quant_linhas + 1):
                        prop_linhas.append(f"L_{l}_{r}_{b}_{p}")
        
        for l in range(1, quant_linhas+1):
            for c in range(1, quant_colunas+1):
                prop_grid.append(f"G_{l}_{c}")

        self.prop_linhas = prop_linhas
        self.prop_colunas = prop_colunas
        self.prop_grid = prop_grid

    def create_mapping(self):
        prop_grid =  self.prop_grid 
        prop_colunas = self.prop_colunas
        prop_linhas = self.prop_linhas 
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
        prop_colunas = {}
        prop_colunas_str = {}
        prop_linhas = {}
        prop_linhas_str = {}
        clausulas_unicidade = []

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
                clausulas_unicidade.append([-c1, -c2])
        for lista_posicoes in prop_linhas.values():
            for c1, c2 in combinations(lista_posicoes, 2):
                clausulas_unicidade.append([-c1, -c2])
        
        self.clausulas_unicidade = clausulas_unicidade
        self.prop_colunas = prop_colunas
        self.prop_linhas = prop_linhas
        self.prop_colunas_str = prop_colunas_str
        self.prop_linhas_str = prop_linhas_str

    def regra_continuidade(self):
        regras_colunas = self.regras_colunas
        regras_linhas = self.regras_linhas
        quant_colunas = self.quant_colunas
        quant_linhas = self.quant_linhas
        map_str_to_int = self.map_str_to_int

        prop_colunas = {}
        prop_colunas_str = {}
        prop_linhas = {}
        prop_linhas_str = {}
        clausulas_continuidade = []

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
            if b == 1:
                tam_regra = regras_colunas[c][r-1]
                if tam_regra > 1:
                    for pos, prop in lista_prop:
                        if (tam_regra + pos - 1) > quant_linhas:
                            clausulas_continuidade.append([-prop])
                            continue
                        for cont in range (1, tam_regra):
                            bloco_sucessor = b + cont
                            posic_sucessora = pos + cont
                            chave_sucessora = (c, r, bloco_sucessor)           
                            if chave_sucessora in prop_colunas:
                                for prox_pos, prox_prop in prop_colunas[chave_sucessora]:
                                    if posic_sucessora == prox_pos:
                                        clausulas_continuidade.append([-prop, prox_prop])
                                        break

        for (l, r, b), lista_prop in prop_linhas.items():
            if b == 1:
                tam_regra = regras_linhas[l][r-1]
                if tam_regra > 1:
                    for pos, prop in lista_prop:
                        if (tam_regra + pos - 1) > quant_colunas:
                            clausulas_continuidade.append([-prop])
                            continue
                        for cont in range (1, tam_regra):
                            bloco_sucessor = b + cont
                            posic_sucessora = pos + cont
                            chave_sucessora = (l, r, bloco_sucessor)           
                            if chave_sucessora in prop_linhas:
                                for prox_pos, prox_prop in prop_linhas[chave_sucessora]:
                                    if posic_sucessora == prox_pos:
                                        clausulas_continuidade.append([-prop, prox_prop])
                                        break

        self.prop_colunas = prop_colunas
        self.prop_linhas = prop_linhas
        self.prop_colunas_str = prop_colunas_str
        self.prop_linhas_str = prop_linhas_str
        self.clausulas_continuidade = clausulas_continuidade
    
    def regra_quadrado_verdadeiro(self):
        prop_colunas = self.prop_colunas
        prop_linhas = self.prop_linhas
        dicionario_colunas = {}
        dicionario_linhas = {}
        clausulas_quadrado_verdadeiro = []
        
        for chave, itens in prop_colunas.items():
            for tupla in itens:
                item2 = tupla[1]
                if not chave in dicionario_colunas:
                    dicionario_colunas[chave] = []
                dicionario_colunas[chave].append(item2)
        for chave, itens in prop_linhas.items():
            for tupla in itens:
                item2 = tupla[1]
                if not chave in dicionario_linhas:
                    dicionario_linhas[chave] = []
                dicionario_linhas[chave].append(item2)
        for itens in dicionario_colunas.values():
            clausulas_quadrado_verdadeiro.append(itens)
        for itens in dicionario_linhas.values():
            clausulas_quadrado_verdadeiro.append(itens)
        
        self.dicionario_colunas = dicionario_colunas
        self.dicionario_linhas = dicionario_linhas
        self.clausulas_quadrado_verdadeiro = clausulas_quadrado_verdadeiro

    def regra_interconectividade_um(self):
        map_str_to_int = self.map_str_to_int
        clausulas_interconectividade1 = []

        for prop_str, prop_int in map_str_to_int.items():
            if prop_str.startswith("C_"):
                coluna, c, r, b, pos = prop_str.split("_")
                grid = f"G_{c}_{pos}"
                if grid in map_str_to_int:
                    grid_int = map_str_to_int[grid]
                    clausulas_interconectividade1.append([-prop_int, grid_int])
            if prop_str.startswith("L_"):
                linha, l, r, b, pos = prop_str.split("_")
                grid = f"G_{l}_{pos}"
                if grid in map_str_to_int:
                    grid_int = map_str_to_int[grid]
                    clausulas_interconectividade1.append([-prop_int, grid_int])

        self.clausulas_interconectividade1 = clausulas_interconectividade1

    def regra_interconectividade_dois(self):
        map_str_to_int = self.map_str_to_int
        clausulas_interconectividade2 = []
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
                clausulas_interconectividade2.append(clausula)

        self.clausulas_interconectividade2 = clausulas_interconectividade2

    def regra_ordem_e_espacamento(self):
        regras_colunas = self.regras_colunas
        regras_linhas = self.regras_linhas
        map_str_to_int = self.map_str_to_int
        quant_colunas = self.quant_colunas
        quant_linhas = self.quant_linhas
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

        self.clausulas_ordem = clausulas_ordem

'''
#Teste de saída das cláusulas
print("=== UNICIDADE ===")
for c in nanogram.clausulas_unicidade:
    print(c)

print("\n=== CONTINUIDADE ===")
for c in nanogram.clausulas_continuidade:
    print(c)


print("=== QUADRADO VERDADEIRO ===")
for c in nanogram.clausulas_quadrado_verdadeiro:
    print(c)

print("=== INTERCONECTIVIDADE 1 ===")
for c in nanogram.clausulas_interconectividade1:
    print(c)

print("=== INTERCONECTIVIDADE 2 ===")
for c in nanogram.clausulas_interconectividade2:
    print(c)

print("=== ORDEM E ESPAÇAMENTO ===")
for c in nanogram.clausulas_ordem:
    print(c)
'''

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
    nanogram.regra_quadrado_verdadeiro()
    nanogram.regra_interconectividade_um()
    nanogram.regra_interconectividade_dois()
    nanogram.regra_ordem_e_espacamento()

    g = Glucose3()

    for clausula in nanogram.clausulas_unicidade:
        g.add_clause(clausula)
    for clausula in nanogram.clausulas_continuidade:
        g.add_clause(clausula)
    for clausula in nanogram.clausulas_quadrado_verdadeiro:
        g.add_clause(clausula)
    for clausula in nanogram.clausulas_interconectividade1:
        g.add_clause(clausula)
    for clausula in nanogram.clausulas_interconectividade2:
        g.add_clause(clausula)
    for clausula in nanogram.clausulas_ordem:
        g.add_clause(clausula)
    
    if not g.solve():
        print("O nanogram não possui solução")
        return
    
    #o solver analisa o que é clausula verdadeira e o que não é
    #clausula positiva é verdadeira e clausula negativa é falsa
    modelo = g.get_model()
    print(modelo)

    clausulas_verdadeiras = []

    #pega os resultados verdadeiros devolvidos pelo solver
    for m in modelo:
        if m > 0:
            clausulas_verdadeiras.append(m)
    
    print()
    print(clausulas_verdadeiras)

if __name__ == "__main__":
    main()