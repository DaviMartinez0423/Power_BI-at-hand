import tkinter as tk
from tkinter.filedialog import askopenfile
from tkinter import messagebox, simpledialog, ttk
import pandas as pd
import os
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Power_Bi(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry('1200x700')
        self.config(bg='#D4D4D4')
        self.title('Power BI by a Rookie')
        self.datasets = {}
        self.selected_dataset = tk.StringVar()
        self.selected_dataset.trace('w', self.change_dataset)
        self.max_selections = 3
        self.selections_count = 0

        self.welcome_text = tk.Label(self, text='Welcome, please insert your dataset to start', font=('Arial', 15), bg='#D4D4D4')
        self.welcome_text.place(x=200, y=100)

        self.index_button = tk.Button(self, command=self.open_and_load_file, text='Insert Dataframe (csv file)', fg='black')
        self.index_button.place(x=250, y=145)

        self.dropdown_menu = None
        self.add_dataset_button = None
        self.graphics_button = None
        self.scatter_button = None
        self.hist_button = None
        self.box_button = None

        self.columns_options = []

    def open_and_load_file(self):
        self.welcome_text.place_forget()
        self.index_button.place_forget()

        file = askopenfile(mode='r', filetypes=[('CSV Files', '*.csv')])
        if file is not None:
            file_path = file.name
            if os.path.isfile(file_path):
                df = pd.read_csv(file)
                dataset_name = simpledialog.askstring('New Dataset', 'Write a name for the dataset')

                if dataset_name:
                    self.datasets[dataset_name] = df
                    self.selected_dataset.set(dataset_name)
                    self.create_dropdown_menu()
                    self.show_columns(df)
                    if not self.add_dataset_button:
                        self.add_dataset_button = tk.Button(self, command=self.add_new_dataset, text='Add New Dataset (csv file)', fg='black')
                        self.add_dataset_button.place(x=50, y=200)
                    if not self.graphics_button:
                        self.create_graph_buttons()
                else:
                    messagebox.showerror("Error", "Dataset name cannot be empty.")

    def add_new_dataset(self):
        dataset_name = simpledialog.askstring('New Dataset', 'Write a name for the dataset')
        if dataset_name:
            file = askopenfile(mode='r', filetypes=[('CSV Files', '*.csv')])
            if file is not None:
                file_path = file.name
                if os.path.isfile(file_path):
                    df = pd.read_csv(file)
                    self.datasets[dataset_name] = df
                    self.create_dropdown_menu()
                else:
                    messagebox.showerror("Error", "Selected file path is not valid.")
        else:
            messagebox.showerror("Error", "Dataset name cannot be empty.")

    def create_dropdown_menu(self):
        if self.dropdown_menu:
            self.dropdown_menu.destroy()

        self.dropdown_menu = tk.OptionMenu(self, self.selected_dataset, *self.datasets.keys())
        self.dropdown_menu.place(x=50, y=250)

    def change_dataset(self, *args):
        dataset_name = self.selected_dataset.get()
        if dataset_name in self.datasets:
            df = self.datasets[dataset_name]
            self.show_columns(df)

    def show_columns(self, df):
        frame_width = 200
        self.columns_options = []

        columns_frame = tk.Frame(self, bg='white', width=frame_width, height=300, bd=2, relief=tk.SUNKEN)
        columns_frame.place(x=900, y=175)

        canvas = tk.Canvas(columns_frame, bg='white', width=frame_width, height=300)
        scrollbar = tk.Scrollbar(columns_frame, orient='vertical', command=canvas.yview)
        scrollbar.pack(side='right', fill='y')
        canvas.pack(side='left', fill='both', expand=True)
        canvas.configure(yscrollcommand=scrollbar.set)

        inner_frame = tk.Frame(canvas, bg='white')
        canvas.create_window((0, 0), window=inner_frame, anchor='nw')

        columns_table = tk.Label(inner_frame, text='Dataset Columns', font=('Arial', 12), bg='white')
        columns_table.pack(pady=10)
        
        for column in df.columns:
            var = tk.StringVar(value=column)
            column_option = tk.Checkbutton(inner_frame, text=column, variable=var, onvalue=column, offvalue="")
            column_option.pack(anchor=tk.W, padx=20, pady=5)
            self.columns_options.append(var)

        inner_frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox('all'))

    def create_graph_buttons(self):
        y_base_position = 300

        self.graphics_button = tk.Button(self, text='Line Plot', command=lambda: self.open_customization_window('line'))
        self.graphics_button.place(x=50, y=y_base_position)
        y_base_position += 40

        self.scatter_button = tk.Button(self, text='Scatter Plot', command=lambda: self.open_customization_window('scatter'))
        self.scatter_button.place(x=50, y=y_base_position)
        y_base_position += 40

        self.hist_button = tk.Button(self, text='Histogram', command=lambda: self.open_customization_window('hist'))
        self.hist_button.place(x=50, y=y_base_position)
        y_base_position += 40

        self.box_button = tk.Button(self, text='Box Plot', command=lambda: self.open_customization_window('box'))
        self.box_button.place(x=50, y=y_base_position)

    def open_customization_window(self, plot_type):
        customization_window = tk.Toplevel(self)
        customization_window.title(f'Customize {plot_type.capitalize()} Plot')
        customization_window.geometry('400x500')

        selected_columns = [var.get() for var in self.columns_options if var.get()]
        if not selected_columns:
            messagebox.showerror("Error", "No columns selected for plotting.")
            return
        
        tk.Label(customization_window, text="Title:").grid(row=0, column=0, sticky=tk.W)
        title_entry = tk.Entry(customization_window)
        title_entry.grid(row=0, column=1, sticky=tk.W)

        tk.Label(customization_window, text="X Label:").grid(row=1, column=0, sticky=tk.W)
        xlabel_entry = tk.Entry(customization_window)
        xlabel_entry.grid(row=1, column=1, sticky=tk.W)

        tk.Label(customization_window, text="Y Label:").grid(row=2, column=0, sticky=tk.W)
        ylabel_entry = tk.Entry(customization_window)
        ylabel_entry.grid(row=2, column=1, sticky=tk.W)

        color_var = tk.StringVar(value='blue')
        tk.Label(customization_window, text="Color:").grid(row=3, column=0, sticky=tk.W)
        ttk.Combobox(customization_window, textvariable=color_var, values=['blue', 'red', 'green', 'yellow', 'black']).grid(row=3, column=1, sticky=tk.W)

        linestyle_var = tk.StringVar(value='-')
        tk.Label(customization_window, text="Line Style:").grid(row=4, column=0, sticky=tk.W)
        ttk.Combobox(customization_window, textvariable=linestyle_var, values=['-', '--', '-.', ':']).grid(row=4, column=1, sticky=tk.W)

        marker_var = tk.StringVar(value='o')
        tk.Label(customization_window, text="Marker:").grid(row=5, column=0, sticky=tk.W)
        ttk.Combobox(customization_window, textvariable=marker_var, values=['o', 's', 'D', '^', '*']).grid(row=5, column=1, sticky=tk.W)

        linewidth_var = tk.DoubleVar(value=1.0)
        tk.Label(customization_window, text="Line Width:").grid(row=6, column=0, sticky=tk.W)
        tk.Spinbox(customization_window, from_=0.5, to=10.0, increment=0.5, textvariable=linewidth_var).grid(row=6, column=1, sticky=tk.W)

        def generate_graph():
            df = self.datasets[self.selected_dataset.get()]
            self.prepare_graph(df, selected_columns, plot_type, title_entry.get(), xlabel_entry.get(), ylabel_entry.get(), color_var.get(), linestyle_var.get(), marker_var.get(), linewidth_var.get())
            customization_window.destroy()

        def show_help():
            help_window = tk.Toplevel(customization_window)
            help_window.title('Help')
            help_window.geometry('300x200')

            help_text = (
                "Title: The title of the graph\n"
                "X Label: The label for the X-axis\n"
                "Y Label: The label for the Y-axis\n"
                "Color: Color of the plot line/points\n"
                "Line Style: Style of the plot line\n"
                "Marker: Style of the plot markers\n"
                "Line Width: Width of the plot line"
            )
            tk.Label(help_window, text=help_text, justify=tk.LEFT).pack(padx=10, pady=10)

            def close_help():
                help_window.destroy()

            tk.Button(help_window, text='Close', command=close_help).pack(pady=5)

        tk.Button(customization_window, text='Generate Graph', command=generate_graph).grid(row=7, columnspan=2, pady=10)
        tk.Button(customization_window, text='Help', command=show_help).grid(row=8, columnspan=2, pady=10)

    def prepare_graph(self, df, selected_columns, plot_type, title, xlabel, ylabel, color, linestyle, marker, linewidth):
        for column in selected_columns:
            df[column] = pd.to_numeric(df[column], errors='coerce')

        self.graphics(df, selected_columns, plot_type, title, xlabel, ylabel, color, linestyle, marker, linewidth)

    def graphics(self, df, selected_columns, plot_type, title, xlabel, ylabel, color, linestyle, marker, linewidth):
        dataset_name = self.selected_dataset.get()
        fig = Figure(figsize=(6, 4), dpi=100)
        ax = fig.add_subplot(111)

        if plot_type == 'line':
            for column in selected_columns:
                ax.plot(df[column], label=column, color=color, linestyle=linestyle, marker=marker, linewidth=linewidth)
        elif plot_type == 'scatter':
            if len(selected_columns) >= 2:
                ax.scatter(df[selected_columns[0]], df[selected_columns[1]], color=color, marker=marker)
            else:
                messagebox.showerror("Error", "Scatter plot requires at least two columns.")
                return
        elif plot_type == 'hist':
            for column in selected_columns:
                ax.hist(df[column], color=color)
        elif plot_type == 'box':
            ax.boxplot([df[column].dropna() for column in selected_columns], labels=selected_columns)

        ax.set_title(title)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.legend()

        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.draw()
        canvas.get_tk_widget().place(x=225, y=150)

if __name__ == "__main__":
    app = Power_Bi()
    app.mainloop()
