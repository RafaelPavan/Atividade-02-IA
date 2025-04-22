################################################################
###                 M O S T R A   M A Z E                    ###
################################################################
### Neste teste, mostra o labirinto gerado pelo algoritmo de ###
### Aldous-Broder                                            ###
################################################################
### Moises Kaufmann e Rafael Pavan                           ###
################################################################

import pygame
import sys
import copy
from random import randint
import aStar
import brute_force
import time

class ArestasFechadas:
    def __init__(self, superior, inferior, esquerda, direita):
        self.superior = superior
        self.inferior = inferior
        self.esquerda = esquerda
        self.direita = direita

class Celula:
    def __init__(self, arestasFechadas, corPreenchimento, corVisitada, corLinha, corAberta, visitada, aberta):
        self.arestasFechadas = arestasFechadas
        self.corPreenchimento = corPreenchimento
        self.corVisitada = corVisitada
        self.corLinha = corLinha
        self.corAberta = corAberta
        self.visited = visitada
        self.aberta = aberta
        self.solucao = False

    def desenhar(self, tela, x, y, aresta):
        if self.solucao:
            pygame.draw.rect(tela, (0, 255, 0), (x, y, aresta, aresta)) 
        elif self.aberta:
            pygame.draw.rect(tela, self.corAberta, (x, y, aresta, aresta))
        else:
            pygame.draw.rect(tela, self.corPreenchimento, (x, y, aresta, aresta))

        pygame.draw.rect(tela, self.corLinha, (x, y, aresta, aresta), 1)


class AldousBroder:
    def __init__(self, qtLinhas, qtColunas, aresta, celulaPadrao):
        self.matriz = Malha(qtLinhas, qtColunas, aresta, celulaPadrao)
        self.qtLinhas = qtLinhas
        self.qtColunas = qtColunas
        self.aresta = aresta
        self.celulaPadrao = celulaPadrao
        # self.visitados = []

    def __len__(self):
        return len(self.matriz)

    def __iter__(self):
        return iter(self.matriz)

    def resetaLabirinto(self):
        for linha in range(self.qtLinhas):
            for coluna in range(self.qtColunas):
                self.matriz[linha][coluna] = copy.deepcopy(self.celulaPadrao)

    def SorteiaCelulaVizinha(self, linhaCelulaAtual, colunaCelulaAtual):
        encontrou = False
        while (encontrou == False):
            linhaVizinha = linhaCelulaAtual + randint(-1, 1)
            colunaVizinha = colunaCelulaAtual + randint(-1, 1)
            if (
                    linhaVizinha >= 0 and linhaVizinha < self.qtLinhas and colunaVizinha >= 0 and colunaVizinha < self.qtColunas):
                encontrou = True

        return linhaVizinha, colunaVizinha

    def GeraLabirinto(self):

        self.resetaLabirinto()

        unvisitedCells = self.qtLinhas * self.qtColunas
        currentCellLine, currentCellColumn, neighCellLine, neighCellColumn = -1, -1, -1, -1

        # sorteia uma célula qualquer
        currentCellLine = randint(0, self.qtLinhas - 1)
        currentCellColumn = randint(0, self.qtColunas - 1)
        self.matriz[0][0].aberta = True
        self.matriz[self.qtLinhas - 1][self.qtColunas - 1].aberta = True

        while (unvisitedCells > 0):

            # Sorteia um vizinho qualquer da célula atual
            neighCellLine, neighCellColumn = self.SorteiaCelulaVizinha(currentCellLine, currentCellColumn)

            if (self.matriz[neighCellLine][neighCellColumn].visited == False):
                # incluir aqui a rotina paar abrir uma passagem. Por enquanto, apenas pinta a célula
                self.matriz[currentCellLine][currentCellColumn].aberta = True
                self.matriz[neighCellLine][neighCellColumn].visited = True

                unvisitedCells -= 1
                # cont += 1

            currentCellLine, currentCellColumn = neighCellLine, neighCellColumn

class Malha:
    def __init__(self, qtLinhas, qtColunas, aresta, celulaPadrao):
        self.qtLinhas = qtLinhas
        self.qtColunas = qtColunas
        self.aresta = aresta
        self.celulaPadrao = celulaPadrao
        self.matriz = self.GeraMatriz()

    def __len__(self):
        return len(self.matriz)

    def __iter__(self):
        return iter(self.matriz)

    def __getitem__(self, index):
        return self.matriz[index]

    def __setitem__(self, index, value):
        self.matriz[index] = value

    def __aslist__(self):
        return self.matriz

    def GeraMatriz(self):
        matriz = []
        for i in range(self.qtLinhas):
            linha = []
            for j in range(self.qtColunas):
                linha.append(copy.deepcopy(self.celulaPadrao))
            matriz.append(linha)
        return matriz

    def DesenhaLabirinto(self, tela, x, y):
        for linha in range(self.qtLinhas):
            for coluna in range(self.qtColunas):
                self.matriz[linha][coluna].desenhar(tela, x + coluna * self.aresta, y + linha * self.aresta, self.aresta)

def gerar_labirinto_unico(preto, cinza, branco, N, M, aresta):

    celulaPadrao = Celula(ArestasFechadas(False, False, False, False), preto, cinza, preto, branco,False, False)
    labirinto = AldousBroder(N, M, aresta, celulaPadrao)
    labirinto.GeraLabirinto()

    return labirinto

def render_a_star(labirinto, branco, N, M, aresta):
    inicio = time.perf_counter()
    pygame.init()

    [largura, altura] = [600, 300]

    vermelho = (255, 0, 0)
    a_star_call = aStar.resolve_labirinto_astar(labirinto.matriz, N, M)

    # Cria a janela
    tela = pygame.display.set_mode((largura, altura))
    pygame.display.set_caption('A* (A Star)')

    ###
    ### Loop principal
    ###

    fim = time.perf_counter()
    print(f"Tempo de execução A*: {fim - inicio:.4f} segundos")
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        ### preenche a tela com a cor branca
        tela.fill(branco)
        
        xOffset = (tela.get_width() - (M * aresta)) // 2
        yOffset = (tela.get_height() - (N * aresta)) // 2
        labirinto.matriz.DesenhaLabirinto(tela, xOffset, yOffset)

        if a_star_call:
            for (linhaC, colunaC) in a_star_call:
                x = xOffset + colunaC * aresta
                y = yOffset + linhaC * aresta
                pygame.draw.rect(tela, vermelho, (x, y, aresta, aresta))
        else:
            print("O  labirinto em questão não possui solução")
            break

        ### atualiza a tela
        pygame.display.flip()


def render_brute_force(labirinto, branco, N, M, aresta):
    inicio = time.perf_counter()
    pygame.init()

    # Dimensões da janela
    [largura, altura] = [600, 300]

    caminho = []
    visitados = set()

    brute_force_call = brute_force.resolver_forca_bruta(labirinto.matriz, 0, 0, N - 1, M - 1, visitados, caminho)

    # Cria a janela
    tela = pygame.display.set_mode((largura, altura))
    pygame.display.set_caption('Brute Force')

    for l, c in caminho:
        labirinto.matriz[l][c].solucao = True
    
    fim = time.perf_counter()
    print(f"Tempo de execução Força Bruta: {fim - inicio:.4f} segundos")
        
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        ### preenche a tela com a cor branca
        tela.fill(branco)

        if brute_force_call:
            [linha, coluna] = ((tela.get_width() - (M * aresta)) // 2,
                           (tela.get_height() - (N * aresta)) // 2)
            labirinto.matriz.DesenhaLabirinto(tela, linha, coluna)
        else:
            print("deu ruim")
            break

        ### atualiza a tela
        pygame.display.flip()

if __name__ == '__main__':
    render_a_star()