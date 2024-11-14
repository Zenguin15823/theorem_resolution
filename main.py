import sys
import resolver

# check validity of arguments
if len(sys.argv) < 2:
    print('Not enough arguments! Use "python main.py <input file>"')
    quit()
if len(sys.argv) > 2:
    print('Too many arguments! Use "python main.py <input file>"')
    quit()

# attempt to open files
try:
    kb_file = open(sys.argv[1], "r")
except:
    print('Could not open file "' + sys.argv[1] + '".')
    quit()
    
# process input file
kb = []
for line in kb_file:
    kb.append(line.split())
# negate the last line (the original clause)
clause = kb.pop()
negated = resolver.negateClause(clause)
# add each term as a separate clause
for n in negated:
    # the format of kb is a list of lists, so put n into a list by itself for consistency
    kb.append([n])    
    
resolver.prove(kb)