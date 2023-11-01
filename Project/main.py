import tkinter as tk
from tkinter import ttk
import sqlite3


class Main(tk.Frame):
    def __init__(self,root):
        super().__init__(root)
        self.init_main()
        self.db=db
        self.view_records()
#инструменты
    def init_main(self):
         toolbar=tk.Frame(bg='#d7d7d7',bd=2) 
         toolbar.pack(side=tk.TOP,fill=tk.X)

         self.img_add=tk.PhotoImage(file='./img/add.png') 
         btn_add=tk.Button(toolbar,text='Добавить',bg='#d7d7d7',
         bd=0,image=self.img_add,
         command=self.open_child)
   
         btn_add.pack(side=tk.LEFT)

         self.img_upd = tk.PhotoImage(file='./img/update.png')
         btn_upd = tk.Button(toolbar, text='Изменить', bg='#d7d7d7',
                            bd=0, image=self.img_upd,
                            command=self.open_update_child)
         btn_upd.pack(side=tk.LEFT)

         self.img_del = tk.PhotoImage(file='./img/delete.png')
         btn_del = tk.Button(toolbar, text='Удалить', bg='#d7d7d7',
                            bd=0, image=self.img_del,
                            command=self.delete_records)
         btn_del.pack(side=tk.LEFT)
        
         self.img_search = tk.PhotoImage(file='./img/search.png')
         btn_search = tk.Button(toolbar,text='Найти', bg='#d7d7d7',
                            bd=0, image=self.img_search,
                            command=self.open_search)
         btn_search.pack(side=tk.LEFT)

         self.img_refresh = tk.PhotoImage(file='./img/refresh.png')
         btn_refresh= tk.Button(toolbar,text='Найти', bg='#d7d7d7',
                            bd=0, image=self.img_refresh,
                            command=self.view_records)
         btn_refresh.pack(side=tk.LEFT)

         self.tree=ttk.Treeview(self,columns=('id','name','phone','email','salary'),
        height=17,show='headings')
         self.tree.column('id',width=45,anchor=tk.CENTER)
         self.tree.column('name',width=300,anchor=tk.CENTER) 
         self.tree.column('phone',width=150,anchor=tk.CENTER)
         self.tree.column('email',width=150,anchor=tk.CENTER)
         self.tree.column('salary',width=150,anchor=tk.CENTER)

         self.tree.heading('id',text='id')
         self.tree.heading('name',text='ФИО')
         self.tree.heading('phone',text='Телефон')
         self.tree.heading('email',text='E-mail')
         self.tree.heading('salary',text='Зарплата')

         self.tree.pack(side=tk.LEFT)

         scroll=tk.Scrollbar(self,command=self.tree.yview)
         scroll.pack(side=tk.LEFT,fill=tk.Y)
         self.tree.configure(yscrollcommand=scroll.set)
 
    def records(self,name,phone,email,salary):
        self.db.insert_data(name,phone,email,salary)
        self.view_records()
    

    def update_record(self,name,phone,email,salary):
        id=self.tree.set(self.tree.selection()[0],'#1')
        self.db.cur.execute('''
    UPDATE employees
    SET name=?, phone=?, email=?,salary=?
    WHERE id=?
            ''', (name, phone, email,salary, id))
        self.db.conn.commit()
        self.view_records()

    def delete_records(self):
        for row in self.tree.selection():
            self.db.cur.execute('DELETE FROM employees WHERE id = ?',
                                (self.tree.set(row, '#1'), ))
        self.db.conn.commit()
        self.view_records()

#поиск 
    def view_records(self):
        self.db.cur.execute('SELECT * FROM employees') 
        [ self.tree.delete(i) for i in self.tree.get_children()]  
        [self.tree.insert('','end',values=i) for i  in self.db.cur.fetchall()] 

    def search_records(self, name):
        self.db.cur.execute('SELECT * FROM employees WHERE name LIKE ?', 
                            ('%' + name + '%', ))
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=i) for i in self.db.cur.fetchall()]

    def open_child(self):
        Child()

    def open_update_child(self):
        Update()

    def open_search(self):
        Search()


class Child(tk.Toplevel):
     def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view=app

     def init_child(self):
        self.title('Добавление сотрудника')
        self.geometry('400x200')
        self.resizable(False,False)

        self.grab_set()

        self.focus_set()

        Label_name=tk.Label(self,text='ФИО:')
        Label_name.place(x=50,y=50)
        Label_phone=tk.Label(self,text="Телефон")
        Label_phone.place(x=50,y=80)
        Label_email=tk.Label(self,text="E-mail")
        Label_email.place(x=50,y=110)
        Label_salary=tk.Label(self,text="Зарплата")
        Label_salary.place(x=50,y=140)
        
        
        self.entry_name=tk.Entry(self)
        self.entry_name.place(x=200,y=50)
        self.entry_phone=tk.Entry(self)
        self.entry_phone.place(x=200,y=80)
        self.entry_email=tk.Entry(self)
        self.entry_email.place(x=200,y=110)
        self.entry_salary=tk.Entry(self)
        self.entry_salary.place(x=200,y=140)
     
        btn_cancel=tk.Button(self,text='Закрыть',command=self.destroy)
        btn_cancel.place(x=200,y=165)
       
        self.btn_add=tk.Button(self,text='Добавить')
        self.btn_add.bind('<Button-1>',lambda ev:self.view.records(self.entry_name.get(),
                                                             self.entry_phone.get(),
                                                             self.entry_email.get(),
                                                             self.entry_salary.get()))
        self.btn_add.place(x=265,y=165)

#обновление
class Update(Child):
    def __init__(self):
        super().__init__()
        self.init_update()
        self.db=db
        self.default_data()

#кнопка изменения 
    def init_update(self):
        self.title('Изменение сотрудника')
        self.btn_add.destroy()
        self.btn_upd = tk.Button(self, text='Изменить')
        self.btn_upd.bind('<Button-1>', 
                          lambda ev: self.view.update_record(self.entry_name.get(),
                                                             self.entry_phone.get(),
                                                             self.entry_email.get(),
                                                             self.entry_salary.get()))
        self.btn_upd.bind('<Button-1>', lambda ev: self.destroy(), add='+')                                                    
        self.btn_upd.place(x=265, y=165)


    def default_data(self):
        id = self.view.tree.set(self.view.tree.selection()[0], '#1')
        self.db.cur.execute('SELECT * from employees WHERE id = ?', (id))
        row = self.db.cur.fetchone()
        self.entry_name.insert(0, row[1])
        self.entry_phone.insert(0, row[2])
        self.entry_email.insert(0, row[3])
        self.entry_salary.insert(0, row[4])

class Search(tk.Toplevel):
      def __init__(self):
        super().__init__(root)
        self.init_search()
        self.view=app
     
     
      def init_search(self):
        self.title('Поиск')
        self.geometry('300x100')
        self.resizable(False,False)

        self.grab_set()

        self.focus_set()

        Label_name=tk.Label(self,text='ФИО:')
        Label_name.place(x=30,y=30)
       
        self.entry_name=tk.Entry(self)
        self.entry_name.place(x=130,y=30)
        
        btn_cancel=tk.Button(self,text='Закрыть',command=self.destroy)
        btn_cancel.place(x=150,y=70)
       
        self.btn_add=tk.Button(self,text='Поиск')
        self.btn_add.bind('<Button-1>', lambda ev:self.view.search_records(self.entry_name.get()))
                                                           
        self.btn_add.place(x=225,y=70)
#создание таблицы
class Database():
    def  __init__(self):
        self.conn=sqlite3.connect('Employee.db')
        self.cur=self.conn.cursor()
        self.cur.execute('''  CREATE TABLE IF NOT EXISTS employees(
                     id INTEGER PRIMARY KEY,
                     name TEXT,
                     phone TEXT,
                     email TEXT,
                     salary INTEGER) ''' ) 
        self.conn.commit()
    
    def insert_data(self,name,phone,email,salary):
        self.cur.execute('''
        INSERT INTO employees(name,phone,email,salary) 
        VALUES(?,?,?,?)''',(name,phone,email,salary))  
        self.conn.commit()

#запуск
if  __name__=='__main__':
    root=tk.Tk() 
    db=Database()
    app=Main(root) 
    app.pack()
    root.title('Список сотрудников компании')
    root.geometry('820x400') 
    root.resizable(False,False)
    root.mainloop()
    
