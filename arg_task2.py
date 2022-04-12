import argparse
import sys
parser = argparse.ArgumentParser("\nLR1 grammar parser by yuangyan\nCourseworkwork for semester2, 2022\n")
parser.add_argument("--showParsing", action="store_true",
                    help="show Parsing Process")
parser.add_argument("-i", "--input", type=str,
                    help="input file name, 'lex_parsed.txt' by default", metavar='')
parser.add_argument("-r", "--rule", type=str,
                    help="rule file name, 'grammar_rule.txt' by default", metavar='')
parser.add_argument("-o", "--output", type=str,
                    help="output file name, '<input file name>_LR1.txt' by default", metavar='')
args = parser.parse_args()

inputstr = "lex_parsed.txt"
outputstr = "lex_parsed_LR1.txt"
rulestr = 'grammar_rule.txt'
inputlist = list()
G = dict()
isVN = set()
filter = dict()
indextable = dict()
lexlist = list()

if args.input :
    inputstr = args.input
dotpos = inputstr.find('.')

if dotpos != -1 :
    outputstr = inputstr[:dotpos] + "_LR1.txt"
else:
    outputstr = inputstr + "_LR1.txt"

if args.output :
    outputstr = args.output
if args.rule :
    rulestr = args.rule


with open(rulestr, 'r', encoding='utf-8') as f:
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

with open(inputstr, 'r', encoding='utf-8') as f:
    linecount = 1
    for line in f.readlines():
        row = line.split()
        currentline = int(row[0])

        if currentline > linecount :
            linecount = currentline
        row = line.split()
        if filter.get(row[1]) != None :
            indextable[len(inputlist)] = currentline
            inputlist.append(filter[row[1]])
            lexlist.append(row[2])
        
        else :
            if row[1] != 'invalid_syntax' :
                indextable[len(inputlist)] = currentline
                inputlist.append(row[2])
                lexlist.append(row[2])
            else:
                print('\033[1;31m')
                print('error')
                print('in line' + str(currentline) + ': ' + row[2] + '\ninvalid syntax')
                print('\033[0m')
                sys.exit()


def printerror(index) :
    frontstr = str()
    backstr = str()
    indexline = indextable[index]
    total = 0

    with open(inputstr, 'r', encoding='utf-8') as f:
        for line in f.readlines():
            
            row = line.split()
            currentline = int(row[0])
            if currentline == indexline :
                if total < index :
                    frontstr += row[2]
                else:
                    backstr += row[2]
            if currentline > indexline :
                break

            total += 1
    print('in line ' + str(index) +': ' + frontstr + backstr)
    print(len('in line ' + str(index) +': ' + frontstr) * ' ' + '^')
    print('invalid syntax: ' + lexlist[index])


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
            printerror(i)
            return 'error'

        if nextmove[0] == 1 :

            statstack.append(nextmove[1])
            synstack.append(s[i])
            parsingstack.append((prevstatstack, prevsynstack, s[i:], 'S' + str(nextmove[1])))
            if args.showParsing :
                print((prevstatstack, prevsynstack, s[i:], 'S' + str(nextmove[1])))
            i += 1
            continue

        if nextmove[0] == 0 :
            if nextmove[1] == 'acc' :
                if args.showParsing :
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
                printerror(i)
                
                return 'error'

            if tobematched == list(rule) :
                
                synstack = synstack[: -rulelen]
                statstack = statstack[: -rulelen]
                nextstat = table.get((statstack[-1], chartobeinserted))
            
                if nextstat == None :
                    print('error')
                    printerror(i)
                    return 'error'  
                statstack.append(nextstat[1])
                synstack.append(chartobeinserted)

                easylookingproduction = '<' + chartobeinserted + '> → '
                
                for item in rule :
                    if len(item) > 1 :
                        easylookingproduction += '<' + item + '>'
                    else:
                        easylookingproduction += '<' + item + '>'
                parsingstack.append((prevstatstack, prevsynstack, s[i:], 'r: ' + easylookingproduction))
                if args.showParsing :
                    print((prevstatstack, prevsynstack, s[i:], 'r: ' + easylookingproduction))
    print('error')
    printerror(i)         
    return 'error'

issuccess = LR1(inputlist)
outputstack = list()
maxlen = [0, 0, 0, 0]
for item in parsingstack :
    
    outputstr0 = ''
    outputstr1 = ''
    outputstr2 = ''
    outputstr3 = ''
    for i in range(len(item[0])) :
        outputstr0 += str(item[0][i])
        if i < len(item[0]) - 1 :
            outputstr0 += ','
        if len(outputstr0) > maxlen[0] :
            maxlen[0] = len(outputstr0)

    for syn in item[1] :
        outputstr1 += '<' + syn + '>'
        if len(outputstr1) > maxlen[1] :
            maxlen[1] = len(outputstr1)

    for syn in item[2] :
        outputstr2 += '<' + syn + '>'
        if len(outputstr2) > maxlen[2] :
            maxlen[2] = len(outputstr2)

    for syn in item[3] :
        outputstr3 += syn
        if len(outputstr3) > maxlen[3] :
            maxlen[3] = len(outputstr3)

    outputstack.append((outputstr0, outputstr1, outputstr2, outputstr3))

with open(outputstr, 'w', encoding='utf-8') as f:
    for item in outputstack :
        for i in range(4) :
            f.write(item[i] + (maxlen[i] - len(item[i]) + 4) * ' ')
        #     print(item[i] + '   ', end='')
        # print('\n' ,end='')
        f.write('\n')
    f.write(issuccess)
            