from pickle import GLOBAL
from tkinter import *
from tkinter import filedialog
from tkinter.ttk import Treeview
from db import Database
from PIL import Image, ImageTk
import numpy as np
from sklearn.cluster import KMeans
from collections import Counter
from scipy.spatial import KDTree
from webcolors import CSS3_HEX_TO_NAMES, hex_to_rgb
from colors import COLOR_FAMILIES

#Create window object
app = Tk()
app.title('HexyDB')
app.geometry('800x800')

db = Database('hexy.db')
selected_item = list(db.get_max_index())

def display_image(file):
    file = Image.open(file)
    file = resize(file)
    img_display = ImageTk.PhotoImage(file)
    img_label.configure(image=img_display)
    img_label.image = img_display

def resize(img):
    width, height = int(img.size[0]), int(img.size[1])
    if width > height:
        height = int(300/width*height)
        width = 300
    elif height > width:
        width = int(250/height*width)
        height = 250
    else:
        width, height = 250,250
    img = img.resize((width, height))
    return img

def populate_list():
    for i in hexy_list.get_children():
        hexy_list.delete(i)
    for row in db.fetch():
        hexy_list.insert('', END, values=row)

def select_item(event):
    try:
        global selected_item
        selected_item = hexy_list.focus()
        row = db.load(hexy_list.item(selected_item)['values'][0])
        #Update UI with selected row
        desc_entry.delete(0, END)
        desc_entry.insert(END, row[1])
        color_name_entry.delete(0, END)
        color_name_entry.insert(END, row[2])
        color_name_entry.configure({'background':row[4]})
        color_family_entry.delete(0, END)
        color_family_entry.insert(END, row[3])
        display_image(row[5])

    except IndexError:
        pass

def delete_hex():
    db.remove(hexy_list.item(selected_item)['values'][0])
    clear_text()
    populate_list()

def clear_text():
    desc_entry.delete(0,END)
    color_name_entry.delete(0,END)
    color_name_entry.configure({'background':'white'})
    color_family_entry.delete(0,END)

def update_hex():
    db.update(hexy_list.item(selected_item)['values'][0], desc_text.get(), color_name_text.get(), color_family_text.get())
    populate_list()

def get_color_name(rgb_tuple):
    css3_db = CSS3_HEX_TO_NAMES
    names = []
    rgb_values = []

    for color_hex, color_name in css3_db.items():
        names.append(color_name)
        rgb_values.append(hex_to_rgb(color_hex))

    kdt_db = KDTree(rgb_values)
    _, index = kdt_db.query(rgb_tuple)
    return names[index]

def import_hex():
    file = filedialog.askopenfilename(parent=app, title='Select file', filetypes=[('JPG', '*.jpg')])
    if file:
        global selected_item
        img = Image.open(file)
        #determine dominant color in image
        img_data = np.array(img.getdata())
        clt = KMeans(n_clusters=5)
        clt.fit(img_data)
        pixel_counts = Counter(clt.labels_)
        rgb_color = clt.cluster_centers_[max(pixel_counts, key=pixel_counts.get)]
        #get string name of dominant color
        color_str = get_color_name(rgb_color)
        #save img in local directory
        if db.get_max_index()[0]:
            file_index = db.get_max_index()[0] + 1
        else:
            file_index = 1
        file_path = f'Fabric/{file_index}.jpg'
        img.save(file_path)
        db.insert(f'{COLOR_FAMILIES.get(color_str)[0]} fabric', COLOR_FAMILIES.get(color_str)[0], COLOR_FAMILIES.get(color_str)[1], color_str, file_path)
        
        #update UI
        display_image(file)
        desc_entry.delete(0, END)
        desc_entry.insert(END, f'{COLOR_FAMILIES.get(color_str)[0]} fabric')
        color_name_entry.delete(0, END)
        color_name_entry.insert(END, COLOR_FAMILIES.get(color_str)[0])
        color_name_entry.configure({'background': color_str})
        color_family_entry.delete(0, END)
        color_family_entry.insert(END, COLOR_FAMILIES.get(color_str)[1])
        populate_list()
        #set selected item to be new entry
        selected_item = (db.get_max_index()[0], )
        

#Import Button
import_btn = Button(app, text='Import', command=import_hex, width=12)
import_btn.grid(row=6, column=0, pady=20)

#Update button
update_btn = Button(app, text='Update', width=12, command=update_hex)
update_btn.grid(row=6, column=1, pady=20)

#Delete button
delete_btn = Button(app, text='Delete', width=12, command=delete_hex)
delete_btn.grid(row=6, column=2, pady=20)

#Decsription Field
desc_text = StringVar()
desc_label = Label(app, text='Description:', font=('bold', 14), pady=20)
desc_label.grid(row=7, column=0, sticky=W)
desc_entry = Entry(app, textvariable=desc_text)
desc_entry.grid(row=7, column=1)

#Color Field
color_name_text = StringVar()
color_name_label = Label(app, text='Color Name:', font=('bold', 14), pady=20)
color_name_label.grid(row=8, column=0, sticky=W)
color_name_entry = Entry(app, textvariable=color_name_text)
color_name_entry.grid(row=8, column=1)

#Color Family Field
color_family_text = StringVar()
color_family_label = Label(app, text='Color Family:', font=('bold', 14), pady=20)
color_family_label.grid(row=9, column=0, sticky=W)
color_family_entry = Entry(app, textvariable=color_family_text)
color_family_entry.grid(row=9, column=1)

#DB List
columns =('id', 'description', 'color_name', 'color_family')
hexy_list = Treeview(app, columns=columns, show='headings')
hexy_list.heading('id', text='ID')
hexy_list.column('id', width=30)
hexy_list.heading('description', text='Description')
hexy_list.column('description', width=225)
hexy_list.heading('color_name', text='Color Name')
hexy_list.column('color_name', width=225)
hexy_list.heading('color_family', text='Color Family')
hexy_list.column('color_family', width=225)

hexy_list.grid(row=0, column=0, columnspan=3, rowspan=6, pady=20, padx=20)
#Build scroll bar for list
scrollbar = Scrollbar(app)
scrollbar.grid(row=0, column=3)
hexy_list.configure(yscrollcommand=scrollbar.set)
scrollbar.configure(command=hexy_list.yview)
hexy_list.bind('<<TreeviewSelect>>', select_item)

#img label
img_label = Label(app)
img_label.grid(row=7, column=2, rowspan=3)

populate_list()

#Start program
app.mainloop()