import tkinter as tk
from tkinter.filedialog import askopenfile
from tkinter import messagebox, simpledialog
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

        self.welcome_text = tk.Label(self, text='Welcome, please insert your dataset to start', font=('Arial',15), bg='#D4D4D4')
        self.welcome_text.place(x=250, y=100)

        self.index_button = tk.Button(self, command=self.open_and_load_file, text='Insert Dataframe (csv file)', fg='black')
        self.index_button.place(x=380, y=150)

        self.dropdown_menu = None
        self.add_dataset_button = None

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
                    self.datasets[dataset_name] = df.columns.tolist()
                    self.selected_dataset.set(dataset_name)
                    self.create_dropdown_menu()
                    self.show_columns(df)
                    if not self.add_dataset_button:
                        self.add_dataset_button = tk.Button(self, command=self.add_new_dataset, text='Add New Dataset (csv file)', fg='black')
                        self.add_dataset_button.place(x=380, y=200)
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
                    self.datasets[dataset_name] = df.columns.tolist()
                    self.create_dropdown_menu()
                else:
                    messagebox.showerror("Error", "Selected file path is not valid.")
        else:
            messagebox.showerror("Error", "Dataset name cannot be empty.")

    def create_dropdown_menu(self):
        if self.dropdown_menu:
            self.dropdown_menu.destroy()
        
        self.dropdown_menu = tk.OptionMenu(self, self.selected_dataset, *self.datasets.keys())
        self.dropdown_menu.place(x=900, y=125)

    def change_dataset(self, *args):
        dataset_name = self.selected_dataset.get()
        if dataset_name in self.datasets:
            df = pd.DataFrame(columns=self.datasets[dataset_name])
            self.show_columns(df)

    def show_columns(self, df):
        frame_width = 200
        columns_options = []

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
            var = tk.StringVar()
            column_option = tk.Checkbutton(inner_frame, text=column, variable=var, onvalue=column, offvalue="")
            column_option.pack(anchor=tk.W, padx=20, pady=5)
            columns_options.append(var)

        inner_frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox('all'))

        graphics_button = tk.Button(self, text='Graphic', command=lambda: self.prepare_graph(df, columns_options))
        graphics_button.place(x=100, y=20)

    def prepare_graph(self, df, columns_options):
        selected_columns = [var.get() for var in columns_options if var.get()]
        if selected_columns:
            for column in selected_columns:
                df[column] = pd.to_numeric(df[column], errors='coerce')

            self.graphics(df, selected_columns)
        else:
            messagebox.showerror("Error", "No columns selected for plotting.")

    def graphics(self, df, selected_columns):
        dataset_name = self.selected_dataset.get()
        fig = Figure(figsize=(6, 4), dpi=100)
        ax = fig.add_subplot(111)

        for column in selected_columns:
            ax.plot(df[column], label=column)

        ax.set_xlabel('Índice de datos')
        ax.set_ylabel('Valores')
        ax.set_title('Gráfico para dataset: {}'.format(dataset_name))
        ax.legend()

        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.draw()
        canvas.get_tk_widget().place(x=100, y=100)

if __name__ == "__main__":
    app = Power_Bi()
    app.mainloop()
