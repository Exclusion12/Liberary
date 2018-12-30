import pyodbc
from tkinter import *
import tkinter.ttk as ttk
from datetime import *
from messeges import *


def Lib (con,cur):
    def Library_Contents():
        contents = Tk()
        contents.title("Liberary contents")
        contents.grid_rowconfigure(0,weight=1)
        contents.grid_columnconfigure(0,weight=1)
        contents.config(background="lavender")
        cols=('bid','Name','Author','Number of copies')
        content = ttk.Treeview(contents, columns=cols)
        content.heading('#0',text="id")
        content.column('#0',stretch=YES)
        for i in range(len(cols)):
            content.heading(cols[i],text=cols[i])
            content.column(cols[i],stretch=YES)
        content.pack(side=TOP)
        cur.execute("select * from book")
        for i in cur:
            items=[str(i.bid),str(i.name),str(i.author),str(i.ncopies)]
            content.insert('', END,text=str(i.bid), values=items)
        contents.mainloop()

    def Borrowing():
        def backfromb():
            borrowing.destroy()
            Lib(con,cur)
        def submit():
            a = username.get()
            b = Bookname.get()
            c = datetime.today().strftime('%Y-%m-%d')
            cur.execute("select * from users where username = ?",(a,))
            ncopies=0
            if cur.fetchone() is None:
                Error_401()
            else:
                cur.execute("select * from book where name = ?",(b,))
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
                            messagebox.showinfo("success","User now has that book")
                        except:
                            messagebox.showinfo("Error","User already has that book")

        lib.destroy()
        borrowing = Tk()
        username = StringVar()
        Bookname = StringVar()

        borrowing.geometry("600x200")
        borrowing.title("Borrowing sys")
        borrowing.configure(background="#373737")
        Label(borrowing, text="Username :", bg="#373737", fg="white", font="none 20 bold").grid(row=0, column=0,
                                                                                              sticky="w")
        textentry = Entry(borrowing, textvariable=username, width=40, bg="gray")
        textentry.grid(row=0, column=10, sticky="w")

        Label(borrowing, text="Book Name :", bg="#373737", fg="white", font="none 20 bold").grid(row=3, column=0,
                                                                                               sticky="w")
        textentry = Entry(borrowing, textvariable=Bookname, width=40, bg="gray")
        textentry.grid(row=3, column=10, sticky="w")

        Button(borrowing, text="Submit", width=15, command=submit).grid(row=9, column=5, sticky="w", pady=10)
        Button(borrowing, text="Back", width=15, command=backfromb).grid(row=9, column=10, sticky="w", pady=10)

        #messagebox.showinfo('Note', 'please enter date at this form : YYYY-MM-DD')
        borrowing.mainloop()

    def back():
        def backfromr():
            back.destroy()
            Lib(con,cur)
        def backin():
            a = username.get()
            b = Bookname.get()
            rdate = datetime.today().strftime('%Y-%m-%d')
            cur.execute("select * from users where username = ?",(a,))
            if cur.fetchone() is None:
                Error_401()
            else:
                cur.execute("select * from book where name = ?",(b,))
                if cur.fetchone() is None:
                    Error_400()
                else:
                    cur.execute("select * from users where username = ?",(a,))
                    for i in cur:
                        uid = i.uid
                    cur.execute("select * from book where name = ?",(b,))
                    for i in cur:
                        bid = i.bid
                        ncopies=i.ncopies
                    cur.execute("select * from borrow where uid = ? and bid = ?",(uid,bid))
                    if cur.fetchone() is None:
                        Error_398()
                    else:
                        cur.execute("select * from borrow where uid = ? and bid = ?",(uid,bid))
                        for i in cur:
                            bdate = i.bdate
                            d=i.duration
                        cur.execute("update book set ncopies = ? where bid = ?",(ncopies+1,bid))
                        cur.execute("delete from borrow where uid = ? and bid = ?",(uid,bid))
                        bdate=datetime.strptime(bdate,'%Y-%m-%d')
                        rdate=datetime.strptime(rdate,'%Y-%m-%d')
                        fined = rdate-bdate
                        if fined.days > d:
                            cur.execute("insert into history(uid,bid,bdate,duration,rdate,fined) values(?,?,?,?,?,?)",(uid,bid,bdate,d,rdate,1))
                            messagebox.showinfo("Fined","this user should pay fine for being late")
                        else:
                            cur.execute("insert into history(uid,bid,bdate,duration,rdate,fined) values(?,?,?,?,?,?)",(uid,bid,bdate,d,rdate,0))
                            messagebox.showinfo("Not Fined","this user should not pay any fine")
                        con.commit()
        lib.destroy()
        back = Tk()
        username = StringVar()
        Bookname = StringVar()

        back.geometry("600x300")
        back.title("back sys")
        back.configure(background="#373737")
        Label(back, text="Username :", bg="black", fg="white", font="none 20 bold").grid(row=0, column=0,
                                                                                         sticky="w")
        textentry = Entry(back, textvariable=username, width=40, bg="gray")
        textentry.grid(row=1, column=10, sticky="w")

        Label(back, text="Book Name :", bg="black", fg="white", font="none 20 bold").grid(row=3, column=0,
                                                                                          sticky="w")
        textentry = Entry(back, textvariable=Bookname, width=40, bg="gray")
        textentry.grid(row=4, column=10, sticky="w")

        Button(back, text="Submit", width=15, command=backin).grid(row=9, column=9, sticky="w", pady=10)
        Button(back, text="Back", width=15, command=backfromr).grid(row=10, column=9, sticky="w", pady=10)
        #messagebox.showinfo('Note', 'please enter date at this form : YYYY-MM-DD')
        back.mainloop()

    def ADD_Books():
        lib.destroy()
        book = Tk()
        book.geometry("600x400")
        book.title("book sys")
        book.configure(background="black")
        bookname = StringVar()
        authorname = StringVar()
        profduration = StringVar()
        studentduration = StringVar()
        numberofcopies = StringVar()

        def rfroma():
            book.destroy()
            Lib(con,cur)
        def booking():
            a = bookname.get()
            b = authorname.get()
            c = int(profduration.get())
            d = int(studentduration.get())
            e = numberofcopies.get()
            e=int(e)
            cur.execute("select * from book where name = ? and author = ?",(a,b))
            if cur.fetchone() is None:
                cur.execute("insert into book(name,author,ptime,stime,ncopies) values(?,?,?,?,?)",(a,b,c,d,e))
            else:
                cur.execute("select * from book where name = ? and author = ?",(a,b))
                for i in cur:
                    ncopies=i.ncopies
                cur.execute("update book set ncopies = ?",(ncopies+e,))
            con.commit()
            messagebox.showinfo("Success","book added successfully")
        Label(book, text="Book name :", bg="black", fg="white", font="none 20 bold").grid(row=0, column=0,
                                                                                          sticky="w")
        textentry = Entry(book, textvariable=bookname, width=40, bg="gray")
        textentry.grid(row=1, column=10, sticky="w")
        #
        Label(book, text="author name :", bg="black", fg="white", font="none 20 bold").grid(row=3, column=0,
                                                                                            sticky="w")
        textentry = Entry(book, textvariable=authorname, width=40, bg="gray")
        textentry.grid(row=4, column=10, sticky="w")
        #
        Label(book, text="prof duration :", bg="black", fg="white", font="none 20 bold").grid(row=5, column=0,
                                                                                              sticky="w")
        textentry = Entry(book, textvariable=profduration, width=40, bg="gray")
        textentry.grid(row=6, column=10, sticky="w")
        #
        Label(book, text="student duration :", bg="black", fg="white", font="none 20 bold").grid(row=7, column=0,
                                                                                                 sticky="w")
        textentry = Entry(book, textvariable=studentduration, width=40, bg="gray")
        textentry.grid(row=8, column=10, sticky="w")

        #
        Label(book, text="number of copies :", bg="black", fg="white", font="none 20 bold").grid(row=9, column=0,
                                                                                                 sticky="w")
        textentry = Entry(book, textvariable=numberofcopies, width=40, bg="gray")
        textentry.grid(row=10, column=10, sticky="w")

        Button(book, text="add", width=10, command=booking).grid(row=11, column=9, sticky="w", pady=10)
        Button(book, text="Back", width=10, command=rfroma).grid(row=12, column=9, sticky="w", pady=10)

    def Remove_Books():
        def rfromr():
            book.destroy()
            Lib(con,cur)
        lib.destroy()
        book = Tk()
        book.geometry("600x300")
        book.title("book sys")
        book.configure(background="black")
        bookname = StringVar()
        authorname = StringVar()

        def booking():
            a = bookname.get()
            b = authorname.get()
            cur.execute("select * from book where name= ? and author = ?",(a,b))
            if cur.fetchone() is None:
                Error_400()
            else:
                cur.execute("delete from book where name= ? and author = ?",(a,b))
                con.commit()

        Label(book, text="Book name :", bg="black", fg="white", font="none 20 bold").grid(row=0, column=0,
                                                                                          sticky="w")
        textentry = Entry(book, textvariable=bookname, width=40, bg="gray")
        textentry.grid(row=1, column=10, sticky="w")
        #
        Label(book, text="author name :", bg="black", fg="white", font="none 20 bold").grid(row=3, column=0,
                                                                                            sticky="w")
        textentry = Entry(book, textvariable=authorname, width=40, bg="gray")
        textentry.grid(row=4, column=10, sticky="w")
        #


        Button(book, text="Remove", width=10, command=booking).grid(row=9, column=9, sticky="w", pady=10)
        Button(book, text="Back", width=10, command=rfromr).grid(row=10, column=9, sticky="w", pady=10)

        book.mainloop()

    def search_for_books():
        def back_button():
            books.destroy()
            Lib(con,cur)

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

        lib.destroy()
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

    def borrow_table():
        btable = Tk()
        btable.title("Borrowing status")
        btable.grid_rowconfigure(0,weight=1)
        btable.grid_columnconfigure(0,weight=1)
        btable.config(background="lavender")
        cols=('Username','Book name','Duration','Borrow date')
        content = ttk.Treeview(btable, columns=cols)
        content.heading('#0',text="id")
        content.column('#0',stretch=YES)
        for i in range(len(cols)):
            content.heading(cols[i],text=cols[i])
            content.column(cols[i],stretch=YES)
        content.pack(side=TOP)
        cur.execute("select book.name as bookname,users.username as username ,bdate,duration from borrow join book on borrow.bid=book.bid join users on borrow.uid=users.uid")
        for i in cur:
            items=[str(i.username),str(i.bookname),str(i.duration),str(i.bdate)]
            content.insert('', END,text=str(i.id), values=items)
        btable.mainloop()

    def history_table():
        htable = Tk()
        htable.title("Borrowing history")
        htable.grid_rowconfigure(0,weight=1)
        htable.grid_columnconfigure(0,weight=1)
        htable.config(background="lavender")
        cols=('Username','Book name','Duration','Borrow date','Returning date','fined')
        content = ttk.Treeview(htable, columns=cols)
        content.heading('#0',text="id")
        content.column('#0',stretch=YES)
        for i in range(len(cols)):
            content.heading(cols[i],text=cols[i])
            content.column(cols[i],stretch=YES)
        content.pack(side=TOP)
        cur.execute("select id , book.name as bookname,users.username as username ,rdate,bdate,fined,duration from history join book on history.bid=book.bid join users on history.uid=users.uid")
        for i in cur:
            items=[str(i.username),str(i.bookname),str(i.duration),str(i.bdate),str(i.rdate),str(i.fined)]
            content.insert('', END,text=str(i.id), values=items)
        htable.mainloop()



    lib = Tk()
    lib.geometry("435x250")
    lib.title("Library Adminstration ")
    lib.configure(background="black")
    Label(lib, text=" Library  Adminstration ", bg="black", fg="white", font="none 20 bold").grid(row=0, column=0,sticky="w", pady=10)

    Button(lib, text="Library Contents", width=15, command=Library_Contents).grid(row=1, column=0, sticky="w", pady=10)
    Button(lib, text="Borrowing", width=15, command=Borrowing).grid(row=2, column=0, sticky="w", pady=10)
    Button(lib, text="Retrieve", width=15, command=back).grid(row=3, column=0, sticky="w", pady=10)
    Button(lib, text="Borrow history", width=15, command=history_table).grid(row=4, column=0, sticky="w", pady=10)
    Button(lib, text="Add Books", width=15, command=ADD_Books).grid(row=1, column=1, sticky="w", pady=10)
    Button(lib, text="Remove Books", width=15, command=Remove_Books).grid(row=2, column=1, sticky="w", pady=10)
    Button(lib, text="Search for Books", width=15, command=search_for_books).grid(row=3, column=1, sticky="w", pady=10)
    Button(lib, text="Borrow table", width=15, command=borrow_table).grid(row=4, column=1, sticky="w", pady=10)
    lib.mainloop()



if __name__ == "__main__":
    con = pyodbc.connect('Driver={SQL Server};'
                      'Server=EXCLUSION;'
                      'Database=liberary;'
                      'Trusted_Connection=yes;')
    cur = con.cursor()
    Lib(con,cur)
