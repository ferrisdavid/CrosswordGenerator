# David Ferris


blank = ' ' # Initializing or defining a free space in the board as an string with a space
LastError = {} # Initializing a dictionary that will be used to keep track of the most recent error for a specific word


def printboard(board): # defining a function to print out the matrix/board by simply looping through the entire board
    m,n = len(board),len(board[0]) # Assigning the number of rows and the number of elements within those rows of the board to variables
    print(' 01234567890123456789') # the printing of these indices and lines are not necessary and are purely fore aesthetic as well as the utility of easily seeing where a letter is placed
    print(' '+'_'*m)
    for i in range(m): # Start of loop to go through each element within the matrix/booard
        print('|',end = '')
        for j in range(n):
            print(board[i][j],end = '')
        print('|'+str(i))
    print(' '+'_'*m)
    print(' 01234567890123456789')

#helper function
def addfirstword(word,board): # here we are defining a function that will add the first word in the list in the middle of the board horizontally
    D = len(board)
    n = len(word)
    if n> D: # if the word is too long then it cannot be placed and we return false we loop through the list in a separate function when the word is too long to ensure that every word is attempted to be placed
        return False
    for k in range(n):# this loop goes through the length of the string and places it in the middle of the board
        column = D//2 - n//2 + k # defining the column for the word to be placed, k is the loop counter variable which allows us to start at the first index of the word and move forward
        board[D//2 - 1][column] = word[k] # here the individual letters of the word are being placed in the correct places
    return board           # I chose to place my word at the ninth index in the board as that is technically the tenth position in the board

#helper function
def checkadjacentvertical(word,board,IntersectIndex,x,y): # here we are defining a function that will check if a placement of a word vertically at a certain location has illegal adjacencies
    BeforeIntersect = word[:IntersectIndex] # The beforeintersect and afterintersect variables are used to separate the current word
    AfterIntersect = word[IntersectIndex+1:]# into the two portions of the correct length in the board where we want to check for adjacencies
    isAdjacent = False # This variable is used to update when we have come across an illegal adjacency 
    if len(BeforeIntersect) <= x + 1 and len(AfterIntersect) <= 19-x: # Here we are ensuring that our word does not reach outside the grid
        for i in range(1,len(BeforeIntersect)+1): # this first loop will move through the board backwards from the point of intersection
            if x == 0: # since we do not know where the intersection is occurying there are many cases we must deal with which is the purpose of these if statements
                return True # if the intersect is at the top of the board and it does not intersect at the first index then we reach outside the grid
            if i ==len(BeforeIntersect): # this sequence of if statements checks if the before intersect only has a length of one
                if x-i != 0:             # and if so checks to make sure that there is no letter directly above it
                    if board[x-i-1][y] != blank:
                        return True
            if i > 1: # this sequence of if statements checks that if we are atleast two positions away from the intersection
                if board[x-i][y] == word[IntersectIndex-i]: # then we must see if there is a letter on the board that is the same as the letter we are currently attempting to place
                    if x-i != 0:
                        if board[x-i-1][y] != blank: # we prevent the possibility of intersecting with another vertically placed word by ensuring the next position is blank
                            isAdjacent = True
                            break
                        else:
                            continue
                    else:
                        continue
                else:
                    if x-i!= 0: # if the position we are at does not have a letter that is the same as the current letter we are at and the spot is not blank then  
                        if board[x-i][y]!=blank: # we have hit an illegal adjacency
                            return True
            if y==0: # if the intersection occurs at the leftmost side then we only need to check the cells on the right side of the letters
                if board[x-i][y+1] != blank: # if there isnt a blank on the right side of each character that is being checked then we have an illegal adjacency
                    isAdjacent = True
                    break
            elif y==19: # if the intersection occurs at the right most side of the board then we need only to check the cells on the left side of each character for an already placed letter
                if board[x-i][y-1] != blank:
                    isAdjacent = True
                    break
            elif board[x-i][y+1] != blank or board[x-i][y-1] != blank: # if we are not on one of the edge cases then both the left and right hand side cells must be checked for already placed letters
                isAdjacent = True
                break    
        for j in range(1,len(AfterIntersect)+1): # this loop will go through the positions in the board where the letters that come after the intersect would go
            if x==19:# if we are at the bottom of the board then we reach outside the grid so we just stop there
                return True
            if j == len(AfterIntersect):# if the length of the after intersect is 1 or we are at the last element then we must check that the cell in front of it is empty
                if x+j != 19:
                    if board[x+j+1][y] != blank: 
                        return True
            if j > 1: # if we are atleast two positions ahead of the intersect then we need to check if the position we are at holds the same letter as the current letter we are comparing
                if board[x+j][y] == word[IntersectIndex+j]:
                    if x+j != 19:
                        if board[x+j+1][y]!= blank: # if we have come across the same letter then we must also check that the cell in front of it is blank
                            isAdjacent = True
                            break
                        else:
                            continue
                    else:
                        continue
            else:
                if x+j != 19:# if the position we are at does not have a letter that is the same as the current letter we are at and the spot is not blank then 
                    if board[x+j][y] != blank:# we have hit an illegal adjacency
                        return True
            if y== 0:# if the intersection occurs at the leftmost side then we only need to check the cells on the right side of the letters
                if board[x+j][y+1] != blank:
                    isAdjacent = True
                    break
            elif y == 19:# if the intersection occurs at the right most side of the board then we need only to check the cells on the left side of each character for an already placed letter
                if board[x+j][y-1] != blank:
                    isAdjacent = True
                    break
            elif board[x+j][y+1] != blank or board[x+j][y-1] != blank:# if we are not on one of the edge cases then both the left and right hand side cells must be checked for already placed letters
                isAdjacent = True
                break
    else:
        LastError[word] = 'reaches outside grid'
        return True
        
    return isAdjacent

#helper function
def addvertical(board, word) : #this function adds valid words to the board vertically
    D = len(board)
    n = len(word)
    #go across the whole board looking for a common letter
    for i in range(len(board)):
        for j in range(len(board[0])):
            for k in range(len(word)):
                if word[k] == board[i][j]: # here we are checking if the current position on the board holds a letter that is in our word
                    BeforeIntersect = word[:k] #once again here we are initializing the strings that come before the intersection and after the intersection
                    AfterIntersect = word[k+1:]
                    if len(BeforeIntersect)>i+1: # these two if statements check if we exceed or boundaries
                        LastError[word] = 'reaches outside grid'
                        continue
                    if len(AfterIntersect)>19-i:
                        LastError[word] = 'reaches outside grid'
                        continue
                    else:
                        if not checkadjacentvertical(word,board,k,i,j): # if we are within the bounds then we check for adjacencies
                            if i != 19 and i != 0:
                                if board[i+1][j] != blank or board[i-1][j] != blank: # here we are checking to make sure that the letter we are intersecting with
                                    LastError[word] = 'illegal adjacencies'          # has not already been used
                                    continue
                            elif i != 19:
                                if board[i+1][j] != blank: # here we are checking to make sure that the letter we are intersecting with
                                    LastError[word] = 'illegal adjacencies'   # has not already been used
                                    continue
                            elif i != 0:
                                if board[i-1][j] != blank: # checking to make sure that the letter we are intersecting with
                                    LastError[word] = 'illegal adjacencies' # has not already been used
                                    continue
                            for p in range(len(BeforeIntersect)): # if all conditions are met then this word has found a valid position and can be placed on the board
                                board[i-p-1][j] = BeforeIntersect[len(BeforeIntersect)-p-1] # I decided to use two loops, one that adds the letters before the intersection and one that adds the letters after
                            for t in range(len(AfterIntersect)):
                                board[i+t+1][j] = AfterIntersect[t]
                            return True
                        else:
                            LastError[word] = 'illegal adjacencies'
    return False

#helper function
def checkadjacenthorizontal(word,board,IntersectIndex,x,y):#the check horizontal works based off the same logic of the check vertical
    BeforeIntersect = word[:IntersectIndex]                 # with only slight variations in what we are checking, instead of checking adjacent
    AfterIntersect = word[IntersectIndex+1:]                # columns we check adjacent rows and the edge cases will be for when the row is at the upper and lower bound rather than the column
    isAdjacent = False
    if len(BeforeIntersect) <= y+1 and len(AfterIntersect) <= 19-y: # once again we make sure the word fits within our board
        for i in range(1,len(BeforeIntersect)+1):
            if y==0:
                return True
            if i == len(BeforeIntersect):
                if y-i!= 0:
                    if board[x][y-i-1] != blank:
                        return True
            if i > 1:
                if board[x][y-i] == word[IntersectIndex-i]:
                    if y-i != 0:
                        if board[x][y-i-1] != blank:
                            isAdjacent = True
                            break
                        else:
                            continue
                    else:
                        continue
            else:
                if y-i!= 0:
                    if board[x][y-i] != blank:
                        return True
            if x== 0:
                if board[x+1][y-i] != blank:
                    isAdjacent = True
                    break
            elif x==19:
                if board[x-1][y-i] != blank:
                    isAdjacent = True
                    break
            elif board[x+1][y-i] != blank or board[x-1][y-i] != blank:
                isAdjacent = True
                break
        for j in range(1,len(AfterIntersect)+1):
            if y == 19:
                return True
            if j == len(AfterIntersect):
                if y+j!=19:
                    if board[x][y+j+1]!=blank:
                        return True
            if j > 1:
                if board[x][y+j] == word[IntersectIndex+j]:
                    if y+j != 19:
                        if board[x][y+j+1] != blank:
                            isAdjacent = True
                            break
                        else:
                            continue
                    else:
                        continue
                else:
                    if y+j != 19:
                        if board[x][y+j] != blank:
                            return True
            else:
                if board[x][y+j] != blank:
                    return True
            if x==0:
                if board[x+1][y+j] != blank:
                    isAdjacent = True
                    break 
            elif x==19:
                if board[x-1][y+j] != blank:
                    isAdjacent = True
                    break
            elif board[x-1][y+j] != blank or board[x+1][y+j] != blank:
                isAdjacent = True
                break
    return isAdjacent

#helper function
def addhorizontal(word,board): # this function adds valid words horizontally
    for i in range(len(board)): # once again the strategy is to loop through the entire board to find a position where the letter in the board is in the word we are currently trying to place
        for j in range(len(board[0])):
            for k in range(len(word)): 
                if word[k] == board[i][j]:
                    BeforeIntersect = word[:k] # initialization of the strings that come before and after the intersect
                    AfterIntersect = word[k+1:]
                    if len(BeforeIntersect) > j+1: # checking if the word fits in the board
                        LastError[word] = 'reaches outside grid'
                        continue
                    if len(AfterIntersect) > 19 - j:
                        LastError[word] = 'reaches outside grid'
                        continue
                    else:
                        if not checkadjacenthorizontal(word,board,k,i,j): # if the word fits then we check if it makes any illegal adjacencies
                            if j!= 19 and j!= 0: # these if/elif statements check that the letter we are trying to intersect with are not already being used as an intersection
                                if board[i][j+1] != blank or board[i][j-1] != blank:
                                    LastError[word] = 'illegal adjacencies'
                                    continue
                            elif j!= 19:
                                if board[i][j+1] != blank:
                                    LastError[word] = 'illegal adjacencies'
                                    continue
                            elif j!=0:
                                if board[i][j-1] != blank:
                                    LastError[word] = 'illegal adjacencies'
                                    continue
                            for p in range(len(BeforeIntersect)): # if all conditions are met then we can place the word horizontally
                                board[i][j-p-1] = BeforeIntersect[len(BeforeIntersect)-p-1] # I use two loops one that will add the letters that come before the intersection and one that adds the letters after the intersection
                            for t in range(len(AfterIntersect)):
                                board[i][j+t+1] = AfterIntersect[t]
                            return True
                        else:
                            LastError[word] = 'illegal adjacencies'
    return False

#Main Function
def crossword(L):
    board = [[blank]*20 for i in range(20)] # initialization of the board as 2D matrix filled with blanks
    while len(L[0]) > 20: # loop through the list while the first element does not fit in the board
        print(L[0],'reaches outside grid') # print the error message and discard the element
        L.pop(0)
    addfirstword(L[0],board) # Then finally once we have reached an acceptable word place it in the middle horizontally
    for i in range(1,len(L)): # loop through the list starting at the first index
        if addvertical(board,L[i]): # if the word can be added vertically place it 
            continue
        elif addhorizontal(L[i],board): # if it cannot be added vertically check if it can be added horizontally
            continue
        else: # if neither is possible then we must report an error
            IsMatch = False 
            for letter in L[i]: # loop through the word as well as the rows of the board and check if any letter is in the board
                for row in range(len(board)):
                    if letter in board[row]:
                        IsMatch = True
                        break
                if IsMatch:
                    break
            if not IsMatch: # if no letters of the word are in the board then set the last error in the dictionary to be no matches
                LastError[L[i]] = 'no matching letter'
            print(L[i],LastError[L[i]]) # then report on the error that occured last on the word
    return board # and finally we return the updated board

# code that tests crossword
printboard(crossword(['hippopotamus','rattlesnake','horse','loon','snake','cat','dinosaur']))
printboard(crossword(['eat','tap','snap']))
printboard(crossword(['turn','sack','rush','dare','self','party','kindhearted','orange','aboard','coil','hope','bolt']))
printboard(crossword(["abcdefghijklmnopqrst",
               "fffffggg",
               "ttttttttttuuuuuuuuuz",
               "yzzz",
               "qqqqqqqqqqqqqqy",
               "xxxxxxxxxaaaaaaa",
               "aaaaggg",
               "xxwwww",
               "wwwwvvvvve",
               "vvvvvvvvvvvvq",
               "mat",
               "mat",
               "make",
               "make",
               "maker",
               "remake",
               "hat"]))
