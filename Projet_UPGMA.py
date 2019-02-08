#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: aminecharko
"""

def trouverDistMin(mat):
    case_min = 999999999 # on génére case_min à l'infini
    x, y = -1, -1
    for i in range(len(mat)):
        for j in range(len(mat[i])):
            if (mat[i][j] < case_min and mat[i][j] != 0):
                case_min = mat[i][j]
                x, y = i, j
    return x, y


def calculMatrice(i,j,matDist,A):
    l = [0]
    for k in range(len(matDist[0])):
        if (k != i and k != j):
            nI = float(A.G.nbFeuille())
            nJ = float(A.D.nbFeuille())
            dIk = float(matDist[i][k])
            dJk = float(matDist[j][k])
            l.append(((nI/(nI+nJ))*dIk)+((nJ/(nI+nJ))*dJk))

    matDist.pop(i)
    matDist.pop(j-1)
    for k in range(len(matDist)):
        matDist[k].pop(i)
        matDist[k].pop(j-1)

    matDist.insert(0,l)
    for k in range(1,len(matDist)):
        matDist[k].insert(0,l[k])

def swap_ab(node,ab,x,y):
    tmp1 = ab.pop(x)
    tmp2 = ab.pop(y-1)
    ab.insert(x,node)

    return ab

class Cl_AB():
    #arbre
    def __init__(self):
        self.id = ""
        self.distG = 0.0 #distance gauche
        self.distD = 0.0 #distance droite
        self.G = None #fils gauche
        self.D = None #fils gauche
        self.pere = None

    #return vrai si self est une feuille, faux sinon
    def estFeuille(self):
        return ((self.D is None) and (self.G is None))

    #return le nombre de feuilles
    def nbFeuille(self):
        if self.estFeuille():
            return 1
        else:
            return self.D.nbFeuille()+self.G.nbFeuille()

    #return la somme de toutes les distances entre la racine et une de ses feuilles
    def lgBranche(self):
        A = self
        dist = 0
        while (not A.estFeuille()):
            dist += A.distG
            A = A.G
        return dist  
    
    def fusionAb(self,AG,AD,dij):
        self.G = AG
        self.distG = dij-AG.lgBranche()
        self.D = AD
        self.distD = dij-AD.lgBranche()
        AG.pere = self
        AD.pere = self
        return self
    
    def UPGMA(self,matDist,ab):
    
        if (len(matDist[0]) > 1) :
            
            x, y = trouverDistMin(matDist)
            node = Cl_AB()
            node.fusionAb(ab[x],ab[y],float(matDist[x][y])/float(2))
            node.id = ab[x].id + ', ' + ab[y].id


            calculMatrice(x,y,matDist,node)
            ab =  swap_ab(node,ab,x,y)
            
            return(self.UPGMA(matDist,ab))
        else :
            return ab[0]
        
    def newick(self): 
        p = ''
        if not self.estFeuille() :
            p += '('+ self.G.newick() + ":" + str(self.distG) + ','
            p +=  self.D.newick() + ":" + str(self.distD) + ')'
        else :
            p += self.id
        return(p)
        
H = [[0,0.092,0.106,0.177,0.207],
     [0.092,0,0.111,0.193,0.218],
     [0.106,0.111,0,0.188,0.218], 
     [0.177,0.193,0.188,0,0.219],
     [0.207,0.218,0.218,0.219,0]]

A1 = Cl_AB()
A2 = Cl_AB()
A3 = Cl_AB()
A4 = Cl_AB()
A5 = Cl_AB()

A1.id = "Homme"
A2.id = "Chimpanze"
A3.id = "Gorille"
A4.id = "Orang-outan"
A5.id = "Gibbon"

A = [A1,A2,A3,A4,A5]

P = Cl_AB()

P = P.UPGMA(H,A)
print(P.__dict__)
print(P.newick())