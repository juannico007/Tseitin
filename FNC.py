# -*- coding: utf-8 -*-

# Subrutinas para la transformacion de una
# formula a su forma clausal

# Subrutina de Tseitin para encontrar la FNC de
# la formula en la pila
# Input: A (cadena) de la forma
#                   p=-q
#                   p=(qYr)
#                   p=(qOr)
#                   p=(q>r)
# Output: B (cadena), equivalente en FNC
def enFNC(A):
    assert(len(A)==4 or len(A)==7), u"Fórmula incorrecta!"
    B = ''
    p = A[0]
    # print('p', p)
    if "-" in A:
        q = A[-1]
        # print('q', q)
        B = "-"+p+"O-"+q+"Y"+p+"O"+q
    elif "Y" in A:
        q = A[3]
        # print('q', q)
        r = A[5]
        # print('r', r)
        B = q+"O-"+p+"Y"+r+"O-"+p+"Y-"+q+"O-"+r+"O"+p
    elif "O" in A:
        q = A[3]
        # print('q', q)
        r = A[5]
        # print('r', r)
        B = "-"+q+"O"+p+"Y-"+r+"O"+p+"Y"+q+"O"+r+"O-"+p
    elif ">" in A:
        q = A[3]
        # print('q', q)
        r = A[5]
        # print('r', r)
        B = q+"O"+p+"Y-"+r+"O"+p+"Y-"+q+"O"+r+"O-"+p
    else:
        print(u'Error enENC(): Fórmula incorrecta!')

    return B

#Funcion para determinar su un caracter en un atomo o no
#Input: A (caracter)
def es_atomo(A):
    return A != "-" and A != "Y" and A != "O" and A != ">" and A != "="

# Algoritmo de transformacion de Tseitin
# Input: A (cadena) en notacion inorder
# Output: B (cadena), Tseitin
def Tseitin(A, letrasProposicionalesA):
    letrasProposicionalesB = [chr(x) for x in range(256, 1200)]
    assert(not bool(set(letrasProposicionalesA) & set(letrasProposicionalesB))), u"¡Hay letras proposicionales en común!"

    #  IMPLEMENTAR AQUI ALGORITMO TSEITIN
    l = []              #Lista de conjunciones
    pila = []           #Pila
    i = -1              #Contador de variables nuevas
    s = A[0]            #Simbolo para trabajar
    
    while len(A) > 0:
        if es_atomo(s) and len(pila) != 0 and pila[-1] == "-":
            i += 1
            atomo = letrasProposicionalesB[i]
            pila = pila[:-1]
            l.append(atomo + "=-" + s)
            A = A[1:]
            if len(A) > 0:
                s = A[0]
        elif s == ")":
            w = pila[-1]
            u = pila[-2]
            v = pila[-3]
            pila = pila[:len(pila) - 4]
            i+=1
            atomo = letrasProposicionalesB[i]
            l.append(atomo + "=(" + v + u + w + ")")
            s = atomo
        else:
            pila.append(s)
            A = A[1:]
            if len(A) > 0:
                s = A[0]
    
    B = ""
    if i < 0:
        atomo = pila[-1]
    else:
        atomo = letrasProposicionalesB[i]
        
    for x in l:
        y = enFNC(x)
        B += "Y" + y
        
    B = atomo + B
    return B

# Subrutina Clausula para obtener lista de literales
# Input: C (cadena) una clausula
# Output: L (lista), lista de literales
# Se asume que cada literal es un solo caracter
def Clausula(C):
    L=[]
    while len(C)>0:
        s=C[0]
        if s =="-" :
            L.append(s+C[1])
            C=C[:3]
        else:
            L.append(s)
            C=C[:2]
    return L  
    
    

# Algoritmo para obtencion de forma clausal
# Input: A (cadena) en notacion inorder en FNC
# Output: L (lista), lista de listas de literales
def formaClausal(A):
   F=[]
   o=0
   while len(A)>0:
       if o>=len(A):
           F.append(Clausula(A))
           A=[]
       else:
           if A[0]=="Y":
               F.append(Clausula(A[:o]))
               A = A[o+1:]
               o=0
           else:
               o+=1
   return F
   
    
