import random
def create_grid(n,m):
    return [[0.00 for _ in range(n)] for _ in range(m)]

def get_neighbor_pos(i,j,n,m,policy=None):
    if policy:
        pos = []
        actions = policy[i][j]
        for action in actions:
            if action == '^':
                pos.append((i-1,j))
            elif action == 'v':
                pos.append((i+1,j))
            elif action == '<':
                pos.append((i,j-1))
            else:
                pos.append((i,j+1))
        return pos
    else:
        k = [-1,0,0,1]
        l = [0,-1,1,0]
        pos = []
        for kk,ll in zip(k,l):
            ikk = i + kk
            jll = j + ll
            if (ikk < 0) or (ikk == m) or (jll < 0) or (jll == n):
                continue
            pos.append((i+kk,j+ll))
        return pos

def print_grid(grid, policy=None):
    for row in grid:
        if policy:
            print(row)
        else:    
            print([round(e,2) for e in row])

def get_policy_grid(grid, n, m):
    policy_grid = [[[] for _ in range(n)] for _ in range(m)]
    for i in range(n):
        for j in range(m):
            if (i == n-1) and (j == m-1):
                continue
            if (i == 0) and (j == 0):
                continue
            neighbor_pos = get_neighbor_pos(i,j,n,m)
            v_max = max([grid[k][l] for k,l in neighbor_pos])
            for k,l in neighbor_pos:
                if grid[k][l] == v_max:
                    if k < i:
                        policy_grid[i][j].append('^')
                    elif k > i:
                        policy_grid[i][j].append('v')
                    elif l < j:
                        policy_grid[i][j].append('<')
                    else:
                        policy_grid[i][j].append('>')
    return policy_grid

def get_path(policy_grid,n,m,x,y):
    actions = []
    while True:
        act = random.choice(policy_grid[x][y])
        if act == '^':
            x -= 1
        elif act == 'v':
            x += 1
        elif act == '<':
            y -= 1
        else:
            y += 1
        actions.append(act)
        if (x == 0 and y == 0) or (x == n-1 and y == m-1):
            break
    return actions

def value_iter(grid,n,m,r,epsilon,gamma):
    while True:
        flag = False
        policy_grid = get_policy_grid(grid,n,m)
        for i in range(n):
            for j in range(m):
                if (i == n-1) and (j == m-1):
                    continue
                if (i == 0) and (j == 0):
                    continue
                v = grid[i][j]
                neighbor_pos = get_neighbor_pos(i,j,n,m,policy_grid)
                grid[i][j] = sum([1/(len(neighbor_pos))*(r + gamma*grid[k][l]) for k,l in neighbor_pos])
                if abs(v - grid[i][j]) < epsilon:
                    flag = True
                    break
        if flag:
            return grid, policy_grid

epsilon = 0.0001
gamma = 0.9
r = -1
n = 5
m = 5
grid = create_grid(n,m)
grid, policy_grid = value_iter(grid,n,m,r,epsilon,gamma)
print_grid(grid)
print()
print_grid(policy_grid,policy=True)
print()
print(get_path(policy_grid,n,m,2,2))