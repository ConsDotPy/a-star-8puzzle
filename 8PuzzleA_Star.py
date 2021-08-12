# Datos de entrada

# init = ["1", "_", "2",
#        "7", "5", "4",
#        "8", "6", "3"]

# Term = ['1', '6', '2',
#        '7', '3', '4',
#        '_', '8', '5']

init = ["8", "7", "6",
        "1", "_", "5",
        "2", "3", "4"]

Term = ['1', '2', '3',
        '8', '_', '4',
        '7', '6', '5']

# Coeficientes de g, h
qK = 1
qH = 1

# Movimietos posibles del Puzzle para posición actual de espacio vacío
movimientos = {
    # Esquinas <---------------
    0: {3: "V", 1: "-->"},
    2: {5: "V", 1: "<--"},
    6: {3: "/\\", 7: "-->"},
    8: {5: "/\\", 7: "<--"},
    # Laterales <--------------
    1: {0: "<--", 4: "V", 2: "-->"},
    3: {6: "V", 4: "-->", 0: "/\\"},
    5: {2: "/\\", 4: "<--", 8: "V"},
    7: {8: "-->", 4: "/\\", 6: "<--"},
    # Centro <-----------------
    4: {1: "/\\", 5: "-->", 7: "V", 3: "<--"}}


# Clase de nodo
class Nodo:
    """"Objeto de nodo que contiene estado actual del puzzle así como el valor f(u) = g(u) + h(u)"""

    def __init__(self, dato, dad, mov):
        # Posición de puzzle
        self._dato = dato
        # Determinar el padre
        self._dad = dad
        # Movimiento con el que se llegó a dicho estado
        self._mov = mov
        # Determinar profundidad del nodo en árbol
        self._depth = 0 if not dad else dad.Depth() + qK
        # Determinar valor de criterio y calcular heurística
        self._heuristic = self.Wrong() + self._depth

    def __le__(self, other):
        """"Método para compara 2 nodos"""
        return self.Heu() <= other.Heu()

    def __lt__(self, other):
        """"Método para compara 2 nodos"""
        return self.Heu() < other.Heu()

    def __eq__(self, other):
        """Se evalua respecto al dato dada la comparación nodo_x == nodo_y. Se usa en la clase BestFirst
        para evitar elementos repetidos o verificarlos"""
        return self.Dato() == other.Dato()

    def Wrong(self):
        """"Cálculo de criterio(Posiciones correctas). El error posición del espacio vacío se cuenta solo una vez si se
            encuentra en distintas pocisiones(Estado final e inicial)."""
        suma = qH * sum([1 for x in range(9) if self._dato[x] != Term[x]])
        return suma - qH if "".join(self._dato).find("_") != "".join(Term).find("_") else suma

    def Depth(self):
        return self._depth

    def Heu(self):
        """Retornar valor heuristico"""
        return self._heuristic

    def Dato(self):
        """Retornar dato asociado o etiqueta de vértice(Estado de 8-Puzzle)"""
        return self._dato

    def Mov(self):
        return self._mov

    def Dad(self):
        return self._dad


# Instancia de cola Q
class ColaQ:
    """Clase simple de una cola. Cola Q no necesita muchos detalles."""

    def __init__(self):
        self._queue = []

    def Push(self, nodo):
        if self.isEmpty():
            self._queue.append(nodo)
        elif not self.Find(nodo):
            self._queue.append(nodo)

    # Búsqueda de duplicados e index
    def Find(self, nodo):
        for duplicate in self._queue:
            if nodo == duplicate:
                return True
        return False

    def isEmpty(self):
        return not self._queue

    def Len(self):
        return len(self._queue)


# Instancia de cola P
class BestFirst:
    """"Cola ordenada de acuerdo a un criterio de evaluación. Validá existencia y ordena elementos en cada Push()."""

    def __init__(self):
        self._queue = []

    # Agregar a cola
    def Push(self, nodo):
        """Ingresar elemento a la cola, ordena y evita duplicados"""
        if self.isEmpty():
            self._queue.append(nodo)
        else:
            self._queue.append(nodo)
            # Acomodar cola nuevos estados
            for x in range(len(self._queue) - 1, 0, -1):
                if self._queue[x] <= self._queue[x - 1]:
                    self._queue[x], self._queue[x - 1] = self._queue[x - 1], self._queue[x]
                else:
                    break

    def Pop(self):
        """Retirar elemento de la cola"""
        return self._queue.pop(0)

    # Búsqueda de duplicados y obtención de index
    def Find(self, nodo):
        """Buscar elemento en la cola"""
        if not self.isEmpty():
            for index, duplicate in enumerate(self._queue):
                if nodo == duplicate:
                    return True, index
        return False

    # Determinar si está cola vacía
    def isEmpty(self):
        """Determinar sí cola esta vacía"""
        return not self._queue

    # Llamar nodo de cola dado index
    def getNode(self, index):
        return self._queue[index]

    # Longitud de cola
    def Len(self):
        return len(self._queue)


# Función principal
def A_Star(Raiz):
    """"Función principal de búsqueda de solución(A*)."""
    global colaQ
    global colaP
    # Primer elemento en cola
    colaP.Push(Raiz)
    # Iterar hasta que P contenga el estado terminal o quede vacía
    while not colaP.Find(Terminal) and not colaP.isEmpty():
        # Remover elemento de cola P y mover a Q
        u = colaP.Pop()
        colaQ.Push(u)
        # Generar hijos de nodo actual
        Expander(u)
        print("Cola P:", colaP.Len())
        print("Cola Q:", colaQ.Len())
    if colaP.isEmpty():
        print("\nNo hay solución, cola P vacía...")
    else:
        # Determinar camino hacía raíz
        Done = colaP.getNode(colaP.Find(Terminal)[1])
        nodePath = Done
        path = []
        while nodePath.Dad() is not None:
            path.append(nodePath.Dato())
            path.append(("Profundidad = " + str(nodePath.Depth()), "Heurística = " + str(nodePath.Heu())))
            path.append("\n" + nodePath.Mov())
            nodePath = nodePath.Dad()
        path.reverse()
        print("\n")
        Imprimir(init)
        for elem in path:
            if isinstance(elem, list):
                Imprimir(elem)
            else:
                print(elem)


def Imprimir(array):
    print(array[0:3])
    print(array[3:6])
    print(array[6:9])


def Expander(nodo):
    """"Función para determinar hijos y agregarlos a P"""
    global colaP
    # Determinar posición de espacio vacío
    pos = "".join(nodo.Dato()).find("_")
    # Iterar sobre las posibles nuevas posiciones(Diccionario)
    for x in movimientos[pos].keys():
        datoHijo = nodo.Dato().copy()
        # Intercambio de pocisiones
        datoHijo[pos], datoHijo[x] = datoHijo[x], datoHijo[pos]
        # Generar nuevo nodo
        Hijo = Nodo(datoHijo, nodo, movimientos[pos][x])
        # Determinar si nuevo nodo existe actualemente en P o en Q
        if not colaP.Find(Hijo) and not colaQ.Find(Hijo):
            colaP.Push(Hijo)


# Instanciar Colas
colaQ = ColaQ()
colaP = BestFirst()

# Nodo terminal(útil para determinar existencia)
Terminal = Nodo(Term, None, None)

root = Nodo(init, None, None)
A_Star(root)
