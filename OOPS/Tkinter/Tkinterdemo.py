from tkinter import *
import mysql.connector 
import tkinter.messagebox as msg 

def create_conn():
    return mysql.connector.connect(
        database ="python_new",
        user="root",
        password="",
        host="localhost"

    )
print(create_conn())

def insert_data():
    if e_fname.get()=="" or e_lname.get()=="" or e_email.get()=="" or e_mobile.get()=="":
        msg.showinfo("Insert Status" , "All Fields Are Mandatory")
    else:
        conn=create_conn()
        cursor=conn.cursor()
        query="insert into student(fname,lname,email,mobile) values(%s,%s,%s,%s)"
        args=(e_fname.get(),e_lname.get(),e_email.get(),e_mobile.get())   
        cursor.execute(query,args) 
        conn.commit()
        conn.close()
        e_fname.delete(0,'end')
        e_lname.delete(0,'end')
        e_email.delete(0,'end')
        e_mobile.delete(0,'end')
        msg.showinfo("Insert Status" , "Data Inserted Successfylly")

    
def search_data():
    e_fname.delete(0,'end')
    e_lname.delete(0,'end')
    e_email.delete(0,'end')
    e_mobile.delete(0,'end')
    if e_id.get()=="":
       msg.showinfo("Search Status" , "ID IS Mendatory")
    else:
        conn=create_conn()
        cursor=conn.cursor()
        query="select * from student where id=%s"
        args=(e_id.get(),)   
        cursor.execute(query,args)
        row=cursor.fetchall()
        if row:
            e_fname.insert(0,row[0][1])
            e_lname.insert(0,row[0][2])
            e_email.insert(0,row[0][3])
            e_mobile.insert(0,row[0][4])
        else:
            msg.showinfo("Search Status" , "Id Not Found")     
        conn.close()


def Update_data():
    if e_id.get()=="" or e_fname.get()=="" or e_lname.get()=="" or e_email.get()=="" or e_mobile.get()=="":
        msg.showinfo("Update Status" , "All Fields Are Mandatory")
    else:
        conn=create_conn()
        cursor=conn.cursor()
        query="update student set fname=%s , lname=%s , email=%s , mobile=%s where id=%s"
        args=(e_fname.get(),e_lname.get(),e_email.get(),e_mobile.get(),e_id.get())   
        cursor.execute(query,args) 
        conn.commit()
        conn.close()
        e_fname.delete(0,'end')
        e_lname.delete(0,'end')
        e_email.delete(0,'end')
        e_mobile.delete(0,'end')
        msg.showinfo("Update Status" , "Data Updated Successfylly")

def Delete_data():
    if e_id.get():
        msg.showinfo("Delete Status" , "All Fields Are Mandatory")
    else:
        conn=create_conn()
        cursor=conn.cursor()
        query="delete from student where id=%s"
        args=(e_id.get())   
        cursor.execute(query,args) 
        conn.commit()
        conn.close()
        e_fname.delete(0,'end')
        e_lname.delete(0,'end')
        e_email.delete(0,'end')
        e_mobile.delete(0,'end')
        msg.showinfo("Deleted Status" , "Data Deleted Successfylly")


root = Tk()
root.geometry("400x380")
root.title("My Tkinter example")
root.resizable(width=False , height=False)


Label(root, text="ID").place(x=50, y=50)
Label(root, text="FIRST NAME").place(x=50, y=100)
Label(root, text="LAST NAME").place(x=50, y=150)
Label(root, text="EMAIL").place(x=50, y=200)
Label(root, text="MOBILE").place(x=50, y=250)


e_id = Entry(root, bg="black", fg="white",
             insertbackground="white",
             highlightthickness=2,
             highlightbackground="white",
             highlightcolor="white")
e_id.place(x=200, y=50)

e_fname = Entry(root, bg="black", fg="white",
                insertbackground="white",
                highlightthickness=2,
                highlightbackground="white",
                highlightcolor="white")
e_fname.place(x=200, y=100)

e_lname = Entry(root, bg="black", fg="white",
                highlightthickness=2,
                highlightbackground="white",
                highlightcolor="white",
                insertbackground="white")
e_lname.place(x=200, y=150)

e_email = Entry(root, bg="black", fg="white",
                highlightthickness=2,
                highlightbackground="white",
                highlightcolor="white",
                insertbackground="white")
e_email.place(x=200, y=200)

e_mobile = Entry(root, bg="black", fg="white",
                 highlightthickness=2,
                 highlightbackground="white",
                 highlightcolor="white",
                 insertbackground="white")
e_mobile.place(x=200, y=250)

# Buttons
Button(root, text="INSERT",command=insert_data).place(x=50, y=350)
Button(root, text="SEARCH",command=search_data).place(x=120, y=350)
Button(root, text="UPDATE",command=Update_data).place(x=210, y=350)
Button(root, text="DELETE",command=Delete_data).place(x=300, y=350)

root.mainloop()