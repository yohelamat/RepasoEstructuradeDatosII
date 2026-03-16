# ==========================================
# REPASO: ESTRUCTURAS DE DATOS II
# Estudiante: Yohel Amat
# ==========================================

# --- CLASE BASE DEL PRODUCTO ---
class Producto:
    def __init__(self, codigo, nombre, cantidad, precio):
        self.codigo = codigo
        self.nombre = nombre
        self.cantidad = cantidad
        self.precio = precio

    def __str__(self):
        return f"[{self.codigo}] {self.nombre} | Cant: {self.cantidad} | ${self.precio}"

# --- 1. ARREGLOS (Carga inicial y Ordenamiento) ---
class ArregloInventario:
    def __init__(self):
        # Arreglo nativo de Python con carga inicial
        self.datos = [
            Producto(301, "Filtro Subaru", 15, 25.0),
            Producto(105, "Laptop ASUS", 5, 850.0),
            Producto(202, "Dobok TKD", 10, 45.0),
            Producto(408, "Piedra Pizza", 8, 30.0)
        ]

    def ordenar_por_precio(self):
        # Método Burbuja para ordenar el arreglo nativo
        n = len(self.datos)
        for i in range(n-1):
            for j in range(0, n-i-1):
                if self.datos[j].precio > self.datos[j+1].precio:
                    self.datos[j], self.datos[j+1] = self.datos[j+1], self.datos[j]
        print("✅ Arreglo ordenado por precio (Ascendente).")

    def mostrar(self):
        for prod in self.datos:
            print(prod)


# --- 2. LISTAS ENLAZADAS (Inventario Dinámico) ---
class NodoLista:
    def __init__(self, producto):
        self.producto = producto
        self.siguiente = None

class ListaEnlazada:
    def __init__(self):
        self.cabeza = None

    def agregar(self, producto):
        nuevo_nodo = NodoLista(producto)
        if not self.cabeza:
            self.cabeza = nuevo_nodo
        else:
            actual = self.cabeza
            while actual.siguiente:
                actual = actual.siguiente
            actual.siguiente = nuevo_nodo

    def eliminar(self, codigo):
        actual = self.cabeza
        anterior = None
        while actual and actual.producto.codigo != codigo:
            anterior = actual
            actual = actual.siguiente
        
        if actual is None:
            return None # No se encontró
        
        if anterior is None:
            self.cabeza = actual.siguiente # Era el primero
        else:
            anterior.siguiente = actual.siguiente # Se salta el nodo
        return actual.producto

    def buscar(self, codigo):
        actual = self.cabeza
        while actual:
            if actual.producto.codigo == codigo:
                return actual.producto
            actual = actual.siguiente
        return None

    def mostrar(self):
        actual = self.cabeza
        if not actual:
            print("Lista vacía.")
        while actual:
            print(actual.producto)
            actual = actual.siguiente


# --- 3. PILAS (Historial y Ctrl+Z / LIFO) ---
class PilaHistorial:
    def __init__(self):
        self.historial = [] # Pila basada en lista (LIFO)

    def registrar_accion(self, accion, producto):
        if len(self.historial) >= 10:
            self.historial.pop(0) # Mantiene solo las últimas 10
        self.historial.append((accion, producto))
        print(f"📝 Historial: Se registró '{accion}' del producto {producto.codigo}")

    def deshacer(self, lista_enlazada):
        if not self.historial:
            print("No hay acciones para deshacer.")
            return
        
        accion, producto = self.historial.pop() # Saca el último (LIFO)
        if accion == "AGREGAR":
            lista_enlazada.eliminar(producto.codigo)
            print(f"⏪ Deshacer: Se eliminó el producto {producto.codigo} que había sido agregado.")
        elif accion == "ELIMINAR":
            lista_enlazada.agregar(producto)
            print(f"⏪ Deshacer: Se restauró el producto {producto.codigo} que había sido eliminado.")


# --- 4. COLAS (Fila de Pedidos / FIFO) ---
class ColaPedidos:
    def __init__(self):
        self.fila = [] # Cola basada en lista (FIFO)

    def nuevo_pedido(self, cliente, codigo_prod, cant):
        self.fila.append({"cliente": cliente, "codigo": codigo_prod, "cant": cant})
        print(f"🛒 Pedido encolado: {cliente} solicita {cant} unid. del cód {codigo_prod}.")

    def atender_pedido(self, lista_enlazada):
        if not self.fila:
            print("No hay clientes en la fila.")
            return
        
        pedido = self.fila.pop(0) # Saca el primero (FIFO)
        producto = lista_enlazada.buscar(pedido["codigo"])
        
        if producto and producto.cantidad >= pedido["cant"]:
            producto.cantidad -= pedido["cant"]
            print(f"✅ Pedido despachado a {pedido['cliente']}. Stock restante: {producto.cantidad}")
        else:
            print(f"❌ Error al atender a {pedido['cliente']}: Producto no encontrado o stock insuficiente.")


# --- 5. ÁRBOL BINARIO DE BÚSQUEDA (ABB) ---
class NodoArbol:
    def __init__(self, producto):
        self.producto = producto
        self.izquierda = None
        self.derecha = None

class ArbolBinario:
    def __init__(self):
        self.raiz = None

    def insertar(self, producto):
        if self.raiz is None:
            self.raiz = NodoArbol(producto)
        else:
            self._insertar_recursivo(self.raiz, producto)

    def _insertar_recursivo(self, nodo_actual, producto):
        if producto.codigo < nodo_actual.producto.codigo:
            if nodo_actual.izquierda is None:
                nodo_actual.izquierda = NodoArbol(producto)
            else:
                self._insertar_recursivo(nodo_actual.izquierda, producto)
        elif producto.codigo > nodo_actual.producto.codigo:
            if nodo_actual.derecha is None:
                nodo_actual.derecha = NodoArbol(producto)
            else:
                self._insertar_recursivo(nodo_actual.derecha, producto)

    def inorden(self, nodo):
        if nodo:
            self.inorden(nodo.izquierda)
            print(f"Cód: {nodo.producto.codigo} | {nodo.producto.nombre}")
            self.inorden(nodo.derecha)


# ==========================================
# EJECUCIÓN DEL SISTEMA Y PRUEBAS
# ==========================================
if __name__ == "__main__":
    print("\n" + "="*40)
    print(" INICIANDO SISTEMA INTEGRAL DE INVENTARIO ")
    print("="*40)

    # 1. Prueba de Arreglos
    print("\n--- 1. ARREGLOS ---")
    arreglo = ArregloInventario()
    arreglo.ordenar_por_precio()
    arreglo.mostrar()

    # 2. Prueba de Listas Enlazadas y Pilas
    print("\n--- 2 Y 3. LISTAS ENLAZADAS Y PILAS (HISTORIAL) ---")
    lista = ListaEnlazada()
    pila = PilaHistorial()
    
    # Cargamos datos a la lista
    for p in arreglo.datos:
        lista.agregar(p)
    
    nuevo_prod = Producto(505, "Memoria 32GB", 20, 75.0)
    lista.agregar(nuevo_prod)
    pila.registrar_accion("AGREGAR", nuevo_prod)
    
    print("\nInventario en Lista Enlazada:")
    lista.mostrar()
    
    print("\nAplicando 'Deshacer'...")
    pila.deshacer(lista)
    print("\nInventario tras deshacer:")
    lista.mostrar()

    # 3. Prueba de Colas
    print("\n--- 4. COLAS (FILA DE PEDIDOS) ---")
    cola = ColaPedidos()
    cola.nuevo_pedido("Carlos", 105, 2) # Pide 2 laptops
    cola.nuevo_pedido("María", 301, 5)  # Pide 5 filtros
    
    print("\nAtendiendo fila:")
    cola.atender_pedido(lista)
    cola.atender_pedido(lista)

    # 4. Prueba de Árboles
    print("\n--- 5. ÁRBOL BINARIO (ABB) ---")
    arbol = ArbolBinario()
    # Insertamos los datos del arreglo al árbol
    for p in arreglo.datos:
        arbol.insertar(p)
    
    print("Recorrido Inorden del Árbol (Se imprime ordenado por Código automáticamente):")
    arbol.inorden(arbol.raiz)
    
    print("\n" + "="*40)
    print(" FIN DE LAS PRUEBAS ")
    print("="*40 + "\n")