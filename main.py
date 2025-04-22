import multiprocessing
import labirinto

def run_astar(unico, branco, N, M, aresta):
    labirinto.render_a_star(unico, branco, N, M, aresta)

def run_brute_force(unico, branco, N, M, aresta):
    labirinto.render_brute_force(unico, branco, N, M, aresta)

def define_labirinto_unico(preto, branco, cinza, N, M, aresta):
    preto = (0, 0, 0)
    branco = (255, 255, 255)
    cinza = (128, 128, 128)
    N = 20 
    M = 20  
    aresta = 10

    return labirinto.gerar_labirinto_unico(preto, cinza, branco, N, M, aresta)

def main():
    preto = (0, 0, 0)
    branco = (255, 255, 255)
    cinza = (128, 128, 128)
    N = 20
    M = 20
    aresta = 10

    unico = define_labirinto_unico(preto, branco, cinza, N, M, aresta)

    p1 = multiprocessing.Process(target=run_astar, args=(unico, branco, N, M, aresta))
    p2 = multiprocessing.Process(target=run_brute_force, args=(unico, branco, N, M, aresta))

    p1.start()
    p2.start()

    p1.join()
    p2.join()

if __name__ == "__main__":
    main()
