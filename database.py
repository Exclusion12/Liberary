from prostd import *
from admin import *
from lib import *

con = pyodbc.connect('Driver={SQL Server};'
                      'Server=EXCLUSION;'
                      'Database=liberary;'
                      'Trusted_Connection=yes;')
cur = con.cursor()

#comitted in sql server management studio

'''
create table users(
uid integer identity(1,1) primary key,
username nvarchar(50) NOT NULL unique,
password nvarchar(50) not null,
role nvarchar(50) not null);


create table book(bid integer primary key identity(1,1),
name nvarchar(50) not null,
author nvarchar(50) not null,
ptime int not null,
stime int not null,
ncopies int not null);


create table  borrow (id integer primary key identity(1,1),
uid int not null,
bid int not null,
bdate date not null,
duration int not null,
unique(uid,bid),
FOREIGN KEY (uid) REFERENCES users,
FOREIGN KEY (bid) REFERENCES book);


create table  history (
id integer primary key identity(1,1),
uid int not null,
bid int not null,
bdate date not null,
duration int not null,
rdate date,
fined bit);

insert into users(username,password,role) values('admin','admin','admin')

'''

# cur.execute("create table users(uid integer primary key identity(1,1),username nvarchar(50) NOT NULL unique,password nvarchar(50) not null,role nvarchar(50) not null);")
# cur.execute("create table book(bid integer primary key identity(1,1),name nvarchar(50) not null,author nvarchar(50) not null,ptime int not null,stime int not null,ncopies int not null);")
# cur.execute("create table  borrow (id integer primary key identity(1,1),uid int not null,bid int not null,unique(uid,bid),bdate date not null ,duration int not null ,rdate date,fined bit, FOREIGN KEY (uid) REFERENCES users,FOREIGN KEY (bid) REFERENCES book);")
# cur.execute("insert into users(username,password,role) values('admin','admin','admin')")
# con.commit()


def login():
    cur.execute("select * from users where username = ? and password = ?",(user.get(),password.get()))
    if cur.fetchone() is None:
        Error_404()
    else:
        cur.execute("select * from users where username = ? and password = ?",(user.get(),password.get()))
        for i in cur:
            if i.role=="admin":
                root.destroy()
                admin(con,cur)
            elif i.role=="student":
                root.destroy()
                prostd(i.username,i.role,con,cur)
            elif i.role=="prof":
                root.destroy()
                prostd(i.username,i.role,con,cur)
            elif i.role=="lib":
                root.destroy()
                Lib(con,cur)

def login_page ():
    root.title("Library system")
    root.configure(background="#373737")
    root.geometry("300x100")

    # creat a lable / lma n3oz nktb 7aga
    Label(root, text="User Name  : ", bg="#373737", fg="white", font="Arial 15 ").grid(row=1, column=0, sticky="w")
    Label(root, text="password  : ", bg="#373737", fg="white", font="Arial 15 ").grid(row=4, column=0, sticky="w")
    # creat an entry BOx

    textentry = Entry(root, textvariable=user, width=20, bg="#DFDFDF")
    textentry.grid(row=1, column=10, sticky="w")
    textentry.focus()

    textentry2 = Entry(root, textvariable=password, width=20, bg="#DFDFDF", show="*")
    textentry2.grid(row=4, column=10, sticky="w")

    # add a bottom
    Button(root, text="login", width=6 ,command=login).grid(row=6, column=10, sticky="w")
    root.mainloop()


root=Tk()
user = StringVar()
password = StringVar()
login_page()
