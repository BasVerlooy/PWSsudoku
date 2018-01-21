from random import randint
#in rij en kolom mogelijk
def rijkolom(i,Sgrid,x,y,mogelijk):
    for rijkolom in range(0,9):
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
#in 3x3 blok mogelijk
def blok(i,Sgrid,x,y,mogelijk):
    k = (x // 3) * 3
    l = (y // 3) * 3
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
    for i in range (1, 10):
        #getallen niet mogelijk in rij en kolom
        if rijkolom(i,Sgrid,x,y,True) == False:
            isMogelijkList[i][1] = 1
        elif blok(i,Sgrid,x,y,True) == False:
            isMogelijkList[i][1] = 1
    #mogelijke getallen in een lijst
    mogelijkList = []
    for i in range (0, len(isMogelijkList)):
        if isMogelijkList[i][1] == 0:
            mogelijkList.append(i)
    return mogelijkList
#Zoektocht naar een lijst van "lege" vakken
def emptyList(Sgrid):
    leegList=  []
    for x in range (0, 9):
        for y in range (0, 9):
            if Sgrid[x][y] == 0:
                mogelijk = False
                mogelijkList = possibleList(Sgrid,x,y)
                leegList.append(list((x,y,0,mogelijkList)))
            else:
                mogelijk = True
                if rijkolom(Sgrid[x][y],Sgrid,x,y,mogelijk) == False:
                    return False
                elif blok(Sgrid[x][y],Sgrid,x,y,mogelijk) == False:
                    return False
    return leegList
#Mogelijke getallen invullen
def invul(i,Sgrid,x,y,leegList):
    o = 0
    #als er een getal is ingevuld
    if Sgrid[x][y] != 0:
        
        #hoeveelste waarde van mogelijklist is ingevuld
        for o in range (0, len(leegList[i][3])):
            if leegList[i][3][o] == Sgrid[x][y]:
                o += 1
                break
    #zijn eigen waarde is niet mogelijk
    mogelijk = False
    
    #welke kleinst mogelijk getal is mogelijk?
    for j in range (o, len(leegList[i][3])+1):
            #alle mogelijkheden zijn geprobeerd
            if j ==  len(leegList[i][3]):
                return False
            #in rij/kolom mogelijk?
            elif rijkolom(leegList[i][3][j],Sgrid,x,y,mogelijk) == False:
                continue
            #in 3x3 blok mogelijk?
            elif blok(leegList[i][3][j],Sgrid,x,y,mogelijk) == False:
                continue
            #mogelijk!
            else:
                leegList[i][2] = j
                return leegList[i][3][j]
#oplosser
def leeg(Sgrid,leegList,eerste,ekeren):
    #hoeveel keer opgelost
    keer = 0
    #alle lege plekken met mogelijke getallen om in te vullen
    leegList = emptyList(Sgrid)
    #het is onoplosbaar
    if leegList == False:
        return False
    #er moeten getallen ingevuld worden
    else:
        i = 0
        while True:
            
            #checken of de laatste een waarde heeft
            if Sgrid[leegList[len(leegList)-1][0]][leegList[len(leegList)-1][1]] != 0:
                keer += 1
                i -= 1
                
                #de eerste oplossing
                if keer == 1:
                    #????Soms hebben oplossingen nog steeds lege plekken???
                    if len(emptyList(Sgrid)) != 0:
                        return False
                    #het is vol
                    else:
                        if eerste == True:
                            if ekeren == 14:
                                return Sgrid
                            else:
                                return True
                #het is voor de tweede keer opgelost
                else:
                    if len(emptyList(Sgrid)) == 0:
                        return False
                
                #kijken of er meerdere oplossingen zijn
                x = leegList[i][0]
                y = leegList[i][1]
                i -= 1
                Sgrid[x][y] = 0
            elif keer >=1 and Sgrid[leegList[0][0]][leegList[0][1]] == 0:
                return True
            
            #kijken of het getal mogelijk is            
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
#Sgrid kopiëren
def Sudokugrid(leegSgrid):
    Sgrid = []
    for i in range (0, len(leegSgrid)):
        grid = [] + leegSgrid[i]
        Sgrid.insert(i,grid)
    return Sgrid
#begin getallen invoegen
def begin(leegSgrid,ekeren):
    leegList = emptyList(leegSgrid)
    
    #kiezen welke plek gekozen worden
    plek = randint(0,len(leegList)-1)
    
    #de plek in de sudoku
    rij = leegList[plek][0]
    kolom = leegList[plek][1]
    
    #waarde van die plek
    waarde = leegList[plek][3][randint(0,len(leegList[plek][3])-1)]
    
    #waarde invullen
    leegSgrid[rij][kolom] = waarde
    Sgrid = Sudokugrid(leegSgrid)
    return leeg(Sgrid,leegList,True,ekeren)
def genereer(begingetal):
    leegSgrid =  [[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0]]
    for ekeren in range (0,begingetal):
        goed = begin(leegSgrid,ekeren)
        while goed == False:
            goed = begin(leegSgrid,ekeren)
        if ekeren == begingetal-1:
            return goed
def weghalen(nummers,begingetal,volSgrid):
    #plek bepalen om weg te halen
    rij = randint(0,len(volSgrid)-1)
    kolom = randint(0,len(volSgrid)-1)
    #waarde onthouden om het zo nodig terug te plaatsen
    waarde = volSgrid[rij][kolom]
    #plek weghalen
    volSgrid[rij][kolom] = 0
    Sgrid = Sudokugrid(volSgrid)
    goed = leeg(Sgrid,emptyList(Sgrid),False,False)
    return [goed,rij,kolom,waarde]
def legen(nummers):
    global oplossing
    #aantal getallen om te generern
    begingetal = 15
    volSgrid = genereer(begingetal)
    oplossing = Sudokugrid(volSgrid)
    #getallen weghalen tot "nummers"
    for i in range (0,nummers):
        goed = weghalen(nummers,begingetal,volSgrid)
        #als de sudoku niet oplosbaar is, terugplaatsen en andere weghalen
        while goed[0] == False:
            volSgrid[goed[1]][goed[2]] = goed[3]
            goed = weghalen(nummers,begingetal,volSgrid)
    return volSgrid
def moeilijkheid(niveau):
    if niveau == "makkelijk": 
        nummers = 40
    elif niveau == "normaal": 
        nummers = 60
    elif niveau == "moeilijk":
        nummers = 80
    else:
        return False
    return legen(nummers)
niveau = "moeilijk"
oplossing = []
print('sudoku oefening: ' + str(moeilijkheid(niveau)))
print('sudoku oplossing: ' + str(oplossing))
