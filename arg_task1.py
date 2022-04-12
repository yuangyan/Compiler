import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--showDFA", action="store_true",
                    help="show DFA coverted from input NFA")
parser.add_argument("-i", "--input", type=str,
                    help="input file name, 'lex.txt' by default")
parser.add_argument("-r", "--rule", type=str,
                    help="rule file name, 'lex_rule.txt' by default")
parser.add_argument("-o", "--output", type=str,
                    help="output file name, '<input file name>_parsed.txt' by default")
args = parser.parse_args()


inputstr = "lex.txt"
outputstr = "lex_parsed.txt"
rulestr = 'lex_rule.txt'
NFA = dict()
DFAType = set()
Keyword = set()
AssignmentOperator = set()
BinaryOperator = set()
UnaryOperator = set()
Delimiter = set()
Expressionrule = dict()

if args.input :
    inputstr = args.input
dotpos = inputstr.find('.')

if dotpos != -1 :
    outputstr = inputstr[:dotpos] + "_parsed.txt"
else:
    outputstr = inputstr + "parsed.txt"

if args.output :
    outputstr = args.output
if args.rule :
    rulestr = args.rule

with open(rulestr, 'r', encoding='utf-8') as f:
    for line in f.readlines():
        line = line.strip('\n')
        row = line.split()
        if row[0] == 'NFA' :
            index = 3
            production = set()
            while index < len(row) :
                production.add(row[index])
                index += 1
            NFA[(row[1], row[2])] = production
            continue

        if row[0] == 'Expressionrule' :
            index = 3
            production = set()
            while index < len(row) :
                production.add(row[index])
                index += 1
            Expressionrule[(row[1], row[2])] = production
            continue

        if row[0] == 'DFAType' :
            DFAType.add(row[1])
            continue

        if row[0] == 'Keyword' :
            Keyword.add(row[1])
            continue

        if row[0] == 'AssignmentOperator' :
            AssignmentOperator.add(row[1])
            continue

        if row[0] == 'BinaryOperator' :
            BinaryOperator.add(row[1])
            continue

        if row[0] == 'UnaryOperator' :
            UnaryOperator.add(row[1])
            continue

        if row[0] == 'Delimiter' :
            Delimiter.add(row[1])
            continue

def sorttuple(tup) :
    l = list(tup)
    l.sort()
    return tuple(l)


def typeof(ch) :
    if ch == '+' or ch == '-' :
        return '+/-'
    if ch == 'e' or ch == 'E' :
        return 'e/E'
    if '0' < ch <= '9' :
        return 'd+'
    if ch == 'i' :
        return ch
    if ('a' <= ch <= 'z') or ('A' <= ch <= 'Z') :
        return 'char'
    return ch

def closure(NFA, depts) :
    target = set()
    for i in depts :
        target.add(i)
    while((not depts) == False) :
        dept = depts.pop()
        dests = NFA.get((dept, 'ε'))
        if dests != None :
            for dest in dests :
                if (dest in target) == False :
                    depts.append(dest)
                    target.add(dest)
    return target

def NFA2DFA(NFA) :
    DFA = {}
    edges = set([])
    statset = set([])
    unsolvedstatsets = []
    existingstatsets = []
    
    start = closure(NFA, ['S'])
    statset = start

    existingstatsets.append(statset)
    unsolvedstatsets.append(statset)  

    for key in NFA.keys() :
        if key[1] != 'ε' :
            edges.add(key[1])

    while((not unsolvedstatsets) == False) :
        statset = unsolvedstatsets.pop()
        for edge in edges :
            movestatset = set([])
            newstatset = set([])
            for stat in statset :
                if NFA.get((stat, edge)) != None :
                    for item in NFA.get((stat, edge)) :
                        movestatset.add(item)

            remainingstatlist = []
            for item in movestatset :
                remainingstatlist.append(item)
            newstatset = closure(NFA, remainingstatlist)
            if (not newstatset) == False :
                DFA[(sorttuple(tuple(statset)), edge)] = newstatset
                if (newstatset in existingstatsets) == False :
                    existingstatsets.append(newstatset)
                    unsolvedstatsets.append(newstatset)   

    namedict = {sorttuple(tuple(start)): 0}
    id = 1
    for item in existingstatsets :
        if item != start :
            namedict[sorttuple(tuple(item))] = id
            id += 1
    
    newDFA = dict()


    for key in DFA.keys() :
        newname = namedict[key[0]]
        targetname = namedict[sorttuple(tuple(DFA[key]))]
        newDFA[(newname, key[1])] = targetname

    return newDFA, namedict

DFA, namedict = NFA2DFA(NFA)
reversednamedict = {v:k for k,v in namedict.items()}

if args.showDFA :
    print('DFA:')
    for key, value in DFA.items() :
        arrowstr = str(key[0]) + '---' + str(key[1]) + '--->' + str(value)
        type = reversednamedict[value]
        for item in type :
            if (item in DFAType) == True :
                arrowstr += '   (' + item + ')'
        print(arrowstr)



def Parse(DFA, s) :
    if s == 'i' :
        return 'IDENTIFIER'
    if s in Keyword :
        return 'KEYWORD'
    if s in AssignmentOperator :
        return 'ASSIGNMENT_OPERATOR'
    if s in BinaryOperator :
        return 'BINARY_OPERATOR'
    if s in UnaryOperator :
        return 'UNARY_OPERATOR'
    if s in Delimiter :
        return 'DELIMITER'

    stat = 0
    for i in range(len(s)) :
        nextstat = DFA.get((stat, typeof(s[i])))
        if nextstat != None :
            stat = nextstat
        else :
            return 'invalid syntax'

    type = reversednamedict[stat]
    for item in type :
        if (item in DFAType) == True :
            return item
    return 'invalid syntax'



ExprDFA, Exprnamedict = NFA2DFA(Expressionrule)
Exprreversednamedict = {v:k for k,v in Exprnamedict.items()}

def ParseExpr(DFA, l) :
    stat = 0
    for i in range(len(l)) :
        nextstat = DFA.get((stat, l[i]))
        if nextstat != None :
            stat = nextstat
        else :
            return 'invalid'
    return 'valid'



# read file to be analyzed
input = list()

with open(inputstr, 'r', encoding='utf-8') as f:
    linecount = 1
    for line in f.readlines():
        line = line.strip('\n')
        row = line.split()
        for item in row :
            input.append((linecount, str(item)))
        linecount += 1


output = list()
for item in input :

    components = list()
    typelist = list()
    # 最长匹配
    isinvalid = False
    parsingstr = item[1]
    while(parsingstr != ''):
        longestmatch = 0
        for i in range(len(parsingstr)) :
            if Parse(DFA, parsingstr[:i+1]) != 'invalid syntax' :
                longestmatch = i + 1
        
        if longestmatch == 0 :
            isinvalid = True
            break   
        # 检查只有固定的几种可以拼接（没有空格）
        parsedtype = Parse(DFA, parsingstr[:longestmatch])
        components.append((parsingstr[:longestmatch], parsedtype))
        if (parsedtype in {'INT', 'DOUBLE', 'COMPLEX'}) == True :
            typelist.append('datatype')

        elif parsedtype == 'IDENTIFIER' :
            typelist.append('identifier')

        elif parsedtype == 'ASSIGNMENT_OPERATOR' :
            typelist.append('assignment_operator')
        
        elif parsedtype == 'BINARY_OPERATOR' :
            typelist.append('binary_operator')
        
        elif parsedtype == 'UNARY_OPERATOR' :
            typelist.append('unary_operator')
        
        
        elif parsedtype == 'KEYWORD' :
            typelist.append('keyword')

        elif parsedtype == 'DELIMITER' :
            typelist.append('delimiter')
        
        else :
            typelist.append('other type')

        parsingstr = parsingstr[longestmatch:]
    
    if isinvalid == True :
        output.append((item[0], 'invalid_syntax', item[1]))

    else :
        if len(components) < -1 :
            if ParseExpr(ExprDFA, typelist) == 'invalid' :
                output.append((item[0], 'invalid_syntax', item[1]))
                continue

        for pairs in components :
                output.append((item[0], pairs[1], pairs[0]))

with open(outputstr, 'w', encoding='utf-8') as f:
    for item in output :
        f.write(str(item[0]) + ' ' + item[1] + ' ' + item[2] + '\n')