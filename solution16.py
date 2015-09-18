
"""
References:
We referred following websites for implementing the A* search for 16 tile problem.
https://gist.github.com/joshuakenzo/1291155
http://stackoverflow.com/questions/4159331/python-speed-up-an-a-star-pathfinding-algorithm
http://web.mit.edu/eranki/www/tutorials/search/

Commands to execute the code:
python solution16.py input.txt
Output will be the moves taken to return to goal state
Few input files to test the code were attached

Approach:
We started programming by considering the input state as the initial state and for every state there are 16 possible branches. L1 - 1st row towards left
L2 - 2nd row towards left ...... We considered each direction of movement as an action. There are 16 actions possible for every board.
We use A* with manhattan distance as heuristic to find the next best action.

We display the moves we take inorder to reach the goal state as our output.

The function used is g(n)+h(n)
g(n) = 1 (for every expansion)
h(n) = manhattan distance (If the tile is present in the coreners of the same row or column then we take h as 1 
since one slide will be enough to push the tile to its position)

The heuristic function that we took is admissible because it is not an over estimate.

We assumed that manhattan distance is the best heuristic for this problem. 
We used a priority queue to store the node intsances that were not visited yet and a list to store the node instances visited
We tried using various data structures but priority queue seemed to work best. 

The overall algorithm worked fine but it is taking too long to compute the moves. A better way of using data structures might reduce the time complexity.
We are able to finc solution for most complex moves but the time taken is too long.
"""
import copy
import sys
import math
import time
import bisect
import random
import itertools
import pdb
import Queue as Q

class Board:
    """
    class for storing Board configuration
    """
    def __init__(self,text):
        """ Initializing board with the values from input text"""
        self.size = 4
        matrix_size = 16
        values = []
        if text!= None:
            for n in text.split(","):
                values.append(int(n))
            if sorted(values) != range(1,matrix_size+1):
                print "invalid numbers"
                sys.exit(1)
        else:
            print "enter valid input text"
	
        self.matrix=[[0 for x in range(4)] for x in range(4)] 
        for y in range(4):
            for x in range(4):
                self.matrix[y][x]=values[(y*4)+x]
        """filling the values for goal state"""
        """storing the indices of the values as key value pairs with value being the location of the key"""
        self.goals = {}
        for x in range(matrix_size):
            self.goals[x + 1] = x % 4, x / 4

    def astar(self):
        
        #closedlist = set() 
        closedlist = []
        q = Q.PriorityQueue()
        q.put(Node(self, None, 0, None))
        visited = 0        
        while not q.empty():
            visited+=1
            node = q.get()
            if node.board.h() == 0:
                moves = []
                while node.parent:
                    moves.append(node.action)
                    node = node.parent
                moves.reverse()
                print "Solution found!"
                print "Number of nodes visited = ", visited
                print "All moves:", ", ".join(str(move) for move in moves)
                break
            else:
                for new_node in node.expand():
                    if new_node not in q.queue and new_node not in closedlist:
                        q.put(new_node)
                #closedlist.add(node)
                closedlist.append(node)
   
    def h(self):
        h = 0
        for y, row in enumerate(self.matrix):
            for x, tile in enumerate(row):
                h1 = math.fabs(x - self.goals[tile][0]) + \
                     math.fabs(y - self.goals[tile][1])
                if h1==3 and (x == self.goals[tile][0] or y == self.goals[tile][1]):
                    h1 = 1
                h += h1
        return h
    def apply_action(self, action):
       
	if action == 'R1':
            temp = self.matrix[0][3]
            for i in range(3,0,-1):
                self.matrix[0][i] = self.matrix[0][i-1]
            self.matrix[0][0] = temp
        elif action=='R2':
            temp = self.matrix[1][3]
            for i in range(3,0,-1):
                self.matrix[1][i] = self.matrix[1][i-1]
            self.matrix[1][0] =  temp
        elif(action=='R3'):
            temp = self.matrix[2][3]
            for i in range(3,0,-1):
                self.matrix[2][i] = self.matrix[2][i-1]
            self.matrix[2][0] =  temp
        elif(action=='R4'):
            temp = self.matrix[3][3]
            for i in range(3,0,-1):
                self.matrix[3][i] = self.matrix[3][i-1]
            self.matrix[3][0] =  temp
        elif(action=='L1'):
            temp = self.matrix[0][0]
            for i in range(0,3):
                self.matrix[0][i] = self.matrix[0][i+1]
            self.matrix[0][3] =  temp
        elif(action=='L2'):
            temp = self.matrix[1][0]
            for i in range(0,3):
                self.matrix[1][i] = self.matrix[1][i+1]
            self.matrix[1][3] =  temp
        elif(action=='L3'):
            temp = self.matrix[2][0]
            for i in range(0,3):
                self.matrix[2][i] = self.matrix[2][i+1]
            self.matrix[2][3] =  temp
        elif(action=='L4'):
            temp = self.matrix[3][0]
            for i in range(0,3):
                self.matrix[3][i] = self.matrix[3][i+1]
            self.matrix[3][3] =  temp
        elif(action=='U1'):
            temp = self.matrix[0][0]
            for i in range(0,3):
                self.matrix[i][0] = self.matrix[i+1][0]
            self.matrix[3][0] =  temp
        elif(action=='U2'):
            temp = self.matrix[0][1]
            for i in range(0,3):
                self.matrix[i][1] = self.matrix[i+1][1]
            self.matrix[3][1] =  temp
        elif(action=='U3'):
            temp = self.matrix[0][2]
            for i in range(0,3):
                self.matrix[i][2] = self.matrix[i+1][2]
            self.matrix[3][2] =  temp
        elif(action=='U4'):
            temp = self.matrix[0][3]
            for i in range(0,3):
                self.matrix[i][3] = self.matrix[i+1][3]
            self.matrix[3][3] =  temp
        elif(action=='D1'):
            temp = self.matrix[3][0]
            for i in range(3,0,-1):
                self.matrix[i][0] = self.matrix[i-1][0]
            self.matrix[0][0] =  temp
        elif(action=='D2'):
            temp = self.matrix[3][1]
            for i in range(3,0,-1):
                self.matrix[i][1] = self.matrix[i-1][1]
            self.matrix[0][1] =  temp
        elif(action=='D3'):
            temp = self.matrix[3][2]
            for i in range(3,0,-1):
                self.matrix[i][2] = self.matrix[i-1][2]
            self.matrix[0][2] =  temp
        elif(action=='D4'):
            temp = self.matrix[3][3]
            for i in range(3,0,-1):
                self.matrix[i][3] = self.matrix[i-1][3]
            self.matrix[0][3] =  temp
    
    def actions(self):
        actions = []
        actions.append("L1")
        actions.append("L2")
        actions.append("L3")
        actions.append("L4")
        actions.append("R1")
        actions.append("R2")
        actions.append("R3")
        actions.append("R4")
        actions.append("U1")
        actions.append("U2")
        actions.append("U3")
        actions.append("U4")
        actions.append("D1")
        actions.append("D2")
        actions.append("D3")
        actions.append("D4")	
        return actions 
    def __str__(self):
        grid = "\n".join([" ".join(["{:>2}"] * 4)] * 4)
        values = itertools.chain(*self.matrix)
        return grid.format(*values).replace("None", "  ")


class Node:
    def __init__(self, board, action, cost, parent):
        self.board = board
        self.action = action
        self.cost = cost
        self.parent = parent
        """storing f = g(n)+h(n)"""
        self.f = cost + board.h() 
    
    def expand(self):
        
        nodes = []

        for action in self.board.actions():
            board = copy.deepcopy(self.board)
            board.apply_action(action)
            nodes.append(Node(board, action, self.cost + 1, self))
        
        return nodes

    def __eq__(self, rhs):
        if isinstance(rhs, Node):
            return self.board.matrix == rhs.board.matrix
        else:
            return rhs == self

    def __hash__(self):
        return hash((self.board,self.action,self.cost,self.parent))
    def __lt__(self, rhs):
        return self.f < rhs.f
    def __cmp__(self, other):
        return cmp(self.cost,other.cost)
def main():
	file = sys.argv[1]
	inputfile = open(file)
	inputfile = inputfile.readlines()
	temp = ""
	count = 0
	for line in inputfile:
		count = count + 1
		temp+=(line.split(" ")[0].rstrip())+","
		temp+=(line.split(" ")[1].rstrip())+","
		temp+=(line.split(" ")[2].rstrip())+","
		if(count!=4):
			temp+=(line.split(" ")[3].rstrip())+","
		else:
			temp+=(line.split(" ")[3].rstrip())
	b = Board(temp)
	b.astar()
if __name__ == "__main__":main()
