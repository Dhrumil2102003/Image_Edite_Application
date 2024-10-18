from tkinter import *
import tkinter as tk
import tkinter.filedialog as tk_file
from tkinter.colorchooser import askcolor
from PIL import Image, ImageTk, ImageDraw

root = Tk()
root.title("Paint")
root.geometry("1000x600")

stroke_size = IntVar()
stroke_size.set(1)

# Create stroke_color
stroke_color = StringVar()
stroke_color.set("black")

# Image store and open variable
open_image = ''
img_path = ''
edited_image = ''
draw = None  # Initialize drawing object
image_height = 0
image_width = 0
rect_id = None
start_x = start_y = 0 

# Create save image function
def save_image():
    global edited_image  # Ensure you're using the global variable
    if edited_image:
        file_name = tk_file.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), 
                                                                                  ("JPG files", "*.jpg"), 
                                                                                  ("JPEG files", "*.jpeg"), 
                                                                                  ("All files", "*.*")])
        if file_name:
            edited_image.save(file_name)  # Save the edited image

# Create clear function
def clear_image():
    global open_image, edited_image, img_path

    if img_path: 
        opened_image = Image.open(img_path)
        edited_image = opened_image.copy()  
        open_image = ImageTk.PhotoImage(opened_image) 
        canvas.delete("all")  
        canvas.create_image(0, 0, anchor=tk.NW, image=open_image)  

# Create open function
def open_image_file():
    global open_image, img_path, image_height, image_width, edited_image, draw  # Include draw here

    img_path = tk_file.askopenfilename()
    if img_path:
        opened_image = Image.open(img_path)
        edited_image = opened_image.copy()  
        draw = ImageDraw.Draw(edited_image)  # Initialize drawing object
        image_height = opened_image.height
        image_width = opened_image.width
        open_image = ImageTk.PhotoImage(opened_image)
        canvas.config(width=image_width, height=image_height)
        frame2.config(width=image_width, height=image_height)
        canvas.config(scrollregion=canvas.bbox("all"))  
        canvas.delete("all")
        canvas.create_image(0, 0, anchor=tk.NW, image=open_image)

# Add frame to tkinter
frame1 = Frame(root, height=100, width=1100)
frame1.grid_forget()

# Create tool frame
toolFrame = Frame(frame1, height=100, width=100, relief=SUNKEN, borderwidth=3)
toolFrame.grid(row=0, column=0)

# Create pencil function
def usepencil():
    stroke_color.set("black")
    canvas['cursor'] = 'pencil'

# Load an image for pencil icon
img = Image.open("C:/Users/ADMIN/Music/project/image/icon/pencil.png")
img = img.resize((20, 20))
icon = ImageTk.PhotoImage(img)

# Create pencil
pencilButton = Button(toolFrame, width=20, height=20,command=usepencil,bg="white",image=icon)
pencilButton.grid(row=0, column=0)

# Create Tool Label
toolsLabel = Label(toolFrame, text="Tools", width=10, bg="white")
toolsLabel.grid(row=2, column=0)

# Create Size Frame
sizeFrame = Frame(frame1, height=100, width=100, relief=SUNKEN, borderwidth=3)
sizeFrame.grid(row=0, column=1)

# Create default button
defaulteButton = Button(sizeFrame, text="Default", width=10)
defaulteButton.grid(row=0, column=0)

options = [1, 2, 3, 4, 5, 10]

# Create drop-down menu for size
sizeList = OptionMenu(sizeFrame, stroke_size, *options)
sizeList.grid(row=1, column=0)

# Create size Label
sizeLabel = Label(sizeFrame, text="Size", width=10, bg="white")
sizeLabel.grid(row=2, column=0)

# Create color box frame
colorBoxFrame = Frame(frame1, height=100, width=100, relief=SUNKEN, borderwidth=3)
colorBoxFrame.grid(row=0, column=2)

# Create crop function to crop the image 
def crop_image_with_mouse(left, top, right, bottom):
    global edited_image, open_image
    
    edit_img = Image.open(img_path)
    edited_image = edit_img.crop((left, top, right, bottom))
    open_image = ImageTk.PhotoImage(edited_image)
    canvas.delete("all")  
    canvas.create_image(0, 0, anchor=tk.NW, image=open_image)

def start_crop(event):
    global start_x, start_y, rect_id
    start_x, start_y = event.x, event.y
    if rect_id:
        canvas.delete(rect_id) 
    rect_id = canvas.create_rectangle(start_x, start_y, start_x, start_y, outline='red')

def update_crop_area(event):
    global rect_id
    canvas.coords(rect_id, start_x, start_y, event.x, event.y)

def end_crop(event):
    global start_x, start_y, rect_id
    x1, y1, x2, y2 = start_x, start_y, event.x, event.y
    left = min(x1, x2)
    right = max(x1, x2)
    top = min(y1, y2)
    bottom = max(y1, y2)
    
    crop_image_with_mouse(left, top, right, bottom)

def SelectColor():
    selectedColor = askcolor(title="Select Color")
    if selectedColor[1]:  # If a color is selected
        stroke_color.set(selectedColor[1])

# Create select color button
colorBoxButton = Button(colorBoxFrame, text="Select Color", width=10, command=SelectColor)
colorBoxButton.grid(row=0, column=0)

frame2 = Frame(root, bg="yellow")
frame2.grid(row=1, column=0)

# Add canvas 
canvas = Canvas(frame2, bg="white")
canvas.grid(row=0, column=0, sticky="nsew")

# Variable for pencil 
prvPoint = [0, 0]
currentPoint = [0, 0]

# Create the paint function and bind it
def paint(event):
    global prvPoint, currentPoint, draw  # Include draw in the scope
    x = event.x
    y = event.y
    currentPoint = [x, y]

    if prvPoint != [0, 0]:  # Only draw if there's a previous point
        # Draw on the canvas (for visual feedback)
        canvas.create_polygon(prvPoint[0], prvPoint[1], currentPoint[0], currentPoint[1],
                           fill=stroke_color.get(), width=stroke_size.get())

        # Draw on the edited_image
        draw.polygon([prvPoint[0], prvPoint[1], currentPoint[0], currentPoint[1]],
                   fill=stroke_color.get(), width=stroke_size.get())

    prvPoint = currentPoint

    # Reset starting point when mouse is released
    if event.type == "5":  # Event type 5 corresponds to ButtonRelease-1
        prvPoint = [0, 0]

# Show and hide brush
def toggle_frame():
    if frame1.winfo_ismapped():
        frame1.grid_forget()
    else:
        frame1.grid(row=0, column=0, sticky="nw")

# Create menu bar
menu_bar = tk.Menu(root)

file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label='Open', command=open_image_file)
file_menu.add_command(label='Save', command=save_image)
file_menu.add_command(label='Clear', command=clear_image)

menu_bar.add_cascade(label='File', menu=file_menu)

menu_bar.add_command(label='Crop', command=lambda: (canvas.bind("<ButtonPress-1>", start_crop), 
                                                     canvas.bind("<B1-Motion>", update_crop_area), 
                                                     canvas.bind("<ButtonRelease-1>", end_crop),
                                                   canvas.config(cursor="crosshair")))

menu_bar.add_command(label='Brush', command=lambda: (canvas.bind("<B1-Motion>", paint),
                                                     canvas.bind("<ButtonRelease-1>", paint),
                                                    toggle_frame()))

root.config(menu=menu_bar)

#root.resizable(False,False)
root.mainloop()
