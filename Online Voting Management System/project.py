import tkinter  
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import simpledialog
from tkinter import filedialog as fd
import sqlite3 as sqltor
import matplotlib.pyplot as plt

# Database setup
conn = sqltor.connect('main.db')  # main database
cursor = conn.cursor()  # main cursor
cursor.execute("""CREATE TABLE IF NOT EXISTS poll (name)""")

# Global font and color settings
BG_COLOR = "#34495E"
FG_COLOR = "#ECF0F1"
BTN_BG = "#3498DB"
BTN_FG = "#FFFFFF"
FONT_HEADER = ("Helvetica", 14, "bold")
FONT_NORMAL = ("Helvetica", 10)

# Poll Page
def pollpage():
    def proceed():
        chose = choose.get()
        command = 'update polling set votes=votes+1 where name=?'
        pd.execute(command, (chose,))
        pd.commit()
        messagebox.showinfo('Success!', 'You have voted')

    choose = StringVar()
    names = []
    pd = sqltor.connect(plname + '.db')  # poll database
    pcursor = pd.cursor()
    pcursor.execute('select name from polling')
    data = pcursor.fetchall()
    for item in data:
        names.append(item[0])

    ppage = Toplevel()
    ppage.configure(bg=BG_COLOR)
    ppage.geometry('400x400')
    ppage.title('Vote for Your Candidate')

    Label(ppage, text='Vote for one candidate:', font=FONT_HEADER, fg=FG_COLOR, bg=BG_COLOR).pack(pady=10)
    for name in names:
        Radiobutton(ppage, text=name, value=name, variable=choose, bg=BG_COLOR, fg=FG_COLOR,
                    font=FONT_NORMAL, selectcolor=BG_COLOR).pack(anchor="w", padx=20)

    Button(ppage, text="Vote", command=proceed, bg=BTN_BG, fg=BTN_FG, font=FONT_NORMAL).pack(pady=20)

# My Polls Page
def polls():
    def proceed():
        global plname
        plname = psel.get()
        if plname == '-select-':
            return messagebox.showerror('Error', 'Select a poll')
        mpolls.destroy()
        pollpage()

    cursor.execute('select name from poll')
    data = cursor.fetchall()
    pollnames = ['-select-'] + [item[0] for item in data]

    psel = StringVar()
    mpolls = Toplevel()
    mpolls.configure(bg=BG_COLOR)
    mpolls.geometry('400x200')
    mpolls.title('Select Your Poll')

    Label(mpolls, text='Select Poll:', font=FONT_HEADER, bg=BG_COLOR, fg=FG_COLOR).pack(pady=20)
    select = ttk.Combobox(mpolls, values=pollnames, state='readonly', textvariable=psel, font=FONT_NORMAL)
    select.pack(pady=10)
    select.current(0)

    Button(mpolls, text='Proceed', command=proceed, bg=BTN_BG, fg=BTN_FG, font=FONT_NORMAL).pack(pady=10)

# Create Poll Page
def create():
    def proceed():
        pname = name.get()
        can = cname.get()
        if pname == '' or can == '':
            return messagebox.showerror('Error', 'Enter all fields')
        candidates = can.split(',')
        cursor.execute('insert into poll (name) values (?);', (pname,))
        conn.commit()

        pd = sqltor.connect(pname + '.db')
        pcursor = pd.cursor()
        pcursor.execute("""CREATE TABLE IF NOT EXISTS polling (name TEXT, votes INTEGER)""")
        for candidate in candidates:
            pcursor.execute('insert into polling (name, votes) values (?, ?)', (candidate, 0))
        pd.commit()
        messagebox.showinfo('Success', 'Poll Created')
        cr.destroy()

    cr = Toplevel()
    cr.configure(bg=BG_COLOR)
    cr.geometry('400x300')
    cr.title('Create New Poll')

    Label(cr, text='Create a Poll', font=FONT_HEADER, bg=BG_COLOR, fg=FG_COLOR).pack(pady=10)
    Label(cr, text='Poll Name:', bg=BG_COLOR, fg=FG_COLOR, font=FONT_NORMAL).pack()
    name = Entry(cr, font=FONT_NORMAL)
    name.pack(pady=5)

    Label(cr, text='Candidates (comma-separated):', bg=BG_COLOR, fg=FG_COLOR, font=FONT_NORMAL).pack()
    cname = Entry(cr, font=FONT_NORMAL)
    cname.pack(pady=5)

    Button(cr, text='Proceed', command=proceed, bg=BTN_BG, fg=BTN_FG, font=FONT_NORMAL).pack(pady=10)

# Poll Results
def selpl():
    def results():
        sel = sele.get()
        if sel == '-select-':
            return messagebox.showerror('Error', 'Select Poll')
        pl.destroy()
        def project():
            names, votes = zip(*r)
            plt.title('Poll Results')
            plt.pie(votes, labels=names, autopct='%1.1f%%', startangle=140, shadow=True)
            plt.axis('equal')
            plt.show()

        res = Toplevel()
        res.configure(bg=BG_COLOR)
        res.geometry('400x400')
        res.title('Poll Results')

        Label(res, text='Results:', font=FONT_HEADER, bg=BG_COLOR, fg=FG_COLOR).pack(pady=10)
        con = sqltor.connect(sel + '.db')
        pcursor = con.cursor()
        pcursor.execute('select * from polling')
        r = pcursor.fetchall()
        for item in r:
            Label(res, text=f"{item[0]}: {item[1]} votes", bg=BG_COLOR, fg=FG_COLOR, font=FONT_NORMAL).pack()

        Button(res, text='Project Results', command=project, bg=BTN_BG, fg=BTN_FG, font=FONT_NORMAL).pack(pady=10)

    cursor.execute('select name from poll')
    pollnames = ['-select-'] + [item[0] for item in cursor.fetchall()]

    pl = Toplevel()
    pl.configure(bg=BG_COLOR)
    pl.geometry('400x200')
    pl.title('View Poll Results')

    Label(pl, text='Select Poll:', font=FONT_HEADER, bg=BG_COLOR, fg=FG_COLOR).pack(pady=20)
    sele = ttk.Combobox(pl, values=pollnames, state='readonly', font=FONT_NORMAL)
    sele.pack(pady=10)
    sele.current(0)

    Button(pl, text='Get Results', command=results, bg=BTN_BG, fg=BTN_FG, font=FONT_NORMAL).pack(pady=10)

# About Dialog
def about():
    messagebox.showinfo('About', 'Developed by Aditya\nVoting Program in Python')

# Main Window
home = Tk()
home.geometry('500x500')
home.title('Voting Program')
home.configure(bg=BG_COLOR)

Label(home, text='Voting Program', font=("Helvetica", 18, "bold"), fg=FG_COLOR, bg=BG_COLOR).pack(pady=20)
Button(home, text='Create New Poll', command=create, bg=BTN_BG, fg=BTN_FG, font=FONT_NORMAL).pack(pady=10)
Button(home, text='My Polls', command=polls, bg=BTN_BG, fg=BTN_FG, font=FONT_NORMAL).pack(pady=10)
Button(home, text='Poll Results', command=selpl, bg=BTN_BG, fg=BTN_FG, font=FONT_NORMAL).pack(pady=10)
Button(home, text='About', command=about, bg=BTN_BG, fg=BTN_FG, font=FONT_NORMAL).pack(pady=10)

home.mainloop()
