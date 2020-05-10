class Snake:
    def __init__(self):
        self.locations=[(0,0),(1,0)]
        self.direction="r"
        self.popped=None

    def isOccupied(self,x,y):
        return (x,y) in self.locations

    def move(self, dir=None, board=None):
        last=self.locations[-1]
        moveTo=None
        if dir == None:
            dir = self.direction
        if dir=="r":
            moveTo=(last[0]+1,last[1])
            self.direction='r'
        elif dir=="l":
            moveTo=(last[0]-1,last[1])
            self.direction = 'l'
        elif dir=="u":
            moveTo=(last[0],last[1]-1)
            self.direction = 'u'
        elif dir=="d":
            moveTo=(last[0],last[1]+1)
            self.direction = 'd'

        if not (0<=moveTo[0]<len(board) and 0<=moveTo[1]<len(board)):
            return False, False

        if board[moveTo[0]][moveTo[1]] == 1:
            return False, False

        if board[moveTo[0]][moveTo[1]] == 2:
            self.eat()
            board[moveTo[0]][moveTo[1]] = 1
            return True, True

        self.locations.append(moveTo)
        self.popped = self.locations.pop(0)

        board[self.popped[0]][self.popped[1]]=0
        board[self.locations[-1][0]][self.locations[-1][1]]=1
        return True, False

    def eat(self):
        dir = self.direction
        last = self.locations[-1]
        if dir=="r":
            self.locations.append((last[0]+1,last[1]))
        elif dir=="l":
            self.locations.append((last[0]-1,last[1]))
        elif dir=="u":
            self.locations.append((last[0],last[1]-1))
        elif dir=="d":
            self.locations.append((last[0],last[1]+1))


