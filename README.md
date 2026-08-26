# Nonogram Solver

Solucionador de Nonograms desenvolvido em Python como trabalho final da disciplina de
Lógica para Computação.

## Sobre o projeto

O projeto consiste no desenvolvimento de um programa capaz de resolver
qualquer Nonograms de acordo com as regras de preenchimento das linhas
e colunas especificadas no arquivo `SETTINGS.py`, independentemente das
configurações do tabuleiro.

A solução utiliza conceitos de lógica computacional e modelagem do problema
como uma instância de satisfatibilidade booleana (SAT). As restrições do
Nonogram são transformadas em cláusulas que são processadas por um solver SAT,
responsável por encontrar uma configuração válida para o tabuleiro. O resultado
da solução é exibido diretamente no terminal.

## Como funciona

O solucionador utiliza o arquivo `SETTINGS.py` para armazenar exemplos de
Nonograms e suas respectivas configurações. Cada Nonogram possui um nome,
as dimensões do tabuleiro e as regras que devem ser satisfeitas para suas
linhas e colunas.

Para executar um Nonogram, seu nome é informado ao programa por meio do
terminal. O programa localiza as configurações correspondentes no
`SETTINGS.py` e utiliza essas informações para construir a representação
lógica do problema.

A partir das regras fornecidas, o programa cria proposições que representam
as posições dos blocos nas linhas e colunas e as células do tabuleiro.
Em seguida, são geradas cláusulas booleanas que representam as restrições
necessárias para que uma solução seja válida.

As principais restrições implementadas são:

- **Unicidade:** garante que cada bloco de uma regra ocupe uma única posição.
- **Continuidade:** garante que as células pertencentes a um mesmo bloco
  sejam consecutivas.
- **Ordem e espaçamento:** garante que os blocos respeitem a ordem definida
  pelas regras e mantenham o espaçamento necessário entre blocos distintos.
- **Interconectividade:** relaciona os blocos das linhas e das colunas às
  células correspondentes do tabuleiro.

As cláusulas são então enviadas ao solver `Glucose3`, da biblioteca PySAT,
que verifica a existência de uma atribuição que satisfaça todas as
restrições.

Quando uma solução é encontrada, o modelo retornado pelo solver é
interpretado para identificar as células preenchidas. Por fim, o tabuleiro
resolvido é construído e exibido no terminal.

## Tecnologias utilizadas

- Python
- PySAT
- Glucose3

## Estrutura do projeto

```bash
nonogram/
├── Nanogram.py
├── SETTINGS.py
└── README.md
```

## Como executar

### Pré-requisitos

- Python 
- pip

### 1. Clone o repositório

```bash
git clone https://github.com/pedrolucashs/nonogram.git
cd nonogram
```

### 2. Instale as dependência

```
pip install -r requirements.txt
```

### 3. Execute o solucionador

```
py Nanogram.py <nome-do-nonogram>
```

## Exemplos
```
py Nanogram.py macaco
```

```markdown
> Observação: os Nonograms disponíveis e suas respectivas regras são
> definidos no arquivo `SETTINGS.py`.
```
## Contribuições

Desenvolvimento colaborativo entre os três integrantes da equipe, com participação conjunta 
na implementação, modelagem das regras, testes e evolução do solucionador.

## Equipe