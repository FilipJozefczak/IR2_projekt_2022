import tkinter as tk
from tkinter import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
NavigationToolbar2Tk)
from tkinter import messagebox
from tkinter import filedialog
from PIL import Image, ImageTk

filenameInt = None
filenameCzas = None
isPlotGenerated = False
canvas = None
toolbar = None



def openFileInt(): #funkcja otwiera plik tekstowy int, oraz przydziela dane z kazdej kolumny do odpowiednich list danych
    global filenameInt
    filenameInt = filedialog.askopenfilename()
    file = open(filenameInt,'r')
    data = file.read().replace(",", ".").split()
    global minutes_from_file
    global call_intensity
    minutes_from_file=[]
    call_intensity=[]
    for i in range(len(data)):
        if i%2:
            call_intensity.append(float(data[i]))
        else:
            minutes_from_file.append(float(data[i]))
    for i in range(1, 1440):
        if i not in minutes_from_file:
            minutes_from_file.insert(i-1, float(i))
            call_intensity.insert(i - 1, 0.0)

def openFileCzas(): #funkcja otwiera plik czas oraz oblicza średni czas na podstawie danych w nim zawartych
    global filenameCzas
    global avg_time
    filenameCzas = filedialog.askopenfilename()
    file = open(filenameCzas, 'r')
    data = file.read().split()
    avg_time = sum([int(i) for i in data])/len(data)

def generate(): #funkcja odpowiada za wygenerowanie wykresu oraz obsługę błędów (błędne dane wprowadzone przez użytkownika itp)
    global canvas
    global toolbar
    global isPlotGenerated
    if filenameInt and filenameCzas:
        fig = Figure(figsize = (10,5), dpi = 100)
        plot = fig.add_subplot(111)

        try:
            number = float(input1.get(1.0, "end-1c"))
        except ValueError:
            messagebox.showerror('Wpisano zły zakres minut w dobie!',  'Proszę wybierz zakres z przedziału <1, 1439>')
        try:
            number = float(input2.get(1.0, "end-1c"))
        except ValueError:
            messagebox.showerror('Wpisano zły zakres minut w dobie!', 'Proszę wybierz zakres z przedziału <1, 1439>')

        in1 = float(input1.get(1.0, "end-1c"))
        in2 = float(input2.get(1.0, "end-1c"))

        try:
            if in1 < 1 or in1 > in2 or in2 < in1 or in2 > 1439:
                raise ValueError("Wartości in1 i in2 są niepoprawne")
        except ValueError as error:
            messagebox.showerror('Wpisano zły zakres minut w dobie!', 'Proszę wybierz zakres z przedziału <1, 1439>')

        index1 = minutes_from_file.index(in1)
        index2 = minutes_from_file.index(in2)

        plot.plot(minutes_from_file[index1:index2],
                  [float(i*avg_time) for i in call_intensity[index1:index2]])
        plot.set_xlabel('Minuty w dobie')
        plot.set_ylabel('Średnie natęzenie ruchu telekomunikacyjnego [Erlang]')

        isPlotGenerated = True
        if canvas:
            canvas.get_tk_widget().pack_forget()
            toolbar.pack_forget()

        canvas = FigureCanvasTkAgg(fig, master = window)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, )
        toolbar = NavigationToolbar2Tk(canvas)
        toolbar.update()
        canvas.get_tk_widget().pack()

    else:
        messagebox.showerror("Nie wybrano plików!", "Wybierz odpowiednie pliki z danymi i spróbuj ponownie")

def new_window(file_path, title, parent):
    window_info = tk.Toplevel(parent)
    window_info.title(title)
    window_info.image = Image.open(file_path)
    window_info.photo = ImageTk.PhotoImage(window_info.image)
    label = tk.Label(window_info, image=window_info.photo)
    label.pack()


if __name__ == "__main__": #funkcja main, główne okno aplikacji, przyciski
    window = Tk()
    window.title('Projekt')
    window.configure(bg='lightgrey')
    window.geometry("700x700")

    input1 = tk.Text()
    input1.place(relx=0.15, rely=0.1, relheight=0.05, relwidth=0.1)
    input1.insert(tk.END, '1')
    input2 = tk.Text()
    input2.place(relx=0.27, rely=0.1, relheight=0.05, relwidth=0.1)
    input2.insert(tk.END, '1439')

    openfileInt_button = Button(text="Otwórz int", command=openFileInt)
    openfileInt_button.place(relx=0.15, rely=0.03, relheight=0.05, relwidth=0.1)
    openfileCzas_button = Button(text="Otwórz czas", command=openFileCzas)
    openfileCzas_button.place(relx=0.27, rely=0.03, relheight=0.05, relwidth=0.1)

    generate_button = Button(text="Generuj", command=generate, bg='green2')
    generate_button.place(relx=0.42, rely=0.06, relheight=0.05, relwidth=0.2)

    info1_button = Button(text="Pomoc", command=lambda:
    new_window("pomoc.png", "Pomoc", window))
    info1_button.place(relx=0.65, rely=0.06, relheight=0.05, relwidth=0.1)

    info2_button = Button(text="Teoria", command=lambda:
    new_window("teoria.png", "Teoria", window))
    info2_button.place(relx=0.75, rely=0.06, relheight=0.05, relwidth=0.1)

    window.mainloop()

