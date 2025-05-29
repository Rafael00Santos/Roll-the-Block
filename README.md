# Space Block - README

## Descrição do Jogo
Space Block é um jogo de puzzle baseado no conceito de "Roll The Block", onde o objetivo é mover um bloco através de um tabuleiro até alcançar a posição de meta. O bloco deve terminar na posição vertical sobre a marca de vitória para completar o nível.

O jogo foi desenvolvido em Python e oferece duas interfaces:
    Interface Gráfica (pygame_interface.py): Versão visual com gráficos e controles intuitivos
    Interface de Terminal (terminal_interface.py): Versão para console com visualização em texto

Somente os níveis do 1 ao 6 podem ser resolvidos pelos algoritmos de pesquisa, devido ao aumento dos obstáculos nos níveis 7, 8 e 9.

## Características Principais
9 níveis de dificuldade progressiva (de 7x7 a 16x16)
Mecânicas de movimento realistas do bloco (rotação e deslize).
Sistema de contagem de movimentos.
Legenda dos obstáculos.
Barra que reage a distância do bloco ao objetivo tendo em conta somente os quatro movimentos permitidos, tem como base a distância de Manhattan de forma semelhante à heuristica utilizada.

Algoritmos de pesquisa para resolver os níveis automaticamente(Niveis 1 a 6):
    DFS (Depth-First Search)
    BFS (Breadth-First Search)
    Greedy Search
    A* Search

## Como Jogar
Comandos
Interface Gráfica:

    W: Mover para cima
    A: Mover para esquerda
    S: Mover para baixo
    D: Mover para direita
    Q: Sair do nível
    ESPAÇO: Pausar/continuar (nos modos de algoritmo)

Interface de Terminal:

    Mesmas teclas (W/A/S/D/Q) para movimentação

## Objetivo
Mover o bloco (representado por "B" no terminal ou um retângulo azul na interface gráfica) até à posição de meta (representada por "X" no terminal ou um retângulo dourado na interface gráfica), terminando na posição vertical. O chão de vidro parte se o bloco estiver na vertical em cima deste. A gema tem de ser apanhada antes de chegar ao objetivo.

#### Requisitos do Sistema
Python 3.x

#### Bibliotecas necessárias:

    pygame
    heapq (já incluída na biblioteca padrão)
    collections (já incluída na biblioteca padrão)

#### Sugestões para instalar:
    Copy
    pip install pygame

## Execute o jogo:

Para a interface gráfica:
    python pygame_interface.py
Para a interface de terminal:
    python terminal_interface.py

    Legenda da matriz: 	
                0-Espaços por onde o bloco andar
				1-Buracos dentro do tabulreiro
                2-Chão de vidro
                4-Gema
				B-Representação do bloco na vertical
				BB-Representação do bloco deitado (Tanto na horizontal como na vertical)
                X-Meta

Ambos os ficheiros vão recorrer as classes definidas no ficheiro 'game_logic' com as regras de movimentação do bloco, formatação do tabuleiro e as restantes funções necessárias para o jogo. Nota: só é possível ter acesso visual aos algoritmos na interface gráfica.

## Estrutura de Arquivos
game_logic.py: Contém as classes principais do jogo (Block, Hole, Board)

pygame_interface.py: Interface gráfica do jogo usando Pygame

terminal_interface.py: Versão do jogo para terminal/console

dfs_solver.py: Implementação do algoritmo DFS para resolver os níveis

bfs_solver.py: Implementação do algoritmo BFS para resolver os níveis

greedy_solver.py: Implementação do algoritmo Greedy Search para resolver os níveis

a_star_solver.py: Implementação do algoritmo A* Search para resolver os níveis

Algoritmos de Resolução Automática
O jogo inclui quatro algoritmos de pesquisa diferentes que podem resolver os níveis automaticamente:

    DFS (Depth-First Search): Busca em profundidade com limite configurável

    BFS (Breadth-First Search): Busca em largura que encontra a solução ótima

    Greedy Search: Algoritmo heurístico que busca minimizar a distância até o objetivo

    A Search*: Combinação de custo real e heurística para encontrar soluções eficientes

#### Nota: 
Executar cada ficheiro individualmente para uma solução com mais especificações(tempo, nodes visitados), cada ficheiro pode também ser configurado na escolha do nível a resolver com as informações presentes no ficheiro pygame_interface.py.

#### Créditos
Desenvolvido como projeto acadêmico baseado no jogo Space Block/Bloroxrz.

#### Problemas Conhecidos
 Em alguns sistemas, a interface gráfica pode fechar ao selecionar um algoritmo de resolução (especialmente DFS)
    Níveis mais complexos podem demorar para ser resolvidos pelos algoritmos
