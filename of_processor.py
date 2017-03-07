#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import tkinter as tk
from tkinter.ttk import *
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfilename
import codecs
import configparser
import logging


class StatusBar(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.label_status = tk.Label(self, bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.label_status.grid(row=0, column=0,
                               sticky=(tk.W, tk.E))

    def set(self, format, *args):
        self.label_status.config(text=format % args)
        self.label_status.update_idletasks()

    def clear(self):
        self.label_status.config(text="")
        self.label_status.update_idletasks()


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.grid()
        master.minsize(width=640, height=480)
        self.menu_bar = tk.Menu(master)
        master.configure(menu=self.menu_bar)

        #  content of a data file
        self.readed_lines = []
        # getting script directory
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.search_tpl_list = []

        self.create_widgets()

    def create_widgets(self):
        # ***************** menu
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)

        self.file_menu.add_command(label="Load conf", command=self.load_config)
        self.file_menu.add_command(label="Quit", command=root.destroy)

        # ***************** search region
        self.str_var_entry_find = tk.StringVar()

        self.label_enter_text_to_find = tk.Label(text="Enter text to find:")
        self.entry_text_to_find = tk.Entry(textvariable=self.str_var_entry_find)
        self.button_find = tk.Button(text="FIND", fg="green",
                                     command=self.find_text,
                                     width=6, height=1)

        #  ***************** listbox region
        self.label_with_selected_text_caption = "Selected value: "
        self.label_with_selected_text = tk.Label(justify=tk.LEFT,
                                                 wraplength=640,
                                                 text=self.label_with_selected_text_caption)
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
        self.str_var_combobox = tk.StringVar()

        self.combobox_search_tpl = tk.ttk.Combobox(state="readonly",
                                                   textvariable=self.str_var_combobox,
                                                   values=self.search_tpl_list)

        self.combobox_search_tpl.bind("<<ComboboxSelected>>",
                                      self.update_search_entry_on_cmtpl)

        self.button_load = tk.Button(text="LOAD", fg="green",
                                     command=self.open_data_file,
                                     width=6, height=1)
        self.button_save_to = tk.Button(text="SAVE", fg="blue",
                                        command=self.save_selection,
                                        width=6, height=1)
        self.button_quit = tk.Button(text="QUIT", fg="red",
                                     command=root.destroy,
                                     width=6, height=1)

        self.status_bar = StatusBar(self.master)

        # ***************** display it all
        self.grid(column=0, row=0, sticky=(tk.N, tk.S, tk.E, tk.W))

        self.label_enter_text_to_find.grid(column=1, row=1, sticky=tk.W)
        self.entry_text_to_find.grid(column=2, row=1, columnspan=3,
                                     sticky=tk.W + tk.E)

        self.button_find.grid(column=5, row=1, sticky=tk.W,
                              padx=3, pady=3)

        self.label_with_selected_text.grid(column=1, row=2,
                                           columnspan=5, rowspan=2,
                                           sticky=(tk.N, tk.S, tk.W))

        self.listbox.grid(column=1, row=4, columnspan=3, rowspan=4,
                          sticky=(tk.N, tk.S, tk.E, tk.W))
        self.yscrollbar.grid(column=4, row=4, rowspan=4,
                             sticky=tk.N + tk.S + tk.W)
        self.xscrollbar.grid(column=1, row=8, columnspan=3,
                             sticky=tk.W + tk.E + tk.N)

        self.button_load.grid(column=5, row=4, sticky=tk.W + tk.N,
                              padx=3, pady=3)
        self.button_save_to.grid(column=5, row=5, sticky=tk.W + tk.N,
                                 padx=3, pady=3)
        self.button_quit.grid(column=5, row=6, sticky=tk.W + tk.N,
                              padx=3, pady=3)

        self.combobox_search_tpl.grid(column=5, row=7, sticky=tk.W + tk.N,
                                      padx=3, pady=3)

        self.status_bar.grid(column=1, row=9, columnspan=5,
                             sticky=(tk.W, tk.E))

        self.set_widgets_status('disable', 'disable')

        root.rowconfigure(7, weight=1)
        root.columnconfigure(2, weight=1)

    def set_widgets_status(self, status, cb_status):
        self.entry_text_to_find.configure(state=status)
        self.button_find.configure(state=status)
        self.button_save_to.configure(state=status)
        self.button_find.configure(state=status)
        self.combobox_search_tpl.configure(state=cb_status)

    def find_text(self):
        text_to_search = self.entry_text_to_find.get()

        self.listbox.delete(0, tk.END)

        counter = 0

        for line in self.readed_lines:
            if text_to_search.lower() in line.lower():
                self.listbox.insert(tk.END, line)
                counter += 1

        self.status_bar.set("%s lines was found" % counter)

    def on_select(self, event):
        widg = event.widget
        try:
            index = int(widg.curselection()[0])
            text = self.listbox.get(index)
        except Exception as e:
            text = ''
        text = self.label_with_selected_text_caption + text

        self.label_with_selected_text['text'] = text

    def open_data_file(self):
        file_name = askopenfilename(filetypes=(("Text files", "*.txt"),
                                               ("Log files", "*.log"),
                                               ("All files", "*.*")),
                                    initialdir=self.script_dir)
        if file_name:
            try:
                self.readed_lines = []
                self.listbox.delete(0, tk.END)

                with codecs.open(file_name, "r", "utf-8") as f:
                    self.readed_lines = f.readlines()
                for single_line in self.readed_lines:
                    self.listbox.insert(tk.END, single_line)

                self.set_widgets_status('normal', 'readonly')

                self.status_bar.set("Loaded %s lines" % len(self.readed_lines))
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
                self.status_bar.set("Saved %s lines" % len(selection_list))
            except Exception as e:
                print("Error while opening a file %s" % file_name)
                raise e

    def load_config(self):
        self.search_tpl_list = []
        config = configparser.ConfigParser()

        conf_file_name = askopenfilename(filetypes=(("Conf files", "*.conf"),
                                                    ("All files", "*.*")))

        if conf_file_name:
            try:
                logging.debug("Opening %s file" % conf_file_name)
                config.read(conf_file_name)
            except Exception as e:
                print("Error reading {} file".format(conf_file_name))
                logging.error("Error reading %s file" % conf_file_name)
                raise e
        try:
            self.search_tpl_list = config['USER_SETTINGS']['Searches'].split(',')
        except Exception as e:
            logging.error("Error reading ['USER_SETTINGS']['Searches']\
                           in %s file" % conf_file_name)
            pass

        self.combobox_search_tpl['values'] = self.search_tpl_list

        return self.search_tpl_list

    def update_search_entry_on_cmtpl(self, event):
        self.str_var_entry_find.set(self.str_var_combobox.get())


logging.basicConfig(filename='of_processor.log',
                    level=logging.ERROR,
                    format='%(asctime)s - %(levelname)s - %(lineno)d - %(message)s')


root = tk.Tk()
app = Application(master=root)

version = 1.12
app.master.title("Output files processor application. ver %5.2f" % version)

app.mainloop()
