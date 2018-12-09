import sqlite3
from tkinter import *
from tkinter import messagebox
from datetime import *
con = sqlite3.connect('liberary.db')
cur = con.cursor()

#cur.execute("create table users(uid integer primary key autoincrement,username char(50) NOT NULL unique,password char(50) not null,role char(50) not null);")
#cur.execute("create table book(bid integer primary key autoincrement,name char(50) not null,author char(50) not null,ptime int not null,stime int not null,ncopies int not null);")
#cur.execute("create table  borrow (id integer primary key autoincrement,uid int not null,bid int not null,bdate date not null ,duration int not null ,rdate date,fined bit, FOREIGN KEY (uid) REFERENCES users,FOREIGN KEY (bid) REFERENCES book);")
#cur.execute("insert into users(username,password,role) values('admin','admin','admin')")
#con.commit()

def Success_200():
    messagebox.showinfo('Done', 'user is on now')

def Success_201():
    messagebox.showinfo('Done', 'user is now deleted')

def Error_398():
    messagebox.showinfo('Error', 'Borrowing operation is not found')

def Error_399():
    messagebox.showinfo('Error', 'Book is not available now')

def Error_400():
    messagebox.showinfo('Error', 'Book does not exist')

def Error_401():
    messagebox.showinfo('Error', 'Username does not exist')

def Error_402():
    messagebox.showinfo('role', 'enter valid role : admin ,student ,prof ,lib')

def Error_403():
    messagebox.showinfo('Confliction', 'username already exists')

def Error_404():
    messagebox.showinfo('Wrong username or password', 'Enter your password or username correctly')

def Error_405():
    messagebox.showinfo('Wrong username', 'Enter username correctly')

def login():
    cur.execute("select * from users where username = ? and password = ?",(user.get(),password.get()))
    if cur.fetchone() is None:
        Error_404()
    else:
        cur.execute("select * from users where username = ? and password = ?",(user.get(),password.get()))
        for i in cur:
            if i[3]=="admin":
                root.destroy()
                admin()
            elif i[3]=="student":
                root.destroy()
                prostd(i[1],i[3])
            elif i[3]=="prof":
                root.destroy()
                prostd(i[1],i[3])
            elif i[3]=="lib":
                root.destroy()
                Lib()

def login_page ():
    root.title("Library system")
    root.configure(background="black")

    # creat a lable / lma n3oz nktb 7aga
    Label(root, text="User Name  : ", bg="black", fg="white", font="none 20 bold").grid(row=1, column=0, sticky="w")
    Label(root, text="password  : ", bg="black", fg="white", font="none 20 bold").grid(row=4, column=0, sticky="w")
    # creat an entry BOx

    textentry = Entry(root, textvariable=user, width=40, bg="gray")
    textentry.grid(row=3, column=10, sticky="w")

    textentry2 = Entry(root, textvariable=password, width=40, bg="gray", show="*")
    textentry2.grid(row=5, column=10, sticky="w")

    # add a bottom
    Button(root, text="login", width=6 ,command=login).grid(row=6, column=10, sticky="w")
    root.mainloop()

def prostd(username,role):
    def Library_Contents():
        content2 = Tk()
        content2.title("Content ")
        content2.geometry("400x400")
        scrollbar = Scrollbar(content2)
        scrollbar.pack(side=RIGHT, fill=Y)
        listbox=[1,2,3,4,5]
        for i in range(5):
            listbox[i] = Listbox(content2, width=13, height=13, yscrollcommand=scrollbar.set)
        listbox[0].insert(END,"  bid")
        listbox[1].insert(END,"  name")
        listbox[2].insert(END,"  author")
        listbox[3].insert(END,"  nofcopies")
        listbox[4].insert(END,"  Borrowing duration")
        cur.execute("select * from book")
        for i in cur:
            listbox[0].insert(END,i[0])
            listbox[1].insert(END,i[1])
            listbox[2].insert(END,i[2])
            listbox[3].insert(END,i[5])
            if role=="prof":
                listbox[4].insert(END,i[3])
            else:
                listbox[4].insert(END,i[4])
        for i in range(5):
            listbox[i].pack(side=LEFT, fill=BOTH)
        scrollbar.config(command=listbox[0].yview)
        content2.mainloop()
    def Borrowing():
        def backfromb():
            borrowing.destroy()
            prostd(username,role)
        def submit():
            a = username
            b = Bookname.get()
            c = datetime.today().strftime('%Y-%m-%d')
            cur.execute("select * from book where name = ?",(b,))
            if cur.fetchone() is None:
                Error_400()
            else:
                cur.execute("select * from users where username = ? ",(a,))
                for i in cur:
                    uid=i[0]
                    role=i[3]
                if role=="student":
                    cur.execute("select * from book where name = ?",(b,))
                    for i in cur:
                        bid=i[0]
                        time=i[4]
                elif role=="prof":
                    cur.execute("select * from book where name = ?",(b,))
                    for i in cur:
                        bid=i[0]
                        time=i[3]
                        ncopies=i[5]
                if ncopies==0:
                    Error_399()
                else:
                    cur.execute("insert into borrow(uid,bid,bdate,duration) values (?,?,?,?)",(uid,bid,c,time))
                    cur.execute("update book set ncopies = ? where bid = ?",(ncopies-1,bid))
                    con.commit()
        Prostd.destroy()
        borrowing = Tk()
        Bookname = StringVar()
        borrowing.geometry("600x300")
        borrowing.title("Borrowing sys")
        borrowing.configure(background="black")

        Label(borrowing, text="Book Name :", bg="black", fg="white", font="none 20 bold").grid(row=3, column=0,
                                                                                               sticky="w")
        textentry = Entry(borrowing, textvariable=Bookname, width=40, bg="gray")
        textentry.grid(row=4, column=10, sticky="w")

        Button(borrowing, text="Submit", width=15, command=submit).grid(row=9, column=9, sticky="w", pady=10)
        Button(borrowing, text="Back", width=15, command=backfromb).grid(row=10, column=9, sticky="w", pady=10)
        #messagebox.showinfo('Note', 'please enter date at this form : YYYY-MM-DD')
        borrowing.mainloop()

    Prostd = Tk()
    Prostd.geometry("400x400")
    if role=="prof":
        Prostd.title("Prof interface")
        Label(Prostd, text=" Prof interface ", bg="black", fg="white", font="none 20 bold").grid(row=0, column=0,sticky="w", pady=10)
    else:
        Prostd.title("Student interface")
        Label(Prostd, text=" Student interface ", bg="black", fg="white", font="none 20 bold").grid(row=0, column=0,sticky="w", pady=10)
    Prostd.configure(background="black")
    Button(Prostd, text="Library Contents", width=15, command=Library_Contents).grid(row=1, column=0, sticky="w", pady=10)
    Button(Prostd, text="Borrowing", width=15, command=Borrowing).grid(row=5, column=0, sticky="w", pady=10)
    Prostd.mainloop()


def Lib ():
    def Library_Contents():
        content = Tk()
        content.title("Content ")
        content.geometry("400x400")
        scrollbar = Scrollbar(content)
        scrollbar.pack(side=RIGHT, fill=Y)
        listbox=[1,2,3,4]
        for i in range(4):
            listbox[i] = Listbox(content, width=13, height=13, yscrollcommand=scrollbar.set)
        listbox[0].insert(END,"  bid")
        listbox[1].insert(END,"  name")
        listbox[2].insert(END,"  author")
        listbox[3].insert(END,"  nofcopies")
        cur.execute("select * from book")
        for i in cur:
            listbox[0].insert(END,i[0])
            listbox[1].insert(END,i[1])
            listbox[2].insert(END,i[2])
            listbox[3].insert(END,i[5])
        for i in range(4):
            listbox[i].pack(side=LEFT, fill=BOTH)
        scrollbar.config(command=listbox[0].yview)
        content.mainloop()

    def Borrowing():
        def backfromb():
            borrowing.destroy()
            Lib()
        def submit():
            a = username.get()
            b = Bookname.get()
            c = datetime.today().strftime('%Y-%m-%d')
            cur.execute("select * from users where username = ?",(a,))
            if cur.fetchone() is None:
                Error_401()
            else:
                cur.execute("select * from book where name = ?",(b,))
                if cur.fetchone() is None:
                    Error_400()
                else:
                    cur.execute("select * from users where username = ? ",(a,))
                    for i in cur:
                        uid=i[0]
                        role=i[3]
                    if role=="student":
                        cur.execute("select * from book where name = ?",(b,))
                        for i in cur:
                            bid=i[0]
                            time=i[4]
                            ncopies=i[5]
                    elif role=="prof":
                        cur.execute("select * from book where name = ?",(b,))
                        for i in cur:
                            bid=i[0]
                            time=i[3]
                            ncopies=i[5]
                    if ncopies==0:
                        Error_399()
                    else:
                        cur.execute("insert into borrow(uid,bid,bdate,duration) values (?,?,?,?)",(uid,bid,c,time))
                        cur.execute("update book set ncopies = ? where bid = ?",(ncopies-1,bid))
                        con.commit()

        lib.destroy()
        borrowing = Tk()
        username = StringVar()
        Bookname = StringVar()

        borrowing.geometry("600x300")
        borrowing.title("Borrowing sys")
        borrowing.configure(background="black")
        Label(borrowing, text="Username :", bg="black", fg="white", font="none 20 bold").grid(row=0, column=0,
                                                                                              sticky="w")
        textentry = Entry(borrowing, textvariable=username, width=40, bg="gray")
        textentry.grid(row=1, column=10, sticky="w")

        Label(borrowing, text="Book Name :", bg="black", fg="white", font="none 20 bold").grid(row=3, column=0,
                                                                                               sticky="w")
        textentry = Entry(borrowing, textvariable=Bookname, width=40, bg="gray")
        textentry.grid(row=4, column=10, sticky="w")

        Button(borrowing, text="Submit", width=15, command=submit).grid(row=9, column=9, sticky="w", pady=10)
        Button(borrowing, text="Back", width=15, command=backfromb).grid(row=10, column=9, sticky="w", pady=10)

        #messagebox.showinfo('Note', 'please enter date at this form : YYYY-MM-DD')
        borrowing.mainloop()

    def back():
        def backfromr():
            back.destroy()
            Lib()
        def backin():
            a = username.get()
            b = Bookname.get()
            c = datetime.today().strftime('%Y-%m-%d')
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
                        uid = i[0]
                    cur.execute("select * from book where name = ?",(b,))
                    for i in cur:
                        bid = i[0]
                        ncopies=i[5]
                    cur.execute("select * from borrow where uid = ? and bid = ?",(uid,bid))
                    if cur.fetchone() is None:
                        Error_398()
                    else:
                        cur.execute("select * from borrow where uid = ? and bid = ?",(uid,bid))
                        for i in cur:
                            bdate = i[3]
                            d = i[4]
                        cur.excute("update table book set ncopies = ? where bid = ?",(ncopies+1,bid))
                        cur.execute("update table borrow set rdate = ? where uid = ? and bid = ?",(c,uid,bid))
                        fined = c-bdate
                        if fined > d:
                            cur.execute("update table borrow set fined = ? where uid = ? and bid = ?",(1,uid,bid))
                        else:
                            cur.execute("update table borrow set fined = ? where uid = ? and bid = ?",(0,uid,bid))
                        con.commit()

        lib.destroy()
        back = Tk()
        username = StringVar()
        Bookname = StringVar()

        back.geometry("600x300")
        back.title("back sys")
        back.configure(background="black")
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
            Lib()
        def booking():
            a = bookname.get()
            b = authorname.get()
            c = profduration.get()
            d = studentduration.get()
            e = numberofcopies.get()
            e=int(e)
            cur.execute("select * from book where name = ? and author = ?",(a,b))
            if cur.fetchone() is None:
                cur.execute("insert into book(name,author,ptime,stime,ncopies) values(?,?,?,?,?)",(a,b,c,d,e))
                con.commit()
            else:
                cur.execute("select * from book where name = ? and author = ?",(a,b))
                for i in cur:
                    ncopies=i[5]
                cur.execute("update book set ncopies = ?",(ncopies+e,))
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
            Lib()
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

    lib = Tk()
    lib.geometry("400x400")
    lib.title("Library Adminstration ")
    lib.configure(background="black")
    Label(lib, text=" Library  Adminstration ", bg="black", fg="white", font="none 20 bold").grid(row=0, column=0,sticky="w", pady=10)
    Button(lib, text="Library Contents", width=15, command=Library_Contents).grid(row=1, column=0, sticky="w", pady=10)
    Button(lib, text="Borrowing", width=15, command=Borrowing).grid(row=5, column=0, sticky="w", pady=10)
    Button(lib, text="Retrieve", width=15, command=back).grid(row=7, column=0, sticky="w", pady=10)
    Button(lib, text="Add Books", width=15, command=ADD_Books).grid(row=8, column=0, sticky="w", pady=10)
    Button(lib, text="Remove Books", width=15, command=Remove_Books).grid(row=9, column=0, sticky="w", pady=10)

    lib.mainloop()


def admin():
    def register():
        l=["admin","student","lib","prof"]
        if not role.get() in l:
            Error_402()
        else:
            try:
                cur.execute("insert into users(username,password,role) values(?,?,?)",(Newuser.get(),Newpassword.get(),role.get()))
                con.commit()
                Success_200()
            except:
                Error_403()

    def deleted():
        s=Deletedname.get()
        cur.execute("select * from users where username= ? ",(s,))
        if cur.fetchone() is None:
            Error_405()
        else:
            cur.execute("delete from users where username= ? ",(s,))
            con.commit()
            Success_201()

    adminer = Tk()
    Newuser = StringVar()
    Newpassword = StringVar()
    Deletedname=StringVar()
    role = StringVar()

    adminer.title("Admin")
    adminer.configure(background="black")
    # lables
    Label(adminer, text="Register New member  : ", bg="black", fg="white", font="none 20 bold").grid(row=1, column=0,
                                                                                                     sticky="w")
    Label(adminer, text="Name : ", bg="black", fg="white", font="none 20 bold").grid(row=2, column=0, sticky="w")
    Label(adminer, text="Password  : ", bg="black", fg="white", font="none 20 bold").grid(row=4, column=0, sticky="w")
    Label(adminer, text="role  : ", bg="black", fg="white", font="none 20 bold").grid(row=6, column=0, sticky="w")

    Label(adminer, text="Delete members (Enter the name ) : ", bg="black", fg="white", font="none 20 bold").grid(row=13,
                                                                                                                 column=0,
                                                                                                                 sticky="w")
    # entery
    textentry = Entry(adminer, textvariable=Newuser, width=40, bg="gray")
    textentry.grid(row=3, column=10, sticky="w")

    textentry2 = Entry(adminer, textvariable=Newpassword, width=40, bg="gray", show="*")
    textentry2.grid(row=5, column=10, sticky="w")

    textentry4 = Entry(adminer, textvariable=role, width=40, bg="gray")
    textentry4.grid(row=7, column=10, sticky="w")

    textentry3 = Entry(adminer, textvariable=Deletedname, width=40, bg="gray")
    textentry3.grid(row=14, column=10, sticky="w")

    Button(adminer, text="register", width=6, command=register).grid(row=9, column=10, sticky="w")
    Button(adminer, text="Delete", width=6, command=deleted).grid(row=15, column=10, sticky="w")
    adminer.mainloop()

root=Tk()
user = StringVar()
password = StringVar()
login_page()
