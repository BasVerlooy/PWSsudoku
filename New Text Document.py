Sgrid =  [[10,2,6,5,7,1,4,8,3],
          [3,5,1,4,8,6,2,7,9],
          [8,7,4,9,2,3,5,1,6],
          [5,8,2,3,6,7,1,9,4],
          [1,4,9,2,5,8,3,6,7],
          [7,6,3,1,4,9,8,2,5],
          [2,3,8,7,0,4,6,5,1],
          [6,1,7,8,3,5,9,4,2],
          [4,9,5,6,1,2,7,3,8]]
keer = 0
         
#in rij en kolom mogelijk
def rijkolom(i,Sgrid,x,y,mogelijk):
    for rijkolom in range(0,len(Sgrid)):
        #de plek is/ was nul, dus hij kijkt ook naar zijn eigen vakje
        if mogelijk == False:
            if Sgrid[x][rijkolom] == i:
                return False
            elif Sgrid[rijkolom][y] == i:
                return False
        #de plek heeft een waarde, dus hij kijkt niet naar zijn eigen vakje
        else:
            if Sgrid[x][rijkolom] == i and rijkolom != y:
                return False
            elif Sgrid[rijkolom][y] == i and rijkolom != x:
                return False
    return True
#de plek van de 3x3 blok
def blokplekx(x):
    k = 0
    if x >= 0 and x <= 2:
        k = 0
    elif x >= 3 and x <= 5:
        k = 3
    else:
        k = 6
    return k
def blokpleky(y):
    l = 0
    if y >= 0 and y <= 2:
        l = 0
    elif y >= 3 and y <= 5:
        l = 3
    else:
        l = 6
    return l
#in 3x3 blok mogelijk
def blok(i,Sgrid,x,y,mogelijk):
    k = blokplekx(x)
    l = blokpleky(y)
    for m in range (k, k + 3):
        for n in range (l, l + 3):
            if mogelijk == False:
                if Sgrid[m][n] == i:
                    return False
            else:
                if Sgrid[m][n] == i and m != x and n != y:
                    return False
    return True
	
#Zoektocht naar mogelijke getallen
def possibleList(Sgrid,x,y):
    #alle getallen in een lijst
    isMogelijkList = [[0,1],[1,0],[2,0],[3,0],[4,0],[5,0],[6,0],[7,0],[8,0],[9,0]]
    #getallen niet mogelijk in rij en kolom
    for i in range (0, len(Sgrid)):
        if Sgrid[x][i] != 0:
            isMogelijkList[Sgrid[x][i]][1] = 1
        if Sgrid[i][y] != 0:
            isMogelijkList[Sgrid[i][y]][1] = 1
    
    #getallen niet mogelijk in 3x3 blok
    k = blokplekx(x)
    l = blokpleky(y)
    for m in range (k, k + 3):
        for n in range (l, l + 3):
            if Sgrid[m][n] != 0:
                isMogelijkList[Sgrid[m][n]][1] = 1
    #mogelijke getallen in een lijst
    mogelijkList = []
    for i in range (0, len(isMogelijkList)):
        if isMogelijkList[i][1] == 0:
            mogelijkList.append(i)
    return mogelijkList
#Zoektocht naar een lijst van "lege" vakken
def emptyList():
    leegList=  []
    for x in range (0, len(Sgrid)):
        for y in range (0, len(Sgrid)):
            if Sgrid[x][y] == 0:
                mogelijk = False
                mogelijkList = possibleList(Sgrid,x,y)
                leegList.append(list((x,y,0,mogelijkList)))
            elif Sgrid[x][y] > 9:
                print('getal in rij ' + str(x + 1) + ' en in kolom ' + str(y + 1)  + ' is groter dan 9')
                return False
            else:
                mogelijk = True
                if rijkolom(Sgrid[x][y],Sgrid,x,y,mogelijk) == False:
                    return False
                elif blok(Sgrid[x][y],Sgrid,x,y,mogelijk) == False:
                    return False
    return leegList
    
#Mogelijke getallen invullen
def invul(i,Sgrid,x,y,leegList):
    if Sgrid[x][y] != 0:
        for o in range (0, len(leegList[i][3])):
            if leegList[i][3][o] == Sgrid[x][y]:
                o += 1
                break
    else:
        o = 0
    mogelijk = False
    for j in range (o, len(leegList[i][3])+1):
            if j ==  len(leegList[i][3]):
                return False
            elif rijkolom(leegList[i][3][j],Sgrid,x,y,mogelijk) == False:
                continue
            elif blok(leegList[i][3][j],Sgrid,x,y,mogelijk) == False:
                continue
            else:
                leegList[i][2] = j
                return leegList[i][3][j]
#Mogelijklijst invullen
def leeg(Sgrid,keer):
    leegList = emptyList()
    if leegList == False:
        print('onoplosbaar')
    elif len(leegList) == 0:
        print('het is al compleet')
    else:
        i = 0
        while True:
            #checken of de laatste een waarde heeft
            if Sgrid[leegList[len(leegList)-1][0]][leegList[len(leegList)-1][1]] != 0:
                keer += 1
                i -= 1
                if keer == 1:
                    #de eerste oplossing
                    print(Sgrid)
                elif keer == 2:
                    if len(emptyList()) == 0:
                        print('maar er zijn meerdere oplossingen')
                        break
                    else:
                        break
                #alsof de eerste oplossing niet goed is
                    #dus kijken of er meerdere oplossingen zijn
                x = leegList[i][0]
                y = leegList[i][1]
                i -= 1
                Sgrid[x][y] = 0
                        
            while i < len(leegList):            
                x = leegList[i][0]
                y = leegList[i][1]
                getal = invul(i,Sgrid,x,y,leegList)
        
                #getal niet mogelijk, dus naar terug vorige vak
                if getal == False:
                    i -= 1
                    Sgrid[x][y] = 0
                    break
                #getal mogelijk
                else:
                    Sgrid[x][y] = getal
                    i += 1
#uitvoering
leeg(Sgrid,keer)
