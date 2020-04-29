from tkinter import *
from tkinter.filedialog import asksaveasfilename, askopenfilename
from tkinter.simpledialog import askstring
import _thread, time


class Colony():

    def __init__(self, cols, rows):
        self.canvas = None
        self.viewport = None
        
        self.Cols = cols
        self.Rows = rows
        self.Colony = [[0 for i in range(cols)] for j in range(rows)]
        
        self.survive = [2, 3]
        self.birth = [3]
        
        self.initial_colony = []
        self.rectangles = {}
        

    def paint(self, canvas=None):
        color = ('beige','red')
        
        if not canvas == None:
            self.canvas = canvas
            
        if self.viewport == None:
            self.viewport = self.canvas.create_rectangle(0, 0, self.Cols * 10, 
                                    self.Rows * 10, fill='beige', outline='')
        else:
            for value in self.rectangles.values():
                self.canvas.delete(value)
            self.rectangles.clear()
        for j in range(0, len(self.Colony)):
            for i in range(0, len(self.Colony[j])):   
                y = j * 10 + 2
                x = i * 10 + 2
                value = self.Colony[j][i]
                key = str(j) + str(i)
                rect = self.canvas.create_rectangle(x, y, x + 8, y + 8, \
                                                    fill=color[value])
                if value == 1:
                    self.rectangles[key] = rect
                

    def clear(self, reset=False):
        for j in range(0, len(self.Colony)):
            for i in range(0,len(self.Colony[j])):
                self.Colony[j][i] = 0
        if reset:
            self.initial_colony.clear()
        self.paint()
        
    
    def set_rules(self, survive, birth):
        self.survive = survive
        self.birth = birth
        
        
    def get_rules(self):
        return (self.survive, self.birth)
    
        
    def set_initial_colony(self, colony):
        self.initial_colony = colony
        
        
    def get_initial_colony(self):
        return self.initial_colony
        
        
    def restore_initial_colony(self):
        self.clear()
        for cell in self.initial_colony:
            self.Colony[cell[1]][cell[0]] = 1
        self.paint()
                

    def update_cell(self, x, y, pixels=True):
        color = ('beige','red')
        if pixels:
            x = x // 10
            y = y // 10
        if self.Colony[y][x] == 1:
            self.Colony[y][x] = 0
            if pixels:
                self.initial_colony.remove((x, y))
        else:
            self.Colony[y][x] = 1
            if pixels:
                self.initial_colony.append((x, y))
        
        j = y * 10 + 2
        i = x * 10 + 2
        value = self.Colony[y][x]
        key = str(y) + str(x)
        if self.rectangles.get(key, None) == None:
            self.rectangles[key] = self.canvas.create_rectangle(i, j, i + 8, \
                           j + 8, fill=color[value])
        else:
            self.canvas.delete(self.rectangles[key])
            self.rectangles.pop(key, 0)
             

    def evolve(self):
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

        self.master.title("Conway's Game of Life")

        self.pack(fill=BOTH, expand=1)

        menu = Menu(self.master)
        self.master.config(menu=menu)
        
        file = Menu(menu)
        file.add_command(label='Open...', command=self.load)
        file.add_command(label='Save...', command=self.store)
        file.add_command(label='Exit', command=self.client_exit)
        menu.add_cascade(label='File', menu=file)

        edit = Menu(menu)
        edit.add_command(label="Evolve", command=self.evolve)
        edit.add_command(label="Stop", command=self.stop)
        edit.add_command(label="Revert", command=self.revert)
        edit.add_command(label="Clear", command=self.clear)
        edit.add_command(label="Edit rules...", command=self.editrules)
        menu.add_cascade(label='Edit', menu=edit)

        self.width = 100
        self.height = 100

        self.canvas = Canvas(self, width=self.width * 10 + 2, height=self.height * 10 + 2)
        self.canvas.bind("<Button-1>", self.mouseclick)
        self.canvas.pack()

        self.colony = Colony(self.width, self.height)
        self.colony.paint(self.canvas)
        
        
    def store(self):
        colony = self.colony.get_initial_colony()
        filename = asksaveasfilename(filetypes=[('GOL files', '*.gol'), 
                                                    ('Text files', '*.txt')],
                                    defaultextension=[('GOL file', '*.gol')])
        if filename == '':
            return
        
        with open(filename, 'w') as filehandle:
            for item in colony:
                filehandle.write('%s\n' % str(item))
            filehandle.close()
            
    
    def load(self):
        colony = []
        filename = askopenfilename(filetypes=[('GOL files', '*.gol'),                                             ('Text files', '*.txt')])
        if filename == '':
            return
        
        with open(filename, 'r') as filehandle:
            for line in filehandle:
                item = line[:-1]
                items = item.strip('()').split(', ')
                colony.append((int(items[0]), int(items[1])))
            filehandle.close()
        
        self.colony.set_initial_colony(colony)
        self.colony.restore_initial_colony()
        
    
    def revert(self):
        self.colony.restore_initial_colony()
        
    
    def editrules(self):
        rules = self.colony.get_rules()
        string = f'{rules[0]}|{rules[1]}'
        answer = askstring(title='Rules', 
            prompt='Number of neighbors allowing a cell to (survive)|(born).', 
                            initialvalue=string)
        print(answer)
        if answer == None:
            return
        
        newrules = answer.split('|')
        survive = newrules[0].split(', ')
        birth = newrules[1].split(', ')
        survive = [int(item.strip('[]')) for item in survive]
        birth = [int(item.strip('[]')) for item in birth]

        self.colony.set_rules(survive, birth)
        

    def mouseclick(self, event):
        self.colony.update_cell(event.x, event.y)

    def evolve(self):
        self.flag = True
        self.evolve_thread = _thread.start_new_thread(self.evolution, ())

    def evolution(self):
        mutations = 1
        while self.flag and mutations > 0:
            mutations = self.colony.evolve()
            time.sleep(.25)

    def stop(self):
        self.flag = False

    def clear(self):
        self.colony.clear(reset=True)

    def client_exit(self):
        self.flag = False       
        self.master.destroy()                    

        
def main():              
    root = Tk()
    app= Application(root)
    app.mainloop()


if __name__ == '__main__':
    main()



