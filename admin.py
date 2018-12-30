import pyodbc
from tkinter import *
from messeges import *


def admin(con,cur):
    def register():
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


    def search_for_user():
        s=Usersearch.get()
        users = Tk()
        users.title("Search results for "+s)
        #users.geometry("400x400")
        scrollbar = Scrollbar(users)
        scrollbar.pack(side=RIGHT, fill=Y)
        cur.execute("select username from users where username LIKE ?",('%'+s+'%',))
        list = Listbox(users, width=30, height=13, yscrollcommand=scrollbar.set)
        list.insert(END,"Search results for "+s)
        list.insert(END,"- - - - - - - - - - - -")
        list.insert(END,"Username")
        list.insert(END,"-------------")
        for i in cur:
            list.insert(END,i.username)
        list.pack(side=LEFT, fill=BOTH)
        scrollbar.config(command=list.yview)
        users.mainloop()

    adminer = Tk()
    adminer.geometry('500x280')
    Newuser = StringVar()
    Newpassword = StringVar()
    Deletedname=StringVar()
    Usersearch = StringVar()
    # role pop menu
    role = StringVar()
    choices = ["admin","student","lib","prof"]
    role.set('admin')
    popM = OptionMenu(adminer, role, *choices)
    popM.grid(row=6, column=1, sticky="w")

    adminer.title("Admin")
    adminer.configure(background="#373737")
    # lables
    Label(adminer, text="Register New member  : ", bg="#373737", fg="white", font="none 15 bold").grid(row=1, column=0, sticky="w")
    Label(adminer, text="Name : ", bg="#373737", fg="white", font="none 10 bold").grid(row=2, column=0, sticky="w")
    Label(adminer, text="Password  : ", bg="#373737", fg="white", font="none 10 bold").grid(row=4, column=0, sticky="w")
    Label(adminer, text="role  : ", bg="#373737", fg="white", font="none 10 bold").grid(row=6, column=0, sticky="w")
    Label(adminer, text="Delete members (Enter the name ) : ", bg="#373737", fg="white", font="none 10 bold").grid(row=13, column=0,sticky="w")
    Label(adminer, text="Search for member (Enter the name ) : ", bg="#373737", fg="white", font="none 10 bold").grid(row=17, column=0,sticky="w")
    Label(adminer, text="Leave it blank to view all", bg="#373737", fg="white", font="none 10 bold").grid(row=19, column=0,sticky="w")
    # entery
    textentry = Entry(adminer, textvariable=Newuser, width=40, bg="gray")
    textentry.grid(row=2, column=1, sticky="w")
    textentry2 = Entry(adminer, textvariable=Newpassword, width=40, bg="gray", show="*")
    textentry2.grid(row=4, column=1, sticky="w")
    textentry3 = Entry(adminer, textvariable=Deletedname, width=40, bg="gray")
    textentry3.grid(row=13, column=1, sticky="w")
    textentry4 = Entry(adminer, textvariable=Usersearch, width=40, bg="gray")
    textentry4.grid(row=17, column=1, sticky="w")

    Button(adminer, text="register", width=6, command=register).grid(row=9, column=1, sticky="w")
    Button(adminer, text="Delete", width=6, command=deleted).grid(row=15, column=1, sticky="w")
    Button(adminer, text="Search", width=6, command=search_for_user).grid(row=19, column=1, sticky="w")

    def change_dropdown(*args):
    	print( role.get() )
    role.trace('w', change_dropdown)
    adminer.mainloop()



if __name__ == "__main__":
    con = pyodbc.connect('Driver={SQL Server};'
                      'Server=EXCLUSION;'
                      'Database=liberary;'
                      'Trusted_Connection=yes;')
    cur = con.cursor()
    admin(con,cur)
