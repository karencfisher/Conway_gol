from tkinter import *
import _thread, time


class Colony():

    def __init__(self, cols, rows):
        self.Cols = cols
        self.Rows = rows
        self.Colony = [[0 for i in range(cols)] for j in range(rows)]
        
        # default Conway game rules
        self.birth = (3,)
        self.survive = (2,3)
        

    def paint(self, canvas):
        color = ('beige','red')
        self.canvas = canvas
        canvas.create_rectangle(0, 0, self.Cols * 10, self.Rows * 10, fill='beige', outline='')
        for j in range(0, len(self.Colony)):
            for i in range(0, len(self.Colony[j])):   
                y = j * 10 + 2
                x = i * 10 + 2
                value = self.Colony[j][i]
                canvas.create_rectangle(x, y, x + 8, y + 8, fill=color[value])    

    def clear(self):
        for j in range(0, len(self.Colony)):
            for i in range(0,len(self.Colony[j])):
                self.Colony[j][i] = 0
                

    def update_cell(self, x, y, pixels=True):
        color = ('beige','red')
        if pixels:
            x = x // 10
            y = y // 10
        if self.Colony[y][x] == 1:
            self.Colony[y][x] = 0
        else:
            self.Colony[y][x] = 1
        
        j = y * 10 + 2
        i = x * 10 + 2
        value = self.Colony[y][x]
        self.canvas.create_rectangle(i, j, i + 8, j + 8, fill=color[value])
        
        
    def setRules(self, birth, survive):
        self.birth = birth
        self.survive = survive
        
    
    def evolve(self):
        # tbd
        changes=[]
        for j in range(0, len(self.Colony)):
            for i in range(0, len(self.Colony[j])):
                count = 0
                offsets = ((-1, -1),(-1, 0), (-1,1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
                for offset in offsets:
                    try:
                        count += self.Colony[j+offset[0]][i+offset[1]]
                    except IndexError:
                        pass
                if self.Colony[j][i] == 1 and count not in self.survive:
                    changes.append((j,i))
                elif self.Colony[j][i] == 0 and count in self.birth:
                    changes.append((j,i))       
        for change in changes:
            self.update_cell(change[1], change[0], pixels=False)
        return len(changes)
    
                
                
class Application(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.init_window()
        self.flag = False

    def init_window(self):

        self.master.title("Conway Game of Life")

        self.pack(fill=BOTH, expand=1)

        menu = Menu(self.master)
        self.master.config(menu=menu)
        
        file = Menu(menu)
        file.add_command(label='Exit', command=self.client_exit)
        menu.add_cascade(label='File', menu=file)

        edit = Menu(menu)
        edit.add_command(label="Evolve", command=self.evolve)
        edit.add_command(label="Stop", command=self.stop)
        edit.add_command(label="Clear", command=self.clear)
        menu.add_cascade(label='Edit', menu=edit)

        self.width = 100
        self.height = 100

        self.canvas = Canvas(self, width=self.width * 10 + 2, height=self.height * 10 + 2)
        self.canvas.bind("<Button-1>", self.mouseclick)
        self.canvas.pack()

        self.colony = Colony(self.width, self.height)
        self.colony.paint(self.canvas)

    def mouseclick(self, event):
        self.colony.update_cell(event.x, event.y)

    def evolve(self):
        self.flag = True
        _thread.start_new_thread(self.evolution, ())

    def evolution(self):
        mutations = 1
        while self.flag and mutations > 0:
            mutations = self.colony.evolve()
            time.sleep(.5)

    def stop(self):
        self.flag = False

    def clear(self):
        self.colony.clear()
        self.colony.paint(self.canvas)

    def client_exit(self):
        self.master.destroy()                    

        
def main():              
    root = Tk()
    app= Application(root)
    app.mainloop()


if __name__ == '__main__':
    main()



