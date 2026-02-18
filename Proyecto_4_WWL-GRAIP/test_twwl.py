import networkx as nx
from twwl import TWWL  # <--- Aquí importas tu código

def test_ejecucion():
    # 1. Definir tus grafos
    G1 = nx.Graph([(1,2), (2,3), (3,1), (3,4), (3,5)])
    G2 = nx.Graph([(5,1), (1,2), (2,5), (3,5), (3,4)])

    # 2. Asignar etiquetas (obligatorio para TWWL)
    for n in G1.nodes(): G1.nodes[n]['label'] = 'A'
    for n in G2.nodes(): G2.nodes[n]['label'] = 'A'

    # 3. Instanciar y ejecutar el modelo
    modelo = TWWL(H=2)
    mis_grafos = [G1, G2]
    
    print("Calculando distancias...")
    modelo.fit(mis_grafos)
    distancias = modelo.compute_distance_matrix()

    # 4. Mostrar resultados
    print("\nMatriz de resultados:")
    print(distancias)
    print(f"\nDistancia G1 <-> G2: {distancias[0,1]}")

if __name__ == "__main__":
    test_ejecucion()