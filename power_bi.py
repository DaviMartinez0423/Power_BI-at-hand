from tkinter.filedialog import askopenfile
import pandas as pd
import tkinter as tk
import matplotlib
from matplotlib.backends.backend_tkagg import  FigureCanvasTkAgg
import matplotlib.pyplot as plt

root = tk.Tk()
root.geometry('900x500')
root.config(bg='#D4D4D4')
root.title('Power BI by a Rockie')

def open_file():
    file = askopenfile(mode='r', filetypes=[('csv files', '*csv')])

initial_text = tk.Label(root, text='Welcome, please insert your dataset for start', font=('Arial',15), bg='#D4D4D4').place(x=250, y=100)

index_button = tk.Button(root, command=open_file, text='Insert Dataframe (csv file)', fg='black').place(x=370, y=150)

root.mainloop()