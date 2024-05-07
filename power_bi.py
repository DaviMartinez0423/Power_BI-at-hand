from tkinter.filedialog import askopenfile
import pandas as pd
import tkinter as tk
import tkinter.simpledialog as sd

class Power_Bi(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry('1200x700')
        self.config(bg='#D4D4D4')
        self.title('Power BI by a Rookie')
        self.datasets = {}  # Diccionario para almacenar los datasets cargados
        self.selected_dataset = tk.StringVar()  # Variable para almacenar el dataset seleccionado
        self.selected_dataset.trace('w', self.change_dataset)  # Configurar un rastreo para detectar cambios en el dataset seleccionado
        self.max_selections = 3  # Máximo número de opciones seleccionadas
        self.selections_count = 0  # Contador de selecciones

        self.welcome_text = tk.Label(self, text='Welcome, please insert your dataset to start', font=('Arial',15), bg='#D4D4D4')
        self.welcome_text.place(x=250, y=100)

        self.index_button = tk.Button(self, command=self.open_and_load_file, text='Insert Dataframe (csv file)', fg='black')
        self.index_button.place(x=380, y=150)

        self.columns_frame = None
        self.canvas = None
        self.scrollbar = None
        self.columns_options = []
        self.selected_options = []

    def open_and_load_file(self):
        self.welcome_text.place_forget()
        self.index_button.place_forget()

        file = askopenfile(mode='r', filetypes=[('CSV Files', '*.csv')])
        if file is not None:
            df = pd.read_csv(file)
            dataset_name = sd.askstring('New Dataset', 'Write a name for the dataset')

            if dataset_name:
                self.datasets[dataset_name] = df.columns.tolist()
                self.selected_dataset.set(dataset_name)

                # Crear el marco de los botones antes de actualizar el menú desplegable
                self.create_button_frame()
                # Actualizar el menú desplegable con los nuevos datasets
                self.dropdown_menu = tk.OptionMenu(self, self.selected_dataset, *self.datasets.keys())
                self.dropdown_menu.place(x=900, y=125)
                self.show_columns(df)

    def create_button_frame(self):
        # Crear el marco para los botones
        self.button_frame = tk.Frame(self, bg='white')

        # Crear el botón para añadir un nuevo dataset
        btn_add_dataset = tk.Button(self.button_frame, text='Insert Dataframe', command=self.open_and_load_file)
        btn_add_dataset.pack(pady=10)

        # Colocar el marco de botones en la ventana principal
        self.button_frame.place(x=900, y=80)

    def change_dataset(self, *args):
        dataset_name = self.selected_dataset.get()
        if dataset_name in self.datasets:
            df = pd.DataFrame(columns=self.datasets[dataset_name])  # Crear un DataFrame vacío con las columnas del dataset seleccionado
            self.show_columns(df)

    def show_columns(self, df):
        frame_width = 200
        
        if self.columns_frame:
            self.columns_frame.destroy()

        self.columns_frame = tk.Frame(self, bg='white', width=frame_width, height=300, bd=2, relief=tk.SUNKEN)
        self.columns_frame.place(x=900, y=175)

        self.canvas = tk.Canvas(self.columns_frame, bg='white', width=frame_width, height=300)
        self.scrollbar = tk.Scrollbar(self.columns_frame, orient='vertical', command=self.canvas.yview)
        self.scrollbar.pack(side='right', fill='y')
        self.canvas.pack(side='left', fill='both', expand=True)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        inner_frame = tk.Frame(self.canvas, bg='white')
        self.canvas.create_window((0, 0), window=inner_frame, anchor='nw')

        self.columns_table = tk.Label(inner_frame, text='Dataset Columns', font=('Arial', 12), bg='white')
        self.columns_table.pack(pady=10)
        
        for column in df.columns:
            var = tk.StringVar()
            column_option = tk.Checkbutton(inner_frame, text=column, variable=var, onvalue=column, offvalue="")
            column_option.pack(anchor=tk.W, padx=20, pady=5)
            column_option.bind('<ButtonRelease-1>', lambda event, col=column, v=var: self.limit_selections(event, column, var))
            self.columns_options.append(column_option)
            self.selected_options.append(var)

        inner_frame.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox('all'))

    def limit_selections(self, event, column, var):
        if var.get():
            self.selections_count += 1
            if self.selections_count >= self.max_selections:
                for option in self.columns_options:
                    if option.cget('text') != column:
                        option.config(state=tk.DISABLED)
        else:
            self.selections_count -= 1
            if self.selections_count < self.max_selections:
                for option in self.columns_options:
                    option.config(state=tk.NORMAL)

if __name__ == "__main__":
    Execution = Power_Bi()
    Execution.mainloop()
