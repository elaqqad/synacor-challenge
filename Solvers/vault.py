""" Solves the vault puzzle by brute force
"""
from collections import defaultdict


grid = [
    ['22', '-', '9', '*'],
    ['+', '4', '-', '18'],
    ['4', '*', '11', '*'],
    ['*', '8', '-', '1']
]

def evaluate(expression):
    """ evaluate expression if terminal (not ending with an operation)
    """
    if expression[-1] in ['-','*','+']:
        return expression
    return str(eval(expression))
def neighbors(i: int, j: int):
    """ neighbors
    """
    all_corners = [(i, j-1), (i, j+1), (i-1, j), (i+1, j)]
    return [(x, y) for (x, y) in all_corners if (0 <= x <= 3 and 0 <= y <= 3)]

results = defaultdict(set) # key = (i,j) ; all possible results
paths = defaultdict(lambda : defaultdict(list)) # All possible paths of each possible result (i,j) => result => list
results[(0,0)].add('22')
paths[(0,0)]['22'].append('22')

for x in range(4):
    for i in range(0,4):
        for j in range (0,4):
            if i == 0 and j ==0 :
                continue
            for x in neighbors(i,j):
                digit=grid[i][j]
                for r in results[x]:
                    result=evaluate(r+digit)
                    results[(i,j)].add(result)
                    paths[(i,j)][result] = paths[(i,j)][result] + [ a + digit for a in paths[x][r]]
print(results[(3,3)])
print('30' in results[(3,3)])
print(paths[(3,3)]['30'])