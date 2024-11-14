# Zac Hays

# negate a literal
def negate(lit):
    if lit[0] == '~':
        return lit[1:]
    return '~' + lit

# negate the clause. this returns a list of literals which are implied to be connected by ANDs
# since all inputs will be initially connected by ORs due to how the problem is set up
def negateClause(clause):
    negated = []
    for lit in clause:
        negated.append(negate(lit))
    return negated

# checks if two clauses are logically equivalent
def areSame(clause1, clause2):
    forward = max(len(clause1), len(clause2))
    for lit1 in clause1:
        for lit2 in clause2:
            if lit1 == lit2: forward -= 1
    # if the number of equivalent literals = the total number of literals, then it's all equivalent!
    if forward == 0: return True

# checks if the clause is redundant with respect to the kb
def isRedundant(kb, clause):
    for clause2 in kb:
        if areSame(clause, clause2):
            return True
    return False

# checks if the clause evaluates to True by checking for cases of "x or ~x"
def isTrue(clause):
    for lit in clause:
        if negate(lit) in clause:
            return True
    return False

# resolve clause1 using clause2. 
def resolve(clause1, clause2):
    resolved = []
    for lit1 in clause1:
        # if the negative of lit1 is in clause2, replace it with the rest of clause2
        if negate(lit1) in clause2:
            for lit2 in clause2:
                if lit2 != negate(lit1) and lit2 not in resolved: # don't add redundant literals
                    resolved.append(lit2)
        elif lit1 not in resolved: # don't add redundant literals
            resolved.append(lit1)
        # after each step, check if the overall clause (what we know + what we've learned) evaluates to true
        # if it does, stop.
        if isTrue(clause1 + resolved):
            return clause1 # i'm just going to return clause1 in this case since I know it won't get added to the kb
    return resolved

# i feel like this is self explanatory
def clauseToString(clause):
    string = ""
    for lit in clause:
        string += lit + " "
    return string

# finally we can use my beautiful cohesive functions to do the proof
def prove(kb):
    valid = False
    # first, let's print the kb so far
    for num in range(len(kb)):
        print("%d. %s{}" % (num + 1, clauseToString(kb[num])))
    # now start resolving
    i = 0
    while (i < len(kb) - 1):
        if valid: break
        i += 1
        for j in range(i):
            resolved = resolve(kb[i], kb[j])
            # if it's an empty clause, add Contradiction to the knowledge base and stop; it's valid!
            if not resolved:
                kb.append("Contradiction")
                print("%d. Contradiction {%d,%d}" % (len(kb), i + 1, j + 1))
                valid = True
                break
            # otherwise, if it's not redundant and it doesn't evaluate to true, add it to the knowledge base
            if (not isRedundant(kb, resolved)) and (not isTrue(resolved)):
                kb.append(resolved)
                print("%d. %s{%d,%d}" % (len(kb), clauseToString(resolved), i + 1, j + 1))
    # now the loop is over. we either found a contradiction or exhausted all possible resolutions
    if valid: print("Valid")
    else: print("Fail")