from termcolor import colored
import colorama
colorama.init()

###########################
# HEX GRID INITIALIZATION #
###########################

# F = fire, E = earth, A = air, W = water, S = salt, Q = quicksilver, M = mors, V = vitae
# L = lead, T = tin, I = iron, C = copper, K = silver, G = gold, N = Nothing/Empty

# Hex grid tiling: https://www.redblobgames.com/grids/hexagons/

# Definitions
hex_grid = [[None for _ in range(11)] for _ in range(11)]
metals = ['L', 'T', 'I', 'C', 'K', 'G']
metals_loc = {'L': [], 'T': [], 'I': [], 'C': [], 'K': [], 'G': []}
file_s = list(open("puzzle.txt").read().split("\n")[0])
counter = 0
n = (len(hex_grid) - 1) // 2
q = 0

# Iterate across the image and add to the grid whenever a match is found.
invalid = False
print("Reading the hex grid...")
for r in range(-n, n + 1):
    q_iter = q
    while (True):
        if (counter == len(file_s)):
            invalid = True
            break
        hex_grid[q_iter + n][r + n] = file_s[counter]
        if (file_s[counter] in metals): metals_loc[file_s[counter]].append((q, r))

        counter += 1
        q_iter += 1
        if (q_iter > min(n - r, n)): break
    if (invalid): break
    if (q > -n): q -= 1
if (invalid):
    print("The grid is invalid.")
    exit(1)

def print_hex_grid(hex_grid, highlights = []):
    n = (len(hex_grid) - 1) // 2
    q = 0
    for r in range(-n, n + 1):
        print(" " * abs(r), end = "")
        q_iter = q
        while (True):
            if ((q_iter, r) in highlights):
                print(colored(hex_grid[q_iter + n][r + n], "red"), end = "")
            else:
                print(hex_grid[q_iter + n][r + n], end = "")
            q_iter += 1
            if (q_iter > min(n - r, n)): break
            print(" ", end = "")
        print()
        if (q > -n): q -= 1

print("Initial Configuration: ")
print_hex_grid(hex_grid)
print()

#################################
# REVEALED TILES INITIALIZATION #
#################################

# Reveals the tile at (q, r) if there are three consecutive empty tiles around it.
def reveal(hex_grid, revealed, q, r, metal_counter):
    n = (len(hex_grid) - 1) // 2    
    q_lower, q_upper = max(-n - r, -n), min(n - r, n)
    if (not (-n <= r <= n and q_lower <= q <= q_upper)): return
    
    # Don't attempt to reveal an empty tile.
    if (hex_grid[q + n][r + n] == 'N' or hex_grid[q + n][r + n] == None): return
    
    # Check first if this is a metal that can be revealed.
    # If this is a metal that we cannot reveal yet, end this function.
    metals = ['L', 'T', 'I', 'C', 'K', 'G']
    for i in range(len(metals)):
        if (hex_grid[q + n][r + n] == metals[i] and i != metal_counter): return

    # Get a list of which positions surrounding this tile are not filled.
    neighbors = []
    counter = 0
    for (dq, dr) in move_changes:
        Q = q + dq
        R = r + dr
        Q_lower, Q_upper = max(-n - R, -n), min(n - R, n)
        if (-n <= R <= n and Q_lower <= Q <= Q_upper):
            if (hex_grid[Q + n][R + n] == 'N'): neighbors.append(counter)
        else: neighbors.append(counter)
        counter += 1
    if (len(neighbors) < 3): return
    for i in range(len(neighbors)):
        valid = True
        for j in [1, 2]:
            # If there is a contiguous set of three open spaces around the tile, then it is revealed.
            if ((neighbors[i] + j) % 6 != neighbors[(i + j) % len(neighbors)]):
                valid = False
                break
        if (valid and (q, r) not in revealed[hex_grid[q + n][r + n]]):
            revealed[hex_grid[q + n][r + n]].append((q, r))
            break

revealed = {'F': [], 'E': [], 'A': [], 'W': [], 'S': [], 'Q': [], 'M': [], 'V': [],
            'L': [], 'T': [], 'I': [], 'C': [], 'K': [], 'G': []}
# Defined starting at left then moving all the way around clockwise.
move_changes = [(1, 0), (1, -1), (0, -1), (-1, 0), (-1, 1), (0, 1)]
q = 0
for r in range(-n, n + 1):
    q_iter = q
    while (True):
        reveal(hex_grid, revealed, q_iter, r, 0)
        q_iter += 1
        if (q_iter > min(n - r, n)): break
    if (q > -n): q -= 1

##########
# SOLVER #
##########

def remove_and_reveal(hex_grid, revealed, to_remove, metal_counter):
    global move_changes
    # Remove the atoms FIRST.
    for x in to_remove: hex_grid[x[0] + n][x[1] + n] = 'N'
    # THEN check if any new elements adjacent to it were revealed.
    for x in to_remove:
        for (dq, dr) in move_changes: reveal(hex_grid, revealed, x[0] + dq, x[1] + dr, metal_counter)

def solve(hex_grid, revealed, route, metal_counter = 0, depth = 0):
    global metals

    # There are no more moves (valid or invalid)
    if (all([len(revealed[c]) == 0 for c in revealed])):
        # Check if we have removed all of the atoms.
        q = 0
        for r in range(-n, n + 1):
            q_iter = q
            while (True):
                q_iter += 1
                if (hex_grid[q + n][r + n] != 'N'):
                    # There are no moves and there are still atoms on the board
                    # Thus, the puzzle has no solution.
                    return False, []
                if (q_iter > min(n - r, n)): break
            if (q > -n): q -= 1
        # The puzzle is solved!
        return True, route

    # Gold
    if (metal_counter == 5):
        for i in range(len(revealed['G'])):
            x = revealed['G'].pop(i)

            revealed_copy = {k: revealed[k].copy() for k in revealed}
            hex_grid_copy = [row.copy() for row in hex_grid]
            move = [([row.copy() for row in hex_grid], (x,))]

            remove_and_reveal(hex_grid_copy, revealed_copy, [x], metal_counter)
            win, possible_route = solve(hex_grid_copy, revealed_copy, route + move, metal_counter, depth + 1)
            if (win): return True, possible_route

            revealed['G'].insert(i, x)
    
    # Quicksilver + Lead/Tin/Iron/Copper/Silver
    for i in range(len(revealed['Q'])):
        x = revealed['Q'].pop(i)
        for c in "LTICK":
            for j in range(len(revealed[c])):
                y = revealed[c].pop(j)
                
                revealed_copy = {k: revealed[k].copy() for k in revealed}
                hex_grid_copy = [row.copy() for row in hex_grid]
                move = [([row.copy() for row in hex_grid], (x, y))]

                remove_and_reveal(hex_grid_copy, revealed_copy, [x, y], metal_counter)
                # Reveal the next metal(s) if it wasn't revealed already.
                if (len(revealed_copy[metals[metal_counter + 1]]) == 0):
                    for metal_loc in metals_loc[metals[metal_counter + 1]]:
                        q, r = metal_loc
                        reveal(hex_grid_copy, revealed_copy, q, r, metal_counter + 1)
                win, possible_route = solve(hex_grid_copy, revealed_copy, route + move, metal_counter + 1, depth + 1)
                if (win): return True, possible_route
                
                revealed[c].insert(j, y)
        revealed['Q'].insert(i, x)
    
    # Mors + Vitae
    for i in range(len(revealed['M'])):
        x = revealed['M'].pop(i)
        for j in range(len(revealed['V'])):
            y = revealed['V'].pop(j)
            
            revealed_copy = {k: revealed[k].copy() for k in revealed}
            hex_grid_copy = [row.copy() for row in hex_grid]
            move = [([row.copy() for row in hex_grid], (x, y))]
           
            remove_and_reveal(hex_grid_copy, revealed_copy, [x, y], metal_counter)
            win, possible_route = solve(hex_grid_copy, revealed_copy, route + move, metal_counter, depth + 1)
            if (win): return True, possible_route

            revealed['V'].insert(j, y)
        revealed['M'].insert(i, x)
    
    # Fire/Earth/Water/Air + Fire/Earth/Water/Air
    for c in "FEWA":
        for i in range(len(revealed[c])):
            for j in range(i + 1, len(revealed[c])):
                y = revealed[c].pop(j)
                x = revealed[c].pop(i)
                
                revealed_copy = {k: revealed[k].copy() for k in revealed}
                hex_grid_copy = [row.copy() for row in hex_grid]
                move = [([row.copy() for row in hex_grid], (x, y))]
                
                remove_and_reveal(hex_grid_copy, revealed_copy, [x, y], metal_counter)
                win, possible_route = solve(hex_grid_copy, revealed_copy, route + move, metal_counter, depth + 1)
                if (win): return True, possible_route
                
                revealed[c].insert(i, x)
                revealed[c].insert(j, y)
    
    # Salt + Salt
    for i in range(len(revealed['S'])):
        for j in range(i + 1, len(revealed['S'])):
            y = revealed['S'].pop(j)
            x = revealed['S'].pop(i)
            
            revealed_copy = {k: revealed[k].copy() for k in revealed}
            hex_grid_copy = [row.copy() for row in hex_grid]
            move = [([row.copy() for row in hex_grid], (x, y))]
            
            remove_and_reveal(hex_grid_copy, revealed_copy, [x, y], metal_counter)
            win, possible_route = solve(hex_grid_copy, revealed_copy, route + move, metal_counter, depth + 1)
            if (win): return True, possible_route

            revealed['S'].insert(i, x)
            revealed['S'].insert(j, y)
    
    # Fire/Earth/Water/Air + Salt
    for i in range(len(revealed['S'])):
        x = revealed['S'].pop(i)
        for c in "FEWA":
            for j in range(len(revealed[c])):
                y = revealed[c].pop(j)
                
                revealed_copy = {k: revealed[k].copy() for k in revealed}
                hex_grid_copy = [row.copy() for row in hex_grid]
                move = [([row.copy() for row in hex_grid], (x, y))]
                
                remove_and_reveal(hex_grid_copy, revealed_copy, [x, y], metal_counter)
                win, possible_route = solve(hex_grid_copy, revealed_copy, route + move, metal_counter, depth + 1)
                if (win): return True, possible_route

                revealed[c].insert(j, y)
        revealed['S'].insert(i, x)
    
    # If we didn't end already, then there must not be a solution.
    return False, []

route = []
win, route = solve(hex_grid, revealed, route)
if (win):
    i = 1
    for x in route:
        print("Move " + str(i) + ": ")
        print_hex_grid(x[0], x[1])
        print()
        i += 1
    print("The puzzle has been solved!")
else:
    print("There is no solution to this puzzle.")