# -*- coding: utf-8 -*-
from tkinter import *
from tkinter import font as tkFont
from utils import Database, get_fancy_date
from functools import partial


def remove(string: str, to_remove: str) -> str:
    for char in to_remove:
        string = string.replace(char, '')
    return string


def nice_name(name):
    dot = name.index('.')
    return name[0].capitalize()+name[1:dot]+' '+name[dot+1].capitalize()+name[dot+2:]


def nice_data(string):
    return string.replace('\n',' ')
    while string.endswith('\n'):
        return string[:-1]
    return string


def nice_display(data):
    text = ''
    text += get_fancy_date(data[1]) + ' | '
    text += nice_data(data[2]) + ' | '
    text += nice_name(data[3])
    
    return text

#Cration de la fenetre
fenetre = Tk()
fenetre.geometry("1200x600")
fenetre.title("Christian")
fenetre.iconbitmap("christian.ico")
fenetre.grid_rowconfigure(0, weight=0)
fenetre.grid_rowconfigure(10, weight=10)
fenetre.grid_columnconfigure(0, weight=8)
fenetre.grid_columnconfigure(10, weight=10)
database = Database()
labels = []
suggestions = []
#---------------------------------------------------------------------------------------------------------------------------------
#fonction affichant infos quand option cliqué menu déroulant
def pc (labels, i):
    details = database.get_details(i)
    details = [details[k] for k in range(len(details)-1, -1, -1)][:26]
    
    while not len(labels) == 0:
        labels[0].destroy()
        del labels[0]
    
    for j in range(len(details)):
        Affichagetext = Label(fenetre, text = nice_display(details[j]))
        Affichagetext.place(x = 20, y = 80 + 20*j)
        labels.append(Affichagetext)

#Fonction recherche + création menu déroulant en fonction de la recherche
def actionEvent(labels, event):
    computers = database.get_computers(user_Entry.get())
    menuDeroulant = Menu(menuPoste)
    for i in computers:
        menuDeroulant.add_command(label=f'{i}', command = partial(pc, labels, i))
    menuPoste.configure(menu=menuDeroulant)


def set_content(entry, content):
    entry.delete(0,END)
    entry.insert(0,content)
    actionEvent(labels, None)


def test(entry, sv, suggestions):
    while len(suggestions) > 0:
        suggestions[0].destroy()
        del suggestions[0]
    
    rooms = [room for room in database.get_rooms() if room.startswith(sv.get().capitalize())]
    
    for i in range(len(rooms)):
        room = rooms[i]
        button = Button(fenetre, text = room, command=partial(set_content, entry, room))
        button.place(x=208, y=43+i*25)
        suggestions.append(button)


#---------------------------------------------------------------------------------------------------------------------------------
#création barre de saisie
sv = StringVar()
user_Entry = Entry(fenetre,bg="LemonChiffon2",textvariable=sv)
sv.trace("w", lambda name, index, mode, sv=sv: test(user_Entry, sv, suggestions))
user = Label(fenetre, text = "Salle")
user.place(x=169, y=25)
user_Entry.place(x=208, y=25)

#Définiton évènement pour recherche
user_Entry.bind("<Return>", partial(actionEvent, labels))


#création menu déroulant
menuPoste = Menubutton(text='Ordinateurs', width='20', borderwidth=2, bg='gray', activebackground='steel blue',relief = RAISED)
menuPoste.place(x=474, y=21)
#---------------------------------------------------------------------------------------------------------------------------------
#fin programme
fenetre.mainloop()