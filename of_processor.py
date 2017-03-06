#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import tkinter as tk
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfilename
import codecs


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        master.minsize(width=640, height=480)

        #  content of a data file
        self.readed_lines = []
        # getting script directory
        self.script_dir = os.path.dirname(os.path.abspath(__file__))

        self.create_widgets()

    def create_widgets(self):

        # ***************** search region
        self.find_lbl = tk.Label(text="Enter piece of text to find:")
        self.find_input = tk.Entry()
        self.findBtn = tk.Button(text="FIND", fg="green",
                                 command=self.find_text)

        #  ***************** listbox region
        self.selected_lbl_caption = "Selected value: "
        self.selected_lbl = tk.Label(justify=tk.LEFT,
                                     wraplength=640,
                                     text=self.selected_lbl_caption)
        self.listbox = tk.Listbox(selectmode=tk.EXTENDED)
        self.yscrollbar = tk.Scrollbar(command=self.listbox.yview,
                                       orient=tk.VERTICAL)
        self.xscrollbar = tk.Scrollbar(command=self.listbox.xview,
                                       orient=tk.HORIZONTAL)

        self.listbox.configure(yscrollcommand=self.yscrollbar.set)
        self.listbox.configure(xscrollcommand=self.xscrollbar.set)
        self.listbox.bind('<<ListboxSelect>>', self.on_select)

        self.yscrollbar.config(command=self.listbox.yview)

        #  ***************** buttons region
        self.loadBtn = tk.Button(text="LOAD", fg="green",
                                 command=self.open_data_file)
        self.saveToBtn = tk.Button(text="SAVE", fg="blue",
                                   command=self.save_selection)
        self.quitBtn = tk.Button(text="QUIT", fg="red",
                                 command=root.destroy)

        self.grid(column=0, row=0, sticky=(tk.N, tk.S, tk.E, tk.W))

        self.find_lbl.grid(column=1, row=1, sticky=tk.W)
        self.find_input.grid(column=2, row=1, columnspan=3, sticky=tk.W + tk.E)

        self.findBtn.grid(column=5, row=1, sticky=tk.W)

        self.selected_lbl.grid(column=1, row=2, columnspan=5, rowspan=2, sticky=(tk.N, tk.S, tk.W))

        self.listbox.grid(column=1, row=4, columnspan=3, rowspan=4,
                          sticky=(tk.N, tk.S, tk.E, tk.W))
        self.yscrollbar.grid(column=4, row=4, rowspan=4,
                             sticky=tk.N + tk.S + tk.W)
        self.xscrollbar.grid(column=1, row=8, columnspan=3,
                             sticky=tk.W + tk.E + tk.N)

        self.loadBtn.grid(column=5, row=4, sticky=tk.W + tk.N)
        self.saveToBtn.grid(column=5, row=5, sticky=tk.W + tk.N)
        self.quitBtn.grid(column=5, row=6, sticky=tk.W + tk.N)

        self.find_input.configure(state='disable')
        self.findBtn.configure(state='disable')
        self.saveToBtn.configure(state='disable')

        root.rowconfigure(7, weight=1)
        root.columnconfigure(2, weight=1)

    def find_text(self):
        text_to_search = self.find_input.get()

        self.listbox.delete(0, tk.END)

        for line in self.readed_lines:
            if text_to_search.lower() in line.lower():
                self.listbox.insert(tk.END, line)

    def on_select(self, event):
        widg = event.widget
        try:
            index = int(widg.curselection()[0])
            text = self.selected_lbl_caption + self.listbox.get(index)
        except Exception as e:
            text = self.selected_lbl_caption

        self.selected_lbl['text'] = text

    def open_data_file(self):
        file_name = askopenfilename(filetypes=(("Text files", "*.txt"),
                                               ("Log files", "*.log"),
                                               ("All files", "*.*")), initialdir=self.script_dir)
        if file_name:
            try:
                self.readed_lines = []
                self.listbox.delete(0, tk.END)

                with codecs.open(file_name, "r", "utf-8") as f:
                    self.readed_lines = f.readlines()
                for single_line in self.readed_lines:
                    self.listbox.insert(tk.END, single_line)

                self.find_input.configure(state='normal')
                self.findBtn.configure(state='normal')
                self.saveToBtn.configure(state='normal')

            except Exception as e:
                print("Error while opening a file %s" % file_name)
                raise e

    def save_selection(self):
        selection_list_idx = self.listbox.curselection()
        selection_list = []
        for index in selection_list_idx:
            selection_list.append(self.listbox.get(index))

        file_name = asksaveasfilename(filetypes=(("Text files", "*.txt"),
                                                 ("Log files", "*.log"),
                                                 ("All files", "*.*")),
                                      defaultextension="txt")

        if file_name:
            try:
                with codecs.open(file_name, "w", "utf-8") as f:
                    for line in selection_list:
                        f.write(line)
            except Exception as e:
                print("Error while opening a file %s" % file_name)
                raise e


root = tk.Tk()
app = Application(master=root)

version = 1.01
app.master.title("Output files processor application. ver %5.2f" % version)

app.mainloop()
