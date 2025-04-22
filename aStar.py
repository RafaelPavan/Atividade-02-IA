import time
import heapq

inicio = time.perf_counter()

def heuristica(a, b):
    # Distância de Manhattan
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def vizinhos(matriz, linha, coluna):
    direcoes = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # cima, baixo, esquerda, direita
    resultado = []
    for dl, dc in direcoes:
        nl, nc = linha + dl, coluna + dc
        if 0 <= nl < len(matriz) and 0 <= nc < len(matriz[0]):
            resultado.append((nl, nc))
    return resultado


def resolve_labirinto_astar(matriz, linhas, colunas):
    inicio = (0, 0)
    fim = (linhas - 1, colunas - 1)
    fila = []
    heapq.heappush(fila, (0, inicio))
    came_from = {}
    g_score = {inicio: 0}

    while fila:
        _, atual = heapq.heappop(fila)

        if atual == fim:
            caminho = []
            while atual in came_from:
                caminho.append(atual)
                atual = came_from[atual]
            caminho.append(inicio)
            caminho.reverse()
            return caminho

        for vizinho in vizinhos(matriz, *atual):
            if not matriz[vizinho[0]][vizinho[1]].aberta:
                continue

            tentativa_g_score = g_score[atual] + 1
            if vizinho not in g_score or tentativa_g_score < g_score[vizinho]:
                g_score[vizinho] = tentativa_g_score
                f_score = tentativa_g_score + heuristica(vizinho, fim)
                heapq.heappush(fila, (f_score, vizinho))
                came_from[vizinho] = atual

    return None 
