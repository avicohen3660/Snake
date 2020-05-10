import time
from datetime import datetime
from tkinter import *
from PIL import Image, ImageTk
from snake import *
from pynput import keyboard
from random import randrange

fps=5
score=0
boardSize=10
board=[]
for _ in range(boardSize):
    a=[]
    for _ in range(boardSize):
        a.append(0)
    board.append(a)


alive=True
root = Tk()
root.geometry("500x550")
sprite = Image.open("snake2.png")
size=(50,50)
backgroundColor="white"
rightDown = ImageTk.PhotoImage(sprite.crop((0, 0, 64, 64)).resize(size))
leftDown = ImageTk.PhotoImage(sprite.crop((128, 0, 192, 64)).resize(size))
rightUp = ImageTk.PhotoImage(sprite.crop((0, 64, 64, 128)).resize(size))
leftUp = ImageTk.PhotoImage(sprite.crop((128, 128, 192, 192)).resize(size))
horizontal = ImageTk.PhotoImage(sprite.crop((64, 0, 128, 64)).resize(size))
vertical = ImageTk.PhotoImage(sprite.crop((128, 64, 192, 128)).resize(size))
headUp = ImageTk.PhotoImage(sprite.crop((192, 0, 256, 64)).resize(size))
headDown = ImageTk.PhotoImage(sprite.crop((256, 64, 320, 128)).resize(size))
headLeft = ImageTk.PhotoImage(sprite.crop((192, 64, 256, 128)).resize(size))
headRight = ImageTk.PhotoImage(sprite.crop((256, 0, 320, 64)).resize(size))
tailUp = ImageTk.PhotoImage(sprite.crop((256, 192, 320, 256)).resize(size))
tailDown = ImageTk.PhotoImage(sprite.crop((192, 128, 256, 192)).resize(size))
tailLeft = ImageTk.PhotoImage(sprite.crop((256, 128, 320, 192)).resize(size))
tailRight = ImageTk.PhotoImage(sprite.crop((192, 192, 256, 256)).resize(size))
apple = ImageTk.PhotoImage(sprite.crop((0,192,64,256)).resize(size))

snake = Snake()


def on_press(key):
    if key == keyboard.Key.esc:
        return False  # stop listener
    try:
        k = key.char  # single-char keys
    except:
        k = key.name  # other keys
    if k in ['left','right','up','down']:  # keys of interest
        # self.keys.append(1k)  # store it in global-like variable
        k=k[0]
        move(k)




def draw(x,y,image,size=size[0]):
    # canvas.create_rectangle(size*x,size*y,size*(x+1),size*(y+1),fill=backgroundColor, outline="")
    canvas.create_image(size*x,size*y,image=image,anchor=NW)

def drawSnake(snake):
    l = snake.popped
    if l is not None:
        canvas.create_rectangle(size[0]*l[0],size[0]*l[1],size[0]*(l[0]+1),size[0]*(l[1]+1),fill=backgroundColor, outline="")
    locs = snake.locations

    for i, node in enumerate(locs):
        if 0<i<(len(locs)-2):
            continue
        image = None
        if i == 0: #draw tail
            tail = node
            next = locs[1]
            if next[0] == tail[0]:
                if next[1] > tail[1]:
                    image = tailUp
                else:
                    image = tailDown
            else:
                if next[0] == tail[0]+1:
                    image = tailLeft
                else:
                    image = tailRight

        elif i == len(snake.locations)-1: #draw head
            head = node
            prev = locs[i-1]
            if prev[0] == head[0]:
                if prev[1] == head[1]-1:
                    image = headDown
                else:
                    image = headUp
            else:
                if prev[0] == head[0]-1:
                    image = headRight
                else:
                    image = headLeft

        else:
            prev = locs[i-1]
            next = locs[i+1]
            cur = node
            if prev[0] == next[0]:
                image = vertical
            elif prev[1] == next[1]:
                image = horizontal
            elif (prev[0] < cur[0] and next[1] > cur[1]) or next[0] < cur[0]  and prev[1] > cur[1]:
                image = leftDown
            elif (prev[0] < cur[0] and next[1] < cur[1]) or next[0] < cur[0]  and prev[1] < cur[1]:
                image = leftUp
            elif (prev[0] > cur[0] and next[1] > cur[1]) or next[0] > cur[0]  and prev[1] > cur[1]:
                image = rightDown
            elif (prev[0] > cur[0] and next[1] < cur[1]) or next[0] > cur[0]  and prev[1] < cur[1]:
                image = rightUp

        draw(node[0],node[1], image)
        root.update()


def update():
    pass


def move(dir=None,b=board):
    global alive
    global score
    alive, eat = snake.move(None,b)
    if eat:
        # print("eat")
        score+=1
        scoreLabel.configure(text=str(score))
        createFood()
    if not alive:
        return
    drawSnake(snake)
    root.update()

    # for i in range(len(board)):
    #     for j in range(len(board)):
    #         print(str(board[j][i]),end=" ")
    #     print()
    # print()

def createFood():
    x,y=randrange(10),randrange(10)
    while board[x][y] != 0:
        x,y=randrange(10),randrange(10)
    # print(x,y)
    draw(x,y,apple)
    board[x][y]=2
now=datetime.now()
# now.second

if __name__ == '__main__':

    keyPressed = False


    canvas = Canvas(root,width=500,height=500,bg=backgroundColor)
    canvas.pack()
    scoreLabel = Label(root,text=str(score),font=("",20))
    scoreLabel.pack()

    board[0][0] = 1
    board[1][0] = 1
    createFood()

    def game():
        global now
        global fps
        n=datetime.now()
        x=(n-now).microseconds//1000
        if x>300:
            fps=6
        now=n
        global keyPressed
        keyPressed=False
        move()
        if alive:
            root.after(1000//fps,game)
        else:
            print("GAME OVER")


    def handler(event):
        global keyPressed
        if not keyPressed:
            key=event.keysym
            if key in ["Right","Left","Up","Down"]:
                snake.direction=key[0].lower()
                keyPressed = True

    root.bind("<Key>", handler)
    root.after(0,game)
    root.mainloop()