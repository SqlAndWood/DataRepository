

import os

import tkinter as tk
from tkinter import ttk, Menu, Canvas, Label


from tkinter.filedialog import askopenfilename

import OpenFile as of

class MainApplication(ttk.Frame):
    """ main class for the application """
    def __init__(self,master,*args,**kwargs):
        super().__init__(master,*args,**kwargs)

        self.my_toolbar = Toolbar(self)

        self.my_statusbar = StatusBar(self)
        self.my_statusbar.set("This is the status bar")

        self.centerframe = CenterFrame(self)

        self.menubar = MenuBar(self)

        self.pack(side=tk.TOP, expand=True, fill=tk.BOTH)

    def button_function(self, *event):
        print("Master Button Executed")


class CenterFrame(ttk.Frame):

    def __init__(self,master,*args,**kwargs):
        super().__init__(master,*args,**kwargs)

        self.master = master
        self.pack(side=tk.BOTTOM, fill=tk.X)
        self.centerlabel = ttk.Label(self, text="text goes here: refer to Center Frame")
        self.centerlabel.pack()


class StatusBar(ttk.Frame):
    """ Simple Status Bar class - based on Frame """
    def __init__(self,master):
        ttk.Frame.__init__(self,master)

        self.master = master
        self.label = ttk.Label(self,anchor=tk.W)
        self.label.pack()
        self.pack(side=tk.BOTTOM, fill=tk.X)

    def set(self,texto):
        self.label.config(text=texto)
        self.label.update_idletasks()

    def clear(self):
        self.label.config(text="")
        self.label.update_idletasks()


class Toolbar(ttk.Frame):
    """ Toolbar """
    def button_one(self):
        print("button 1 pressed")

    def button_two(self):
        print("button 2 pressed")
        self.master.button_function()


    def __init__(self,master):
        super().__init__(master)

        self.master = master
        self.pack(side=tk.TOP, fill=tk.X)

        self.button1 = ttk.Button(self,text="One",command=self.button_one)
        self.button2 = ttk.Button(self,text="Two",command=self.button_two)

        self.button1.grid(row=0,column=0)
        self.button2.grid(row=0,column=1)

class MenuBar(ttk.Frame):

    def Presentation(self, column_headings):

        # https://subscription.packtpub.com/book/web_development/9781788622301/1/ch01lvl1sec19/displaying-a-list-of-items
        for item in column_headings:
            w = Label(root, text=item)
            w.pack()

    def OpenFile(self):
        print("Open File selected")
        self.master.button_function()

        mapping_folder_path = os.path.abspath(os.path.dirname("."))

        file_name_and_path = askopenfilename(
                                                initialdir=mapping_folder_path,
                                                filetypes=(
                                                            ("Text File", "*.csv"),
                                                            ("All Files", "*.*")
                                                            ),
                                                title="Choose a file."
                                             )

        # label = ttk.Label(root, text=file_name_and_path, foreground="black", font=("Helvetica", 12))
        # label.pack()

        file_name = file_name_and_path[len(mapping_folder_path) + 1:len(file_name_and_path)]

        # Using try in case user types in unknown file or closes without choosing a file.
        try:
            print('about to process data')
            column_headings =   of.ObtainFileHeader(file_name_and_path)
            self.Presentation(column_headings)

            # CreateData(file_name, file_name_and_path, mapping_folder_path)
            # print('completed with the data')
        except:
            print("No file exists")

    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.master = master
        self.pack(side=tk.TOP, fill=tk.X)

        canvas = Canvas(width=300, height=200, bg='white')
        canvas.pack(expand = "YES")

        menu = Menu(root)
        root.config(menu=menu)

        self.file = Menu(menu)

        menu.add_cascade(label='File', menu=self.file)

        self.file.add_command(label='Open', command= self.OpenFile )
        self.file.add_command(label='Exit', command=lambda: exit())


if __name__ == "__main__":
    root = tk.Tk()
    app = MainApplication(root)
    root.mainloop()