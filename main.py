#dictionary to change colors
colorchange = {
    "black" : "white",
    "white" : "black"
}     



def board(state):
    """
    board function: takes a state of a board as input and ourtputs it in a somewhat realistic representation
    """
    #if one player does not have stones any stones left, he wins 
    if state[0]== [] or state[1] == []:
        return "last mover wins"
    
    #we define an empty board
    board = [[str(i) for i in range(13,25)],["--" for i in range(12)],[str(i) for i in range(12,9,-1)] + [str(0)+str(i) for i in range(9,0,-1)]]
    #we add enough empty rows to make it big enough for all scenarios 
    for i in range(15):
        board.insert(1, ["  " for i in range(12)])
        board.insert(len(board)-1, [ "  " for i in range(12)])
    #we define a count and a new line list for storage
    wb = -1
    new_lines = []
    #we iterate over each player
    for color in state:
        #we add to the player variable
        wb += 1
        #we iterate over every field
        for field in color:
            #we check if field is in lower half
            if field[0] < 13:
                index_updown = len(board)-1
                direction = -1
            #we check if field is in upper half
            else:
                index_updown = 0
                direction = +1
            #We iterate over the each field and row in the right half
            for box in range(len(board[index_updown])):
                #check if we found the field
                if int(board[index_updown][box]) == field[0]:
                    add = True
                    times = 1
                    count = 0
                    #add all stones to the fields
                    while add:
                        if board[index_updown + (direction*times)][box] == "  ":
                            if wb == 0:
                                board[index_updown + (direction*times)][box] = "ww"
                            else:
                                board[index_updown + (direction*times)][box] = "bb"
                            count += 1
                            if count == field[1]:
                                add = False
                        times += 1

    #remove empty lines from board
    pr_board = [i for i in board if i != ["  " for i in range(12)]]
    #add captured pieces if neccessary
    out = []
    if state[0][0][0] == 0:
        out.append((state[0][0], "ww"))
    if state[1][0][0] == 0:
        out.append((state[1][0], "bb"))
    if len(out) != 0:
        pr_board.append(out)
    #return board
    return pr_board

#tests can be seen thoughout all other tests

def move(state, indexme, indexop, field, dice):
    """
    Move function:
        
        Takes a state, informations about whos turn it is, a field and a dice throw as input.
        Outputs the state we get if we move one stone in the specified field by the specified amount. 
        
        inputs:
                state : a game state
                indexme: the index of the playing player (0=white, 1=black)
                indexop: the index of the opponenet (0=white, 1=black)
                field: the fiel that we want to make a move on
                dice: the dice number that we want to move
                
        output:
                state: a new game state where field of playing player is moved by one dice number (1-6)
                       returns false if legal move is not possible
    
    
    """
    #if moving player is white
    if indexme == 0:
        #calculate the position of the new field for our stone (moving in positive direction)
        new_field = state[indexme][field][0] + dice
        #if all our stones are in the last quarter and our stone moves exaclty out or is our worst stone and moves out 
        #we take the stone out
        if state[indexme][0][0] > 18 and (new_field == 25 or (field == state[indexme][0][0] and new_field >= 25)):
            #if the stone is alone in the field we delet the emppty field from our state representation
            if state[indexme][field][1] == 1:
                state[indexme].remove(state[indexme][field])
            #otherwise we just delete one stone 
            else:
                state[indexme][field][1] += -1
            #return the final state after the move
            return state
    
    #if moving player is black
    elif indexme == 1:
        #calculate the position of the new field for our stone (moving in negative direction)
        new_field = state[indexme][field][0] - dice
        #if we move from the the middle into the field we add 25 because we move in from high numbers
        if state[indexme][field][0] == 0:
            new_field += 25
        #if all our stones are in the last quarter and our stone moves exaclty out or is our worst stone and moves out 
        #we take the stone out
        if state[indexme][-1][0] < 7 and (new_field == 0 or (field == state[indexme][-1][0] and new_field <=0)):
            if state[indexme][field][1] == 1:
                state[indexme].remove(state[indexme][field])
            #otherwise we just delete one stone 
            else:
                state[indexme][field][1] += -1
            #return the final state after the move
            return state
        
    #if we move outsied of the field, this move is not possible and we return false
    if new_field > 24 or new_field < 1:
        return False
    
    #iterate over all fields of the opponent                                      
    for i in state[indexop]:
        #if the new field colides with an opposing field
        if new_field == i[0]:
            #if opponenet has only one stone on field, we can capture it
            if i[1] == 1:
                #we remove opponents pice from the board
                state[indexop].remove(i)
                exists = False
                #we add the pice to the captured pieces (position 0) if the field exists
                for u in state[indexop]:
                    if u[0] == 0:
                        u[1] +=1
                        exists = True
                        break
                #if it does not we add the field
                if exists == False:
                    state[indexop].append([0,1])
                break
            #if the opponent has more than one piece on the field we cannot move and return false
            else:
                return False
    
    #we remove the pice from the old field (remove field if last pice)
    if state[indexme][field][1] == 1:
        state[indexme].remove(state[indexme][field])
    else:
        state[indexme][field][1] += -1
    
    #if new field exists we add  our pice there and return the state                                      
    for i in state[indexme]:
        if new_field == i[0]:
            i[1] +=1
            return state
    #otherwise we add the field, sort both players fields form small to big
    state[indexme].append([new_field, 1])
    state[indexme].sort(key=lambda x: x[0])
    state[indexop].sort(key=lambda x: x[0])
    #we return the new state
    return state
    

        
#test on initial state
initial_state = [[[1,2], [12, 5], [17, 3], [19, 5]], [[6, 5], [8, 3], [13, 5], [24,2]]]
print("initial state: ")

for i in board(initial_state):
    print(i)

    
print()
print("move field 1 by 4: ")
for i in board(move(initial_state, 0, 1, 0, 4)):
    print(i)

print()
print("move field 24 by 4: ")
for i in board(move(initial_state, 1, 0, 3, 4)):
    print(i)
    
print()
print("move field 1 by 5 (False move): ")
print((move(initial_state, 0, 1, 0, 5)))
    
print()
print("move field 13 by 5: ")
for i in board(move(initial_state, 1, 0, 2, 6)):
    print(i)

print()
print("move field 17 by 1: ")
for i in board(move(initial_state, 0, 1, 3, 1)):
    print(i)
    
    
class backgammon_position():
    """
    Backgammon position class: each instance is a representation of a game position with additinoal information
    """
    def __init__(self, state, color_next, parent = None, heuval = None, roll = None, alpha = -float("inf"), beta = float("inf"), depth = None):
        #color of the player who has the next move
        self.color_next = color_next
        #state of the board
        self.state = state
        #store parent node for depth first search
        self.parent = parent
        #store children for deph first search
        self.children = []
        #store heuristic value of node
        self.heuval = heuval
        #store dice roll that lead to node
        self.roll = roll
        #store alpha and beta for alpha beta pruning 
        self.alpha = alpha
        self.beta = beta
        #store depth of node in tree
        self.depth = depth
        
        #if parent is defined add node as child to parent
        if self.parent != None:
            parent.children.append(self)
            
#tested throughout the code


import copy

def possible_moves(state, dice):
    """
    Takes a state (as backgammon_position class instances) and a dice roll as input and outputs a list of possible moves (as class instances)
    """
    #define indexme and indexop depending on color
    if state.color_next == "white":
        indexme = 0
        indexop = 1
    elif state.color_next == "black":
        indexme = 1
        indexop = 0
        
    #store differnet combinations of dice rolls
    numbers = [dice[0], dice[1], dice[1], dice[0]]
    #list to store states inbetween: start with a copy of the current state
    mid_states = [copy.deepcopy(state.state)]
    #list for end states
    end_states = []
    #list for final states
    final_states = []
    #iterate over dice rolls
    for i in range(len(numbers)):
        #iterate over states in mid states
        for statec in mid_states:
            #if we have stones left and stones captured, try to bring them back to the board
            if len(statec[indexme]) > 0 and 0 == statec[indexme][0][0]:
                new_state = copy.deepcopy(statec)
                new_state = move(new_state, indexme, indexop, 0, numbers[i])
                #if the new state is possible, we add it to tehe end states
                if new_state != False:
                    end_states.append(new_state)
            #if we dont have captured stones
            else:
                #we get new state for moving each of our fields
                for field in range(len(statec[indexme])):
                    new_state = copy.deepcopy(statec)
                    new_state = move(new_state, indexme, indexop, field, numbers[i])
                    #if new states are possible we edd them to the end staes
                    if new_state != False:
                        end_states.append(new_state)
        
        #if we dont have new states, we add the midstates (half move but all thats possible) to the end states
        if len(end_states) == 0:
            end_states = mid_states
        #if we dont have doubles (dice pair) we evaluaer the end staes
        if (i ==1 and dice[0] != dice[1]) or i == 3:
            for i in end_states:
                #if we have not found a state in end state yet, we add it to final states
                if i not in final_states:
                    #if we have a finning state we return it
                    if i[indexme] == []:
                        return [i]
                    final_states.append(i)
            #we reset mid states and end states
            mid_states = [copy.deepcopy(state.state)]
            end_states = []
        
        #if we have doubles or jsut moved of of two piecs, we move end states to midstates
        else:
            mid_states = end_states
            end_states = []
            
    #we return final states
    return final_states
    
    
#test possible moves 
initial_state = [[[1,2], [12, 5], [17, 3], [19, 5]], [[6, 5], [8, 3], [13, 5], [24,2]]]
print("initial state: ")
for i in board(initial_state):
    print(i)

print()
print("possible states after one move with white from initial state and roll [1,5]: ")
print()
test = possible_moves(backgammon_position(initial_state, "white"), [1,5])
for t in test:
    for i in board(t):
        print(i)
    print()
#test if all states are unique
for t1 in range(len(test)):
    for t2 in range(t1+1, len(test)):
        if test[t1] == test[t2]:
            print("False")

print()
print("possible states after one move with black from initial state and roll [1,5]: ")
print()
test = possible_moves(backgammon_position(initial_state, "black"), [1,5])
for t in test:
    for i in board(t):
        print(i)
    print()

#test if all states are unique
for t1 in range(len(test)):
    for t2 in range(t1+1, len(test)):
        if test[t1] == test[t2]:
            print("False")
    
print()
print("possible states after one move with white from initial state and roll [3,3]: ")
print()
test = possible_moves(backgammon_position(initial_state, "white"), [1,5])
for t in test:
    for i in board(t):
        print(i)
    print()

#test if all states are unique
for t1 in range(len(test)):
    for t2 in range(t1+1, len(test)):
        if test[t1] == test[t2]:
            print("False")
            
            
            
            
def heuristic_1(state):
    """
    heuristic function: takes a state as input and outputs the heuristic value 
    
    calculates the minimum number of points needed to remove all stones from the board for each color
    
    returns white - black
    """
    #define initial counts for both colors 
    white = 0
    black = 0
    #add number of points need to remove field times stones on it for all white stones to white
    for field in state[0]:
        white += (25- field[0]) * field[1]
    #add number of points need to remove field times stones on it for all black stones to black
    for field in state[1]:
        if field[0] == 0:
            black += 25 * field[1]
        else:
            black += field[0] * field[1]
    #if white has no stones left return minus infinity 
    if white == 0:
        return -float("inf")
    #if black has no stones left return infinity
    if black == 0:
        return float("inf")
    #return heuristic value
    return white - black
    
    
    
"test heuristic function"
initial_state = [[[1,2], [12, 5], [17, 3], [19, 5]], [[6, 5], [8, 3], [13, 5], [24,2]]]

print(heuristic_1(initial_state) == 0)
print(heuristic_1([[[1,2]],[[24,2]]]) == 0)
print(heuristic_1([[[1,2], [5,5]],[[24,2]]]) == 100)
print(heuristic_1([[[1,2]],[[24,2], [5,5]]]) == -25)
print(heuristic_1([[[1,2], [5,5]],[[24,2], [5,5]]]) == 75)




def find_next_move_1(state, diceroll):
    """
    Function to find the next best move for the AI
    
    Takes a state (as class instance) a dice roll and a maximum depth as input
    
    Does a complete minimax search considering one move per player
    """
    #find all possible dice rolls 
    possible_roles = []
    for i in range(1,7):
        for u in range(i,7):
            possible_roles.append([i,u])
            
    #store all possible moves in a list 
    my_moves_1 = []
    for i in possible_moves(state, diceroll):
        my_move = backgammon_position(i, colorchange[state.color_next])
        my_moves_1.append(my_move)
    #define depth to be 1
    depth = 1
    
    #define count max based on color 
    if state.color_next == "white":
        cou_max = float('inf')
    elif state.color_next == "black":
        cou_max = -float('inf')
    
    #go over each state in possible moves
    for move in my_moves_1:
        next_move = []
        #go over each dice roll possible
        for role in possible_roles:
            #define opposite moves and heu max based on color
            opp_moves = possible_moves(move, role)
            if move.color_next == "white":
                heu_max = float('inf')
            elif move.color_next == "black":
                heu_max = -float('inf')
            #iterate over each opponent move and find best heuristic value (bets move for opponent)
            for opp in opp_moves:
                #calculate heuristic value 
                heu_eval = heuristic_1(opp)
                if move.color_next == "white":
                    if heu_eval < heu_max:
                        heu_max = heu_eval
                        opp_rm = opp
                elif move.color_next == "black":
                    if heu_eval > heu_max:
                        heu_max = heu_eval
                        opp_rm = opp
            #append the best next move with heursitic value and dice toll to next move
            next_move.append([opp_rm, heu_max, role])
        #define count
        count = 0
        #go over each best next move and calculate weighted heursic value for prior move
        for i in next_move:
            if i[2][0] == i[2][1]:
                count += i[1]* (1/36)
            else:
                 count += i[1]* (2/36)
        #find best move dependent on color
        if move.color_next == "black":
            if count < cou_max:
                cou_max = count
                choose = move
        elif move.color_next == "white":
            if count > cou_max:
                cou_max = count
                choose = move
    #return best move          
    return choose
            
            
            
 #test from initial state with differnt rolls 
initial_state = [[[1,2], [12, 5], [17, 3], [19, 5]], [[6, 5], [8, 3], [13, 5], [24,2]]]
teststate = backgammon_position(initial_state, "white")

print("initial state: ")
for i in board(initial_state):
    print(i)

print("best move for roll [5,1]")
for i in board(find_next_move_1(teststate, [5,1]).state):
    print(i)
print()

print("best move for roll [3,2]")
for i in board(find_next_move_1(teststate, [3,2]).state):
    print(i)
print()

print("best move for roll [4,1]")
for i in board(find_next_move_1(teststate, [4,1]).state):
    print(i)
print()

print("best move for roll [2,2]")
for i in board(find_next_move_1(teststate, [2,2]).state):
    print(i)
print()


def find_next_move_2(state, diceroll, max_depth = 1):
    """
    Function to find the next best move for the AI
    
    Takes a state (as class instance) a dice roll and a maximum depth as input
    
    Does a complete minimax search of the specified depth
    """
    #calculate all possible dice rolls 
    possible_roles = []
    for i in range(1,7):
        for u in range(i,7):
            possible_roles.append([i,u])
    
    
    my_moves_1 = []
    #iterate over all possible moves
    for i in possible_moves(state, diceroll):
        #store them as class instances in a list
        my_move = backgammon_position(i, colorchange[state.color_next])
        my_moves_1.append(my_move)
    
    #degien cou max based on color 
    if state.color_next == "white":
        cou_max = float('inf')
    elif state.color_next == "black":
        cou_max = -float('inf')
    
    #set initial depth to 0
    depth = 0
    #define current moves and set them to possibe moves
    current_my_moves = my_moves_1
    #iterate as long as maximum depth is not reached
    while depth < max_depth:
        #increate depth
        depth += 1
        #define new list
        my_current_moves_next = []
        #iterate over current moves list
        for move in current_my_moves:
            next_move = []
            #iterate over possible rolls
            for role in possible_roles:
                #find possible moves for opponent
                opp_moves = possible_moves(move, role)
                #define inital state of maximum heurstic value by color 
                if move.color_next == "white":
                    heu_max = float('inf')
                elif move.color_next == "black":
                    heu_max = -float('inf')
                ##iterate over possible opponent moves
                for opp in opp_moves:
                    #get heuristic value 
                    heu_eval = heuristic_1(opp)
                    #find opp move with best heuristic value based on color 
                    if move.color_next == "white":
                        if heu_eval < heu_max:
                            heu_max = heu_eval
                            opp_rm = opp
                    elif move.color_next == "black":
                        if heu_eval > heu_max:
                            heu_max = heu_eval
                            opp_rm = opp
                #store best opp moves with heurstic vlaue and dice toll
                next_move.append([opp_rm, heu_max, role])
            
            #if depth limit not reached find next set of moves based on opponent move
            if depth != max_depth:
                for role in possible_roles:
                    for i in possible_moves(backgammon_position(opp_rm, colorchange[state.color_next]), role):
                        my_current_moves_next.append(backgammon_position(i, colorchange[state.color_next], parent = move, roll = role))
            #if depth limit is reached find weighted heuristic value 
            else:
                count = 0
                #iterate over next moves
                for i in next_move:
                    if i[2][0] == i[2][1]:
                        count += i[1]* (1/36)
                    else:
                         count += i[1]* (2/36)
                #set heuval of move to count
                move.heuval = count
        #if max depth is not yet reached update list
        if depth != max_depth:
            current_my_moves = my_current_moves_next
    #find heuristic value for all moves
    for i in my_moves_1:
        i.heuval = getval(i)
    
    #find best move based on heurstic values and colors of possible moves
    for i in my_moves_1:
        if move.color_next == "black":
            if count < cou_max:
                cou_max = count
                choose = i
        elif move.color_next == "white":
            if count > cou_max:
                cou_max = count
                choose = i
    #return best move
    return choose


def getval(node):
    """
    get val function: helper function of find_next_move_2
    
    takes a node as input and outputs the heurstic function as a weighted some of children
    works recursively down the tree
    """
    #if heuval is not defined calculated it based on heuvals of children
    if node.heuval == None:
        count = 0
        for i in node.children:
            if i.roll[0] == i.roll[1]:
                count += getval(i)*(1/36)
            else:
                count += getval(i)*(2/36)
            return count
    #if heuval is knows return it
    else:
        return node.heuval
 
#test from initial state with differnt rolls 
initial_state = [[[1,2], [12, 5], [17, 3], [19, 5]], [[6, 5], [8, 3], [13, 5], [24,2]]]
teststate = backgammon_position(initial_state, "white")

print("initial state: ")
for i in board(initial_state):
    print(i)

print("best move for roll [5,1]")
for i in board(find_next_move_2(teststate, [5,1]).state):
    print(i)
print()

print("best move for roll [2,2]")
for i in board(find_next_move_2(teststate, [2,2]).state):
    print(i)
print()



def find_next_move_3(state, diceroll, max_depth = 2):
    """
    Function to find the next best move for the AI
    
    Takes a state (as class instance) a dice roll and a maximum depth as input
    
    Does a complete minimax search of the specified depth
    Uses alpha beta pruning to reduce search time
    """
    #find all possible rolls
    possible_roles = []
    for i in range(1,7):
        for u in range(i,7):
            possible_roles.append([i,u])
    
    #start stack for depth first search
    stack = []
    stack.append(state)
    #append possible moces to stack
    for i in possible_moves(state, diceroll):
        
        my_move = backgammon_position(i, colorchange[state.color_next], depth = 1, parent = state)
        stack.append(my_move)
    cdepth = 1
    
    if state.color_next == "white":
        cou_max = float('inf')
    elif state.color_next == "black":
        cou_max = -float('inf')
    

    found = False
    #get first node and start tree search
    node = stack.pop()
    while found == False:
        #increase depth
        cdepth +=1
        #stop if done searching
        if node.parent == None: 
            found = True
            continue
        
        #see if pruning is possible
        if node.parent.alpha >= node.parent.beta:
            
            while node.depth <= node.parent.depth:
                stack.pop()
            continue
            
        #if not at leave nodes, append new nodes 
        if cdepth <= max_depth:
            
            for rolld in possible_roles:
                poss_mo = []
                for i in possible_moves(node, rolld):
                    
                    node_children = backgammon_position(i, colorchange[node.color_next], depth = cdepth, parent = node, roll = rolld)
                    poss_mo.append(node_children)
                
                #only append best options for each role
                if cdepth != max_depth:
                    if poss_mo[0].color_next == "black":
                        heu_max = float('inf')
                    elif poss_mo[0].color_next == "white":
                        heu_max = -float('inf')
                    for fb in poss_mo:
                        heu_val = heuristic_1(fb.state)
                        
                        if fb.color_next == "white":
                            if heu_val > heu_max:
                                
                                heu_max = heu_val
                                best_node = fb
                        elif fb.color_next == "black":
                            if heu_val < heu_max:
                                
                                heu_max = heu_val
                                best_node = fb
                    stack.append(best_node)
                #if leave node next append all         
                else:
                    for fb in poss_mo:
                        stack.append(fb)
            node = stack.pop()
        #if leave node check for heursitic values
        else:
            
            best_succ = []
            heueval = 0
            pr = node.parent
            #find heuristic values 
            while node.depth == cdepth-1:
                cr = node.roll
        
                
                
                if node.color_next == "black":
                    heu_max = float('inf')
                elif node.color_next == "white":
                    heu_max = -float('inf')    
                #find best for each role
                while node.roll == cr:
                    heu_val = heuristic_1(node.state)
                    
                    if node.color_next == "white":
                        if heu_val > heu_max:
                            
                            heu_max = heu_val
                            best_node = node
                    elif node.color_next == "black":
                        if heu_val < heu_max:
                            
                            heu_max = heu_val
                            best_node = node
                    node = stack.pop()
                best_succ.append(best_node)
            #find weighted average 
            for i in best_succ:   
                if i.roll[0] == i.roll[1]:
                    heueval += heuristic_1(i.state)*(2/36)
                else:
                    heueval += heuristic_1(i.state)*(1/36)
 
            #update alpha/beta
            if pr.color_next == "black":
                if heueval > pr.alpha:
                    pr.alpha = heueval

            elif pr.color_next == "white":
                if heueval < pr.beta:
                    pr.beta = heueval

            #check if pruning is possible
            if pr.alpha >= pr.beta:
                
                while node.depth == cdepth-2:
                    node = stack.pop()
                
            #update alpha/beta
            if node.depth == pr.depth:
                
                if pr.color_next == "black":
                    
                    if pr.alpha < pr.parent.beta:
                        
                        pr.parent.beta = pr.alpha

                if pr.color_next == "white":
                    
                    if pr.beta > pr.parent.alpha:
                        
                        pr.parent.alpha = pr.beta
            
            #update alpha/beta
            if node.depth < pr.depth:
                
                if node.color_next == "black":
                    for i in node.children:
                        if node.alpha < i.beta and i.beta != float(inf):
                            node.alpha = node.i.beta
                    for i in node.children:
                        i.alpha = node.alpha
                if node.color_next == "white":
                    for i in node.children:
                        if node.beta > i.alpha and i.beta != float(inf):
                            node.beta = i.alpha
                    for i in node.children:
                        i.beta = node.beta

            cdepth = node.depth
    #find best move based on tree search and color
    if state.color_next == "white":
        final = float("inf")
        
        for i in state.children:
            
            if i.alpha < final:
                
                final = i.alpha
                best = i

    elif state.color_next == "black":
        final = -float("inf")
        
        for i in state.children:
            
            if i.beta > final:
                
                final = i.beta
                best = i
    #return best move   
    return best
import random 

def dice():
    """
    dice function: returns a diceroll with two dices
    """
    
    dice1 = random.randrange(1,7,1)
    dice2 = random.randrange(1,7,1)
    
    return[dice1, dice2]
 
 initial_state = [[[1,2], [12, 5], [17, 3], [19, 5]], [[6, 5], [8, 3], [13, 5], [24,2]]]
teststate = backgammon_position(initial_state, "white")

for i in board(find_next_move_1(teststate, [5,1]).state):
    print(i)

import time
def game(function = find_next_move_1):
    initial_state = [[[1,2], [12, 5], [17, 3], [19, 5]], [[6, 5], [8, 3], [13, 5], [24,2]]]
    print("Hello, lets play backgammon!!")
    print()
    time.sleep(1)
    
    print("1. white")
    print("2. black")
    c = input("Choose a color: ")
    if c in ["1", "white", "White"]:
        oc = "white"
        mc = "black"
        indexme = 1
        indexop = 0
    else:
        oc = "black"
        mc = "white"
        indexme = 0
        indexop = 1
    
    time.sleep(1)
    print()
    print("Great, Lets see who starts: ")
    print()
    startroll = dice()
    print(startroll)
    while startroll[0] == startroll[1]:
        startroll = dice()
        print(startroll)
    print()
    if startroll[0] > startroll[1]:
        print("You start")
        start = False
    else:
        print("I start")
        start = True
    print()
    
    
    
    
    if start == False:
        beginning_node = backgammon_position(initial_state ,oc)
        for i in board(beginning_node.state):
            print(i)
        print()
        roll = startroll
        print("Your roll: " + str(roll))
        
        time.sleep(1)
        
        print("Your move: ")
        if roll[0] == roll[1]:
            r = 2
        else:
            r = 1
        current_state = beginning_node.state
        for i in range(r):
            
            righin = True
            while righin:
                f = int(input("field 1: "))
                for u in range(len(current_state[indexop])):
                    if current_state[indexop][u][0] == f:
                        f1 = u
                        righin = False
                
                
            dq = int(input("dice (1 or 2): "))
            if dq ==1:
                d1 = roll[0]
                d2 = roll[1]
            else:
                d1 = roll[1]
                d2 = roll[0]
            print()
            current_state = move(current_state, indexop, indexme, f1, d1)
            for i in board(current_state):
                print(i)
            print()
            
            righin = True
            while righin:
                f = int(input("field 2: "))
                for u in range(len(current_state[indexop])):
                    if current_state[indexop][u][0] == f:
                        f2 = u
                        righin = False
                    
            print()
            current_state = move(current_state, indexop, indexme, f2, d2)
            
            for i in board(current_state):
                print(i)
            print()
            
    
    else:
        beginning_node = backgammon_position(initial_state ,mc )
        current_state = beginning_node.state
        for i in board(current_state):
            print(i)
        print()
    
    initiate_game_loop = True
    while initiate_game_loop:
        
        if board(current_state) == "last mover wins":
            initiate_game_loop = False
            continue
        if startroll != None:
            rollm = startroll
            startroll = None
        else:
            rollm = dice()
        
        print("My roll: " + str(rollm))
        print()
        print("My Move: ")
        print()
        my_m = function(backgammon_position(current_state ,mc ), rollm)
        current_state = my_m.state
        for i in board(current_state):
            print(i)
        time.sleep(2)
        if board(current_state) == "last mover wins":
            initiate_game_loop = False
            continue
            
        
        print()
        rollp = dice()
        print("Your roll: " + str(rollp))
        print("Your move: ")
        if rollp[0] == rollp[1]:
            r = 2
        else:
            r = 1
            
        for i in range(r):
            
            righin = True
            while righin:
                f = int(input("field 1: "))
                for u in range(len(current_state[indexop])):
                    if current_state[indexop][u][0] == f:
                        f1 = u
                        righin = False
                
                
            dq = int(input("dice (1 or 2): "))
            if dq ==1:
                d1 = rollp[0]
                d2 = rollp[1]
            else:
                d1 = rollp[1]
                d2 = rollp[0]
            print()
            current_state = move(current_state, indexop, indexme, f1, d1)
            time.sleep(1)
            for i in board(current_state):
                print(i)
            print()
            
            righin = True
            while righin:
                f = int(input("field 2: "))
                for u in range(len(current_state[indexop])):
                    if current_state[indexop][u][0] == f:
                        f2 = u
                        righin = False
                    
            print()
            current_state = move(current_state, indexop, indexme, f2, d2)
            
            for i in board(current_state):
                print(i)
            print()
 
game()
