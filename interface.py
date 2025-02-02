import tkinter as tk

def show_section1():
    section2.pack_forget()
    section3.pack_forget()
    section1.pack()

def show_section2():
    section1.pack_forget()
    section3.pack_forget()
    section2.pack()

def show_section3():
    section1.pack_forget()
    section2.pack_forget()
    section3.pack()

window = tk.Tk()
window.geometry("400x400")

# Section 1: Initial content
section1 = tk.Frame(window)
label1 = tk.Label(section1, text="Welcome to Section 1!")
button_configuration = tk.Button(section1, text="Configuration", command=show_section2)
button_instructions = tk.Button(section1, text="Instructions", command=show_section3)

label1.pack()
button_configuration.pack()
button_instructions.pack()

# Section 2: Configuration content
section2 = tk.Frame(window)
label2 = tk.Label(section2, text="This is the configuration.")
button_back2 = tk.Button(section2, text="Back to Section 1", command=show_section1)

# User input placeholders (Entry widgets)
input1 = tk.Entry(section2)
input2 = tk.Entry(section2)

label2.pack()
input1.pack(fill=tk.X)
input2.pack(fill=tk.X)
button_back2.pack()

# Section 3: Instructions content
section3 = tk.Frame(window)
label3 = tk.Label(section3, text="Instructions for Use")
button_back3 = tk.Button(section3, text="Back to Section 1", command=show_section1)

label3.pack()
button_back3.pack()

# Show the initial section (Section 1)
show_section1()

window.mainloop()
