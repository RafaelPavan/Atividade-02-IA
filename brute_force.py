def resolver_forca_bruta(malha, linha, coluna, fimLinha, fimColuna, visitados, caminho):
    if (linha, coluna) == (fimLinha, fimColuna):
        caminho.append((linha, coluna))
        return True

    if linha < 0 or linha >= malha.qtLinhas or coluna < 0 or coluna >= malha.qtColunas:
        return False

    if (linha, coluna) in visitados:
        return False

    if not malha[linha][coluna].aberta:
        return False

    visitados.add((linha, coluna))
    caminho.append((linha, coluna))

    direcoes = [(0, 1), (1, 0), (0, -1), (-1, 0)] 
    for dx, dy in direcoes:
        if resolver_forca_bruta(malha, linha + dx, coluna + dy, fimLinha, fimColuna, visitados, caminho):
            return True

    caminho.pop()
    return False
