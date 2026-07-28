class Nodo: # Declaracion de la clase

    def __init__(self, t): # Constructor
        self.t = t # Variable de la clase
        self.hijos = [None]*(2*t) # Arreglo de hijos
        self.llaves = [None] * (2*t-1) # Arreglo de llaves
        self.esHoja = True # Validacion por bool
        self.noLlaves = 0 # Numero de llaves

    def BTreeIsFull (self): # Funcion para validar
        return self.noLlaves == 2*self.t -1 # Checa si esta lleno

    def __repr__(self): # Funcion para imprimir como pide
        return "{" + ",".join(map(str,[i for i in self.llaves if i]))+ "}" 

    def __str__(self): # Regresa repr
        return self.__repr__()

class BTree: # Declaracion de la clase
    
    def __init__(self, t): # Constructor con valor dado t
        self.t = t # Guarda atributo para grado
        self.raiz = Nodo (t) # Construccion del nodo raiz

    def BTreeInsert (self, k): # Funcion inserar
        r = self.raiz # Declaracion de r como la raiz
        if r.BTreeIsFull (): # Si la rais esta llena
            s=Nodo (self.t) # Nuevo nodo
            s.esHoja =False # No va a ser hoja
            s.noLlaves =0 # Llaves partiendo en cero
            s.hijos [0] = r # Primer hijo la raiz
            self.raiz =s # Nueva raiz
            self.BTreeSplitChild (s, 0) # Llama a la funcion pasando la nueva raiz y la pocision
            self.BTreeInsertNonFull (s, k) # Pasa la funcion pasando la raiz y la llaves
        else:
            self.BTreeInsertNonFull (r, k) # Llama a la funcion pasando la raiz y la llaves
    
    def BTreeSplitChild (self, x, i): # Declaracion de la llave pasando el padre y el indice
        z = Nodo (self.t) # Nuevo nodo haciendo referencia al hijo
        y = x.hijos [i] # Referencia al hijo en la posicion
        z.esHoja =y.esHoja # Igualacion entre hijos y llaves
        z.noLlaves =self.t-1 # Numero de llaves reducida en menos 1

        for j in range (0, self.t-1): # Pasa los hijos
            z.llaves[j] = y.llaves [j+self.t] # Los hijos de y
            y.llaves [j+self.t] = None # y en nulo

        if not y.esHoja: # Si no es hoja
            for j in range (0, self.t): # Genera el cambio
                z.hijos [j] =y.hijos[j+self.t] # Pasa los hijos
                y.hijos [j + self.t] = None # y vuelto nulo 

        y.noLlaves =self.t-1 # Llaves cambia en menos 1

        for j in range (x.noLlaves, i-1 -1): # Recorrido en hijos
            x.hijos [j+1]= x.hijos [j]

        x.hijos [i+1] = z # Hijo derecho es z

        for j in range (x.noLlaves-1, i-1, -1): # Recorrido en llaves
            x.llaves [j+1] = x.llaves [j]

        x.llaves [i] = y.llaves [self.t-1] # Cambia la mitad
        y.llaves [self.t-1] = None # Se hace nula
        x.noLlaves += 1 # Incremento en uno

    def BTreeInsertNonFull (self, x, k): # Declaracion de funcion
        i=x.noLlaves -1 # Ultimo indice
        if x.esHoja: # Si es la hoja
            while (i>= 0) and (k< x.llaves [i]): # Busca el lugar
                x.llaves [i+1] =x.llaves[i] # Recorrido de llaves
                i -= 1 # Llaves menos uno
            x.llaves [i+1] =k # Ingresa la llave
            x.noLlaves +=1 # Incremento del numero de llaves
        else: # Si no es hoja
            while (i>= 0) and (k<x.llaves [i]): # Busca el indice correcto
                i-=1 # Cambia la posicion
            i+=1 # Cambia el recorrido

            if x.hijos [i].BTreeIsFull(): # Si esta lleno
                self.BTreeSplitChild(x, i) # Aplicacion de la funcon
                if k > x.llaves [i]: # Checa que este correcta la insercion
                    i+=1 # Cambia la posicion

            self.BTreeInsertNonFull (x.hijos [i], k) # Llamado recurivamente


    def BTreeSerch(self, k, x=None): # Declaracion de la funcion
        if x is not None: # Si no esta vacio
            i = 0 # Se iguala la posicion en 0
            while i < x.noLlaves and k > x.llaves[i]: # Checa numero donde buscar
                i += 1 # Incrementa la posicion
            if i < x.noLlaves and k == x.llaves[i]: # Si se encuentra
                return (x, i) # Regresa el valor en posicion
            elif x.esHoja: # Si es una hoja
                return None # Regresa nulo
            else: # Si no 
                return self.BTreeSerch(k, x.hijos[i]) # Regresa  el valor en posicion
        else: # Sino 
            return self.BTreeSerch(k, self.raiz) # Pues la raiz


    def BTreePreOrder(self, ptr, level=0): # Declaracion de la impresion
    
        if ptr != None: # Si el nodo existe
            
            for i in range(ptr.noLlaves): # Recorre las llaves del nodo
                
                if not ptr.esHoja: # Si tiene hijos
                    self.BTreePreOrder(ptr.hijos[i], level + 1) # Recorre hijo izquierdo
                
                for j in range(level): # Indentacion por nivel
                    print("   ", end="")

                print(ptr.llaves[i]) # Imprime la llave
            
            if not ptr.esHoja: # Recorre el ultimo hijo
                self.BTreePreOrder(ptr.hijos[ptr.noLlaves], level + 1)
     

if __name__ == "__main__": # Funcion pricipal

    grado=2 # Nivel del arbol
    
    lista = [3, 1, 4, 2, 5, 7, 6, 11, 15, 22, 35, 21] # Lista a ingresar
    
    print (" Arbol B\n") # Advertencia de lo que esta pasando
    print ("Lista a insertar:", lista) # Imprime los argumentos a pasar
    print ()

    bTree = BTree (grado) # Igualacion de la clase pasando el nivel

    print ("Incercion de elementos\n") # Advertencia de lo que esta pasando

    for r in lista: # Ciclo para la incercion
        bTree.BTreeInsert (r) # Funcion insertando valores
        print ("Insertado", r) # Confirma que se incerto
    print ()

    print ("Busqueda de Elementos\n") # Advertencia de lo que esta pasando
    print ("Exitencia del elemento 3") # Elemento a buscar

    if bTree.BTreeSerch (3) is not None: # Condicion que llama a la funcion pasandole el elemento a buscar
        print (True) # Indica que si esta
    else: # Sino
        print(False) # Indica que no esta

    print ("Exitencia del elemento 6") # Elemento a buscar

    if bTree.BTreeSerch (6) is not None: # Condicion que llama a la funcion pasandole el elemento a buscar
        print (True) # Indica que si esta
    else: # Sino
        print(False) # Indica que no esta

    print ("Exitencia del elemento 15") # Elemento a buscar

    if bTree.BTreeSerch (15) is not None: # Condicion que llama a la funcion pasandole el elemento a buscar
        print (True) # Indica que si esta
    else: # Sino
        print(False) # Indica que no esta

    print ("Exitencia del elemento 0") # Elemento a buscar

    if bTree.BTreeSerch (0) is not None: # Condicion que llama a la funcion pasandole el elemento a buscar
        print (True) # Indica que si esta
    else: # Sino
        print(False) # Indica que no esta

    print ("Exitencia del elemento 13") # Elemento a buscar

    if bTree.BTreeSerch (13) is not None: # Condicion que llama a la funcion pasandole el elemento a buscar
        print (True) # Indica que si esta
    else: # Sino
        print(False) # Indica que no esta

    print ()
    
    print ("Imprecion en Preorden del Arbol\n") # Advertencia de lo que esta pasando
    bTree.BTreePreOrder(bTree.raiz) # Imprime el arbol