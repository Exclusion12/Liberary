from tkinter import messagebox
def Success_200():
    messagebox.showinfo('Done', 'user is on now')

def Success_201():
    messagebox.showinfo('Done', 'user is now deleted')

def Error_398():
    messagebox.showinfo('Error', 'User does not have the book')

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
