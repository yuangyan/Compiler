G = dict()
isVN = set()
filter = dict()
# read grammar
with open('grammar_rule.txt', 'r', encoding='utf-8') as f:
    for line in f.readlines():
        line = line.strip('\n')
        row = line.split()
        if row[0] == 'G' :
            left = row[1]
            index = 2
            production = list()
            while(index < len(row)) :
                production.append(row[index])
                index += 1
            if G.get(left) != None :
                G.get(left).add(tuple(production))
            else:
                G[left] = set()
                G[left].add(tuple(production))
        
        if row[0] == 'isVN' :
            isVN.add(row[1])

        if row[0] == 'filter' :
            filter[row[1]] = row[2]


inputlist = list()
with open('lex_parsed.txt', 'r', encoding='utf-8') as f:
    linecount = 1
    for line in f.readlines():
        row = line.split()
        currentline = int(row[0])
        if currentline > linecount :
            # inputlist.append('`endl')
            linecount = currentline
        row = line.split()
        if filter.get(row[1]) != None :
            inputlist.append(filter[row[1]])
        else :
            if row[1] != 'invalid_syntax' :
                inputlist.append(row[2])
            # invalid syntax类型




def sortanddeduplicate(l) :
    lset = set(l)
    llist = list(lset)
    llist.sort()
    return tuple(llist)

def checkcanbevoid(G) :
    canbevoid = dict()
    for key, value in G.items() :
        canbevoid[key] = False

        for s in value :
            if s == ('',) :
                canbevoid[key] = True
                break

    haschanged = 1
    while(haschanged != 0) :
        haschanged = 0
        for key, value in G.items() :
            originalval = canbevoid[key]
            
            void = True
            for s in value :         
                for ch in s :
                    if canbevoid.get(ch) != True :
                        void = False
                        
                if void == True :
                    canbevoid[key] = True
                    if originalval == False :                  
                        haschanged = 1           

    return canbevoid

def Firstset(G) :
    canbevoid = checkcanbevoid(G)
    FirstG = dict()
    
    for key in G.keys() :
        FirstG[key] = set()
    while(True) :
        hasextended= False
        for key, value in G.items() :
            sizebefore = len(FirstG[key])
            for s in value :
                isended = True
                for ch in s :
                    if canbevoid.get(ch) == True :
                        FirstG[key] = FirstG[key] | (FirstG[ch] - {''})
                    else :
                        if canbevoid.get(ch) == False :
                            FirstG[key] = FirstG[key] | FirstG[ch]
                        elif (ch in isVN) == False :
                            FirstG[key] = FirstG[key] | {ch}
                        isended = False
                        break
                if isended == True :
                    FirstG[key] = FirstG[key] | {''}
            sizeafter = len(FirstG[key])
            if sizeafter > sizebefore :
                hasextended = True

        if hasextended == False :
            break

    return FirstG

def SFirstset(s) :
    firstG = Firstset(G)
    if s == tuple() :

        return {''}
    
    firstset = set()
    canbevoid = checkcanbevoid(G)
    for ch in s :
        if (ch in isVN) == False :
            firstset.add(ch)
            break
        firstset = firstset | firstG[ch]
        if canbevoid[ch] == False :
            break
    
    return firstset

def Formstat(rawstat) :
    unextendedstat = list(rawstat)
    statset = set(rawstat)
    while((not unextendedstat) == False) :
        item = unextendedstat.pop()
        if len(item[2]) > 0 :
            ch = (item[2])[0]
            if ch in isVN :         
                firsts = SFirstset((item[2])[1:])
                # modified
                if firsts == {''} :
                    firsts = item[3]
                next = sortanddeduplicate(firsts)

                for production in G[ch] :
                    newtup = ((ch,), tuple(), production, next)
                    if (newtup in statset) == False:
                        unextendedstat.append(newtup)
                        statset.add(newtup)
    statlist = list(statset)
    statlist.sort()

    newstatlist = list()
    firstrepeated = 0
    mergefirst = []
    i = 0
    while(i <= len(statlist)) :
        if i < len(statlist) :
            if (statlist[i])[:3] == (statlist[firstrepeated])[:3] :
                mergefirst.extend(list((statlist[i])[3]))
                i += 1
            else :
                mergefirst = sortanddeduplicate(mergefirst)
                newstatlist.append(((statlist[i-1])[0], (statlist[i-1])[1], (statlist[i-1])[2], tuple(mergefirst)))
                firstrepeated = i
                mergefirst = []
        else :
            newstatlist.append(((statlist[i-1])[0], (statlist[i-1])[1], (statlist[i-1])[2], tuple(mergefirst)))
            i += 1

    return tuple(newstatlist)

rawstat = [(("S'",), tuple(), ('S',), ('#',))]
statset = Formstat(rawstat)

def DFA(G) :
    rawstat = [(("S'",), tuple(), ('S',), ('#',))]
    statset = Formstat(rawstat)
    dfa = dict()

    unsolvedstats = list()
    allstats = list()
    allstats.append(statset)
    unsolvedstats.append(statset)
    while ((not unsolvedstats) == False) :
        stat2besolved = unsolvedstats.pop()
        tempdict = dict()
        for production in stat2besolved :
            
            if production[2] != tuple() :
                moveto = (production[2])[0]
                if tempdict.get(moveto) == None :
                    tempdict[moveto] = set()

                newprod = list(production[1])
                newprod.append(moveto)
                front = tuple(newprod)
                back = (production[2])[1:]
                tempdict[moveto].add((production[0], front, back, production[3]))

        for key in tempdict.keys() :
            rawstat = tempdict[key]
            newstat = Formstat(rawstat)
            # prevent back edge
            if (newstat in allstats) == False :
                allstats.append(newstat)
                unsolvedstats.append(newstat)
            dfa[(stat2besolved, key)]= newstat

    namedict = dict()
    id = 0
    for stat in allstats :
        namedict[stat] = id
        id += 1

    newdfa = dict()
    for key, value in dfa.items() :
        newdfa[(namedict[key[0]], key[1])] = namedict[value]

    return newdfa, dfa, namedict

def easyset(statset) :
    easy = list()
    for item in statset :
        s = '' + ''.join(item[0]) + '→' + ''.join(item[1]) + '·' + ''.join(item[2]) + ', ' + ''.join(item[3])
        easy.append(s)
    return tuple(easy)

def easydict(goto) :
    easy = dict()
    for key in goto.keys() :
        easy[(easyset(key[0]), key[1])] = easyset(goto[key])
    return easy

newdfa, dfa, namedict = DFA(G)

reversednamedict = {v:k for k,v in namedict.items()}

def LR1table(dfa: dict) :
    table = dict()
    allstat = set()

    for key, value in dfa.items() :
        allstat.add(key[0])
        allstat.add(value)
        if table.get(key) != None :
            pass
        table[key] = (1, value)

    for stat in allstat :
        realstat = reversednamedict[stat]
        for i in range(len(realstat)) :
            production = realstat[i]
            if production == (("S'",), ('S',), tuple(), ('#',)) :
                if table.get((stat, '#')) != None :
                    pass
                
                table[(stat, '#')] = (0, 'acc')
                break

            if production[2] == tuple() :
                for ch in production[3] :
                    if table.get((stat, ch)) != None :
                        pass
                    table[(stat, ch)] = (0, i)

    return table


parsingstack = list()
def LR1(s: list) :
    table = LR1table(newdfa)
    s.append('#')
    statstack = [0]
    synstack = ['#',]
    i = 0
    while(i < len(s)) :

        prevstatstack = statstack.copy()
        prevsynstack = synstack.copy()

        nextmove = table.get((statstack[-1], s[i]))
        if nextmove == None :
            print('error')
            return 'error'

        if nextmove[0] == 1 :

            statstack.append(nextmove[1])
            synstack.append(s[i])
            parsingstack.append((prevstatstack, prevsynstack, s[i:], 'S' + str(nextmove[1])))

            print((prevstatstack, prevsynstack, s[i:], 'S' + str(nextmove[1])))
            i += 1
            continue

        if nextmove[0] == 0 :
            if nextmove[1] == 'acc' :
                print((prevstatstack, prevsynstack, s[i:], 'r: S\'→S'))
                parsingstack.append((prevstatstack, prevsynstack, s[i:], 'r: S\'→S'))
                print('accepted')
                return 'accepted'
            realstat = reversednamedict[statstack[-1]]
            production = realstat[nextmove[1]]
            rule = production[1]
            chartobeinserted = (production[0])[0]
            rulelen = len(rule)
            

            tobematched = synstack[-rulelen: ]

            # index out of range
            if rulelen > len(tobematched) :
                print('error')
                return 'error'

            if tobematched == list(rule) :
                
                synstack = synstack[: -rulelen]
                statstack = statstack[: -rulelen]
                nextstat = table.get((statstack[-1], chartobeinserted))
            
                if nextstat == None :
                    print('error')
                    return 'error'  
                statstack.append(nextstat[1])
                synstack.append(chartobeinserted)

                easylookingproduction = '<' + chartobeinserted.strip('`') + '> → '
                
                for item in rule :
                    if len(item) > 1 :
                        easylookingproduction += '<' + item.strip('`') + '>'
                    else:
                        easylookingproduction += '<' + item.strip('`') + '>'
                parsingstack.append((prevstatstack, prevsynstack, s[i:], 'r: ' + easylookingproduction))
                print((prevstatstack, prevsynstack, s[i:], 'r: ' + easylookingproduction))
    print('error')            
    return 'error'

issuccess = LR1(inputlist)

with open('grammar_parsed.txt', 'w', encoding='utf-8') as f:
    for item in parsingstack :
        for i in item[0] :
            f.write(str(i))
            f.write(',')
        f.write('------')

        for i in item[1] :
            f.write(str(i))
        f.write('------')

        for i in item[2] :
            f.write(i)
        f.write('------')

        f.write(item[3])
        f.write('\n')
    f.write(issuccess)
        