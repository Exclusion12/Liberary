import pyodbc
from tkinter import *
import tkinter.ttk as ttk
from datetime import *
from messeges import *

def prostd(username,role,con,cur):
    def Library_Contents():
        contents = Tk()
        contents.title("Liberary contents")
        contents.grid_rowconfigure(0,weight=1)
        contents.grid_columnconfigure(0,weight=1)
        contents.config(background="lavender")
        cols=('bid','Name','Author','Number of copies','Borrowing duration')
        content = ttk.Treeview(contents, columns=cols)
        content.heading('#0',text="id")
        content.column('#0',stretch=YES)
        for i in range(len(cols)):
            content.heading(cols[i],text=cols[i])
            content.column(cols[i],stretch=YES)
        content.pack(side=TOP)
        cur.execute("select * from book")
        if role == "student":
            for i in cur:
                items=[str(i.bid),str(i.name),str(i.author),str(i.ncopies),str(i.stime)]
                content.insert('', END,text=str(i.bid), values=items)
        else:
            for i in cur:
                items=[str(i.bid),str(i.name),str(i.author),str(i.ncopies),str(i.ptime)]
                content.insert('', END,text=str(i.bid), values=items)
        contents.mainloop()

    def Borrowing():
        def backfromb():
            borrowing.destroy()
            prostd(username,role,con,cur)
        def submit():
            a = username
            b = Bookname.get()
            c = datetime.today().strftime('%Y-%m-%d')
            cur.execute("select * from book where name = ?",(b,))
            ncopies=0
            if cur.fetchone() is None:
                Error_400()
            else:
                cur.execute("select * from users where username = ? ",(a,))
                for i in cur:
                    uid=i.uid
                    role=i.role
                if role=="student":
                    cur.execute("select * from book where name = ?",(b,))
                    for i in cur:
                        bid=i.bid
                        time=i.stime
                        ncopies=i.ncopies
                elif role=="prof":
                    cur.execute("select * from book where name = ?",(b,))
                    for i in cur:
                        bid=i.bid
                        time=i.ptime
                        ncopies=i.ncopies
                if ncopies==0:
                    Error_399()
                else:
                    try:
                        cur.execute("insert into borrow(uid,bid,bdate,duration) values (?,?,?,?)",(uid,bid,c,time))
                        cur.execute("update book set ncopies = ? where bid = ?",(ncopies-1,bid))
                        con.commit()
                        messagebox.showinfo("success","you now have that book")
                    except:
                        messagebox.showinfo("Error","you already have that book")
        Prostd.destroy()
        borrowing = Tk()
        Bookname = StringVar()
        borrowing.geometry("600x300")
        borrowing.title("Borrowing sys")
        borrowing.configure(background="#373737")

        Label(borrowing, text="Book Name :", bg="black", fg="white", font="none 20 bold").grid(row=3, column=0,
                                                                                               sticky="w")
        textentry = Entry(borrowing, textvariable=Bookname, width=40, bg="gray")
        textentry.grid(row=4, column=10, sticky="w")

        Button(borrowing, text="Submit", width=15, command=submit).grid(row=9, column=9, sticky="w", pady=10)
        Button(borrowing, text="Back", width=15, command=backfromb).grid(row=10, column=9, sticky="w", pady=10)
        #messagebox.showinfo('Note', 'please enter date at this form : YYYY-MM-DD')
        borrowing.mainloop()
    def search_for_books():
        def back_button():
            books.destroy()
            prostd(username,role,con,cur)

        def search_for_book():
            name=Bookname.get()
            author=Bookauthor.get()
            book = Tk()
            book.title("Search results for "+name)
            #users.geometry("400x400")
            scrollbar = Scrollbar(book)
            scrollbar.pack(side=RIGHT, fill=Y)
            cur.execute("select * from book where name LIKE ? and author LIKE ?",('%'+name+'%','%'+author+'%'))
            listbox=[1,2,3,4]
            for i in range(4):
                listbox[i] = Listbox(book, width=13, height=13, yscrollcommand=scrollbar.set)
            listbox[0].insert(END,"  bid")
            listbox[1].insert(END,"  name")
            listbox[2].insert(END,"  author")
            listbox[3].insert(END,"  nofcopies")
            for i in cur:
                listbox[0].insert(END,i.bid)
                listbox[1].insert(END,i.name)
                listbox[2].insert(END,i.author)
                listbox[3].insert(END,i.ncopies)
            for i in range(4):
                listbox[i].pack(side=LEFT, fill=BOTH)
            scrollbar.config(command=listbox[0].yview)
            book.mainloop()

        Prostd.destroy()
        books=Tk()
        books.geometry("400x150")
        books.title("Search for books")
        books.configure(background="black")
        Bookname= StringVar()
        Bookauthor= StringVar()

        Label(books, text="book name : ", bg="#373737", fg="white", font="none 10 bold").grid(row=1, column=0,sticky="w")
        Label(books, text="Author    : ", bg="#373737", fg="white", font="none 10 bold").grid(row=3, column=0,sticky="w")

        textentry = Entry(books, textvariable=Bookname, width=40, bg="gray")
        textentry.grid(row=2, column=1, sticky="w")
        textentry2 = Entry(books, textvariable=Bookauthor, width=40, bg="gray")
        textentry2.grid(row=4, column=1, sticky="w")

        Button(books, text="Search", width=6, command=search_for_book).grid(row=7, column=1, sticky="w")
        Button(books, text="Back", width=6, command=back_button).grid(row=9, column=1, sticky="w")

    Prostd = Tk()
    Prostd.geometry("400x400")
    if role=="prof":
        Prostd.title("Prof interface")
        Label(Prostd, text=" Prof interface ", bg="black", fg="white", font="none 20 bold").grid(row=0, column=0,sticky="w", pady=10)
    else:
        Prostd.title("Student interface")
        Label(Prostd, text=" Student interface ", bg="black", fg="white", font="none 20 bold").grid(row=0, column=0,sticky="w", pady=10)
    Prostd.configure(background="#373737")
    Button(Prostd, text="Library Contents", width=15, command=Library_Contents).grid(row=1, column=0, sticky="w", pady=10)
    Button(Prostd, text="Borrowing", width=15, command=Borrowing).grid(row=5, column=0, sticky="w", pady=10)
    Button(Prostd, text="Search for Books", width=15, command=search_for_books).grid(row=10, column=0, sticky="w", pady=10)

    Prostd.mainloop()

if __name__ == "__main__":
    con = pyodbc.connect('Driver={SQL Server};'
                      'Server=EXCLUSION;'
                      'Database=liberary;'
                      'Trusted_Connection=yes;')
    cur = con.cursor()
    prostd("fortest","student",con,cur)
