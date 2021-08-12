# Declarar objeto de estado (NODO)
class Grafo:
    """Estructura de grafo(mapa de adyacencia) con objetos de vértice, arista y cola para búsquedas"""
    __slots__ = ("_vertices","_movimientos","_root","_colaQ","_colaP","_final","_result","_path")
    def __init__(self, RootState = None, FinalSt = ["1", "2", "3","8","_","4","7", "6", "5"]):
        """Constructor de grafo. Declarará atributos. Iniciará vacio en vértices. """
        self._movimientos = {
            # Esquinas <---------------
            0:{3:"V",1:"-->"},
            2:{5:"V",1:"<--"},
            6:{3:"/\\",7:"-->"},
            8:{5:"/\\",7:"<--"},
            # Laterales <--------------
            1:{0:"<--",4:"V",2:"-->"},
            3:{6:"V",4:"-->",0:"/\\"},
            5:{2:"/\\",4:"<--",8:"V"},
            7:{8:"-->",4:"/\\",6:"<--"},
            # Centro <-----------------
            4:{1:"/\\",5:"-->",7:"V",3:"<--"}}
        self._vertices = {}
        self._colaP = self.PQ()
        self._colaQ = self.PQ()
        self._final = FinalSt
        self._root = self.insertarVertice(RootState)
        self._result = None
        self._path = []
    def insertarVertice(self, dato = [  "1","2","3",
                                        "8","_","4",
                                        "7","6","5"],Final = ["1","2","3","8","_","4","7","6","5"]):
        """Inserta y retorna un vértice nuevo de valor dato"""
        v = self.Vertice(dato, Final)
        self._vertices[v] = {}
        return v
    def retornarVertices(self):
        return self._vertices
    def insertarArista(self, orig, dest, dato = None):
        """Inserta y una arista nueva"""
        a = self.Arista(orig, dest, dato)
        self._vertices[dest][orig] = a
    def Raiz(self):
        """Retorna el nodo raíz"""
        return self._root
    def S_Mas(self, nodo_u):
        """Generador de hijos respecto a un padre."""
        Pos = nodo_u._DatoStr().find("_")
        for x in self._movimientos[Pos].keys():
            datoHijo = nodo_u._Dato().copy()
            datoHijo[Pos], datoHijo[x] = datoHijo[x], datoHijo[Pos]
            Hijo = self.Vertice(datoHijo, self._final)
            if not self._colaP._Find(Hijo) and not self._colaQ._Find(Hijo):
                nuevoHijo = self.insertarVertice(datoHijo)
                self.insertarArista(nodo_u, nuevoHijo, self._movimientos[Pos].get(nuevoHijo._DatoStr().find("_")))
                nuevoHijo.ActHeu()
                self._colaP._Push(nuevoHijo)
    def A_Star(self):
        """Best-First Search o A*."""
        Fin = self.Vertice(self._final)
        self._colaP._Push(self.Raiz())
        print("Realizando búsqueda...")
        while not self._colaP._Find(Fin) and not self._colaP._Empty():
            u = self._colaP._Pop()
            u.ActHeu()
            self._colaQ._Push(u)
            self.S_Mas(u)
            print("Cola P:", self._colaP._Len())
            print("Cola Q:", self._colaQ._Len())
        if self._colaP._Find(Fin):
            print("Resultado encontrado, generando camino de A*...")
            Index = self._colaP._Find(Fin, True)
            self._result = self._colaP._Queue()[Index]
            self._path = [self.HojaResult()].copy()
            step = self.HojaResult()
            while not step == self.Raiz():
                direccion = self.retornarVertices()[step]
                for vertice, arista in direccion.items():
                    self._path.extend([arista, vertice])
                    step = vertice
            self._path.reverse()
            for move in self._path:
                if isinstance(move._Dato(), list):
                    print(move._Heuristic())
                    for a,b,c in zip(range(0,9,3),range(1,9,3),range(2,9,3)):
                        print(move._Dato()[a],move._Dato()[b],move._Dato()[c])
                    print("\n")
                else:
                    print(move._Dato(),"\n")
            print("Profundidad:", self.HojaResult()._Depth())
        elif self._colaP._Empty():
            print("Cola P vacía, no hay solución...")
    def HojaResult(self):
        return self._result
    class Vertice:
        """Estructura de vértice para grafo"""
        __slots__ = ("_elemento","_profundidad","_heuristic","_final","_elementoStr","_finalStr","_HCoef","_DCoef")
        def __init__(self,Dato=["1","2","3","8","_","4","7","6","5"],FinalSt=["1","2","3","8","_","4","7","6","5"],HCoef = 1,DCoef=1):
            """Constructor de vertice. Iniciar grafo con insertarVertice(Dato)"""
            self._elemento = Dato
            self._elementoStr = "".join(self._elemento)
            self._profundidad = 0
            self._final = FinalSt
            self._finalStr = "".join(self._final)
            self._HCoef = HCoef
            self._DCoef = DCoef
        def ActHeu(self):
            suma = self._HCoef*sum([1 for x in range(9) if self._Dato()[x] != self._Final()[x]]) + self._DCoef*self._Depth()
            self._heuristic = suma-1*self._HCoef if self._DatoStr().find("_") != self._FinalStr().find("_") else suma
        def __lt__(self, other_state):
            """Se evalua respecto al valor heurístico dada la comparación nodo_x < nodo_y. Se usa
            la clase PQ para ordenar"""
            return self._heuristic < other_state._heuristic
        def __eq__(self, other_state):
            """Se evalua respecto al dato dada la comparación nodo_x == nodo_y. Se usa en la clase PQ
            para evitar elementos repetidos o verificarlos"""
            return self._elemento == other_state._elemento
        def __le__(self, other_state):
            return self._heuristic <= other_state._heuristic
        def _Final(self):
            return self._final
        def _FinalStr(self):
            return self._finalStr
        def _Depth(self):
            """Retornar profundidad de vértice(Estado de Imposible)"""
            return self._profundidad
        def _Dato(self):
            """Retornar dato asociado o etiqueta de vértice(Estado de Imposible)"""
            return self._elemento
        def _DatoStr(self):
            """Retorna dato asociado como lista"""
            return self._elementoStr
        def _Heuristic(self):
            """Retornar valor heuristico"""
            return self._heuristic
        def __hash__(self):
            """Retornarse a si mismo para usarse como key/set/map, a través de la inherencia."""
            return hash(id(self))
    class Arista:
        """Estructura de arista para grafo"""
        __slots__ = ("_origen","_destino","_elemento")
        def __init__(self, V_Origen, V_Destino, Dato = None):
            """Constructor de arista. Iniciar grafo con insertarArista(Dato)"""
            self._origen, self._destino, self._elemento = V_Origen, V_Destino, Dato
            V_Destino._profundidad = V_Origen._profundidad + 1
        def _Dato(self):
            """Retornar valor o etiqueta de arista(función de transformación)"""
            return self._elemento
        def __hash__(self):
            """ Retornarse a si mismo como tupla de incidencia para usarse como llave/valor,
                en diccionario"""
            return hash((self._origen, self._destino))
    class PQ:
        """Clase de cola de prioridad"""
        __slots__ = ("_queue","_orden","_duplis")
        def __init__(self, Ord = True, Dup = False):
            self._queue = []
            self._orden = Ord
            self._duplis = Dup
        def _Push(self, newState):
            """Ingresar elemento a la cola, y ordernalo. Dados los parametros Ord(Ordenada) y
            Dup(Duplicados), ordena y evita duplicados"""
            if self._duplis or self._Empty():
                self._queue.append(newState)
            elif not self._Find(newState):
                self._queue.append(newState)
            if self._orden:
                for x in range(len(self._queue)-1,0,-1):
                    if self._queue[x] < self._queue[x-1]:
                        self._queue[x], self._queue[x-1] = self._queue[x-1], self._queue[x]
                    else:
                        break
        def _Empty(self):
            """Determinar sí cola esta vacía"""
            return self._queue == []
        def _Pop(self):
            """Retirar elemento de la cola"""
            if not self._Empty():
                return self._queue.pop(0)
            else:
                print("Cola vacía")
        def _Find(self, state, Index = False):
            """Buscar elemento en la cola"""
            if not self._Empty():
                for i, duplicate in enumerate(self._Queue()):
                    if state == duplicate:
                        return i if Index else True
            return False
        def _Queue(self):
            """Retorna la cola"""
            return self._queue
        def _Len(self):
            return len(self._Queue())
PathFinder = Grafo(["2","1","6",
                    "4","_","8",
                    "7","5","3"])
PathFinder.A_Star()
