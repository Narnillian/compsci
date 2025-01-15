from tkinter import *
import model

cell_size = 5
is_running = False
speed = 100


def setup():
    global root, grid_view, cell_size, start_button, clear_button, choice

    root = Tk()
    root.title('The Game of Life')

    grid_view = Canvas(root, width=model.width*cell_size,
                             height=model.height*cell_size,
                             borderwidth=0,
                             highlightthickness=0,
                             bg='white')

    start_button = Button(root, text='Start', width=12)
    clear_button = Button(root, text='Clear', width=12)
    slowdown_button = Button(root, text='Slow Down')
    speedup_button = Button(root, text='Speed Up')

    choice = StringVar(root) 
    choice.set('Choose a Pattern')
    option = OptionMenu(root, choice, 'Choose a Pattern', 'glider', 'glider gun', 'random', command=option_handler)
    option.config(width=20)

    grid_view.grid(row=0, columnspan=3, padx=20, pady=20) #game window
    grid_view.bind('<Button-1>', grid_click_handler)

    slowdown_button.grid(row=1, column=0,columnspan=2,padx=20,pady=20) #slow down
    slowdown_button.bind('<Button-1>', slowdown_handler)
    speedup_button.grid(row=1,column=1,columnspan=2,padx=20,pady=20) #speed up
    speedup_button.bind('<Button-1>', speedup_handler)

    start_button.grid(row=2, column=0, sticky=W,padx=20, pady=20) #start button
    start_button.bind('<Button-1>', start_handler)

    option.grid(row=2, column=1, padx=20) #pattern selector

    clear_button.grid(row=2, column=2, sticky=E, padx=20, pady=20) #clear button
    clear_button.bind('<Button-1>', clear_handler)

def option_handler(event):
    global is_running, start_button, choice 

    is_running = False
    start_button.configure(text='Start')

    selection = choice.get()

    if selection == 'glider':
        model.load_pattern(model.glider_pattern, 10, 10)

    elif selection == 'glider gun':
        model.load_pattern(model.glider_gun_pattern, 10, 10)  

    elif selection == 'random':
        model.randomize(model.grid_model, model.width, model.height)

    update(False)

def start_handler(event):
    global is_running, start_button

    if is_running:
        is_running = False
        start_button.configure(text='Start')
    else:
        is_running = True
        start_button.configure(text='Pause')
        update()

def clear_handler(event):
    global is_running, start_button

    is_running = False
    for i in range(0, model.height):
        for j in range(0, model.width):
            model.grid_model[i][j] = 0

    start_button.configure(text='Start')
    update()

def grid_click_handler(event):
    global grid_view, cell_size

    x = int(event.x / cell_size)
    y = int(event.y / cell_size)
    
    if (model.grid_model[x][y] == 1):
        model.grid_model[x][y] = 0
        draw_cell(x, y, 'white')
    else:
        model.grid_model[x][y] = 1
        draw_cell(x, y, 'black')

def speedup_handler(event):
    global speed
    speed -= 10 #decrease delay
    if speed <= 0:
        speed += 10
    print(">"+str(speed))

def slowdown_handler(event):
    global speed
    speed += 10 #increase delay
    print(">"+str(speed))

def update(do_next_gen:bool = True):
    global grid_view, root, is_running

    grid_view.delete(ALL)

    if do_next_gen:
        model.next_gen()
    
    for i in range(0, model.height):
        for j in range(0, model.width):
            if model.grid_model[i][j] == 0:
                continue
            match model.grid_model[i][j]:
                case 1: color = 'green4'
                case 2: color = 'green3'
                case 3: color = 'green2'
                case 4: color = 'lawn green'
                case 5: color = 'chartreuse3'
                case 6: color = 'chartreuse2'
                case 7: color = 'green yellow'
                case 8: color = 'yellow green'
                case 9: color = 'yellow4'
                case 10: color = 'yellow3'
                case 11: color = 'yellow2'
                case 12: color = 'yellow'
                case 13: color = 'goldenrod1'
                case 14: color = 'DarkGoldenrod1'
                case 15: color = 'DarkOrange1'
                case 16: color = 'tomato'
                case 17: color = 'OrangeRed2'
                case 18: color = 'red3'
                case 19: color = 'red2'
                case _: color = 'red'
            draw_cell(i,j,color)
            #if model.grid_model[i][j] == 1:
            #    draw_cell(i, j, 'black')
            #elif model.grid_model[i][j] == 0:
            #    draw_cell(i, j, 'white')
    
    if (is_running):
       root.after(speed,update)

def draw_cell(row, col, color):
    global grid_view, cell_size

    #if color == 'black':
    outline = 'grey'
    #else:
        #outline = 'white'

    grid_view.create_rectangle(row*cell_size,
                               col*cell_size,
                               row*cell_size+cell_size,
                               col*cell_size+cell_size,
                               fill=color, outline=outline)

if __name__ == '__main__':
    setup()
    update()
    mainloop()
