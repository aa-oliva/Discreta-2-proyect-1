import heapq
import random
#Andres Oliva 12149

def draw_tile(graph, id, style, width):
    r = "."
    if 'numero' in style and id in style['numero']: r = "%d" % style['numero'][id]
    if 'apunta' in style and style['apunta'].get(id, None) is not None:
        (x1, y1) = id
        (x2, y2) = style['apunta'][id]
        if x2 == x1 + 1: r = "\u2192"
        if x2 == x1 - 1: r = "\u2190"
        if y2 == y1 + 1: r = "\u2193"
        if y2 == y1 - 1: r = "\u2191"
        if y2 == y1 - 1 and x2 == +1: r = "\u2196"
        if y2 == y1 - 1 and x2 == -1: r = "\u2197"
        if y2 == y1 + 1 and x2 == -1: r = "\u2198"
        if y2 == y1 + 1 and x2 == +1: r = "\u2199"
    if 'inicio' in style and id == style['inicio']: r = "A"
    if 'meta' in style and id == style['meta']: r = "Z"
    if 'camino' in style and id in style['camino']: r = "@"
    if id in graph.walls: r = "#" * width
    return r


def grid(graph, width=2, **style):
    for y in range(graph.height):
        for x in range(graph.width):
            print("%%-%ds" % width % draw_tile(graph, (x, y), style, width), end="")
        print()



class SquareGrid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.walls = []

    def destino(self, id):
        (x, y) = id
        return 0 <= x < self.width and 0 <= y < self.height

    def pasable(self, id):
        return id not in self.walls

    def vecinos(self, id):
        (x, y) = id
        resultado = [(x + 1, y), (x, y - 1), (x - 1, y), (x, y + 1)]
        #resultado = [(x + 1, y), (x, y - 1), (x - 1, y), (x, y + 1), (x+1,y+1), (x+1,y-1), (x-1,y+1), (x-1,y-1)]


        if (x + y) % 2 == 0: resultado.reverse()
        resultado = filter(self.destino, resultado)
        resultado = filter(self.pasable, resultado)
        return resultado


class pesos(SquareGrid):
    def __init__(self, width, height):
        super().__init__(width, height)
        self.p = {}

    def cost(self, inicio, para):
        return self.p.get(para, 1)





class PriorityQueue:
    def __init__(self):
        self.elements = []

    def empty(self):
        return len(self.elements) == 0

    def put(self, item, prioridad):
        heapq.heappush(self.elements, (prioridad, item))

    def get(self):
        return heapq.heappop(self.elements)[1]


def dijkstra(graph, inicio, meta):
    frontera = PriorityQueue()
    frontera.put(inicio, 0)
    anterior = {}
    costo = {}
    anterior[inicio] = None
    costo[inicio] = 0

    while not frontera.empty():
        actual = frontera.get()

        if actual == meta:
            break

        for next in graph.vecinos(actual):
            costo_nuevo = costo[actual] + graph.cost(actual, next)
            if next not in costo or costo_nuevo < costo[next]:
                costo[next] = costo_nuevo
                prioridad = costo_nuevo
                frontera.put(next, prioridad)
                anterior[next] = actual

    return anterior, costo


def constructor(anterior, inicio, meta):
    actual = meta
    camino = [actual]
    while actual != inicio:
        actual = anterior[actual]
        camino.append(actual)
    camino.append(inicio)
    camino.reverse()
    return camino


def heuristica(a, b):
    (x1, y1) = a
    (x2, y2) = b
    return abs(x1 - x2) + abs(y1 - y2)


def a_estrella(graph, inicio, meta):
    frontera = PriorityQueue()
    frontera.put(inicio, 0)
    anterior = {}
    costo = {}
    anterior[inicio] = None
    costo[inicio] = 0

    while not frontera.empty():
        actual = frontera.get()

        if actual == meta:
            break

        for next in graph.vecinos(actual):
            costo_nuevo = costo[actual] + graph.cost(actual, next)
            if next not in costo or costo_nuevo < costo[next]:
                costo[next] = costo_nuevo
                prioridad = costo_nuevo + heuristica(meta, next)
                frontera.put(next, prioridad)
                anterior[next] = actual

    return anterior, costo

"""
Se crea el mapa
"""

mapa = pesos(15, 20)
"""
Aqui se pueden agregar las paredes ejemplo: [(1,5),(15,8),...]
"""
mapa.walls = [()]
"""
Aqui se agregan los pesos a cada casilla ejemplo: [(1,5),(15,8),...]
"""
mapa.p = {loc: random.randint(1,5) for loc in [()]}

"""
Se crea la inicializacion de A*
"""
print ("Se prueba A* ")
print ()
print ("mapa de hijos")
anterior, costo = a_estrella(mapa, (0, 19), (14, 0))
grid(mapa, width=3, apunta=anterior, inicio=(0, 19), meta=(14, 0))
print ()
print("pesos")
grid(mapa, width=3, numero=costo, inicio=(0, 19), meta=(14, 0))
print ()
print("Solucion")
grid(mapa, width=3, camino=constructor(anterior, inicio=(0, 19), meta=(14, 0)))

"""
Se crea la inicializacion de Dijkstra
"""
print ()
print ()
print ("Se prueba Dijkstra ")
print ()
print ("mapa de hijos")
anterior, costo = dijkstra(mapa, (0, 19), (14, 0))
grid(mapa, width=3, apunta=anterior, inicio=(0, 19), meta=(14, 0))
print ()
print("pesos")
grid(mapa, width=3, numero=costo, inicio=(0, 19), meta=(14, 0))
print ()
print("solucion")
grid(mapa, width=3, camino=constructor(anterior, inicio=(0, 19), meta=(14, 0)))
