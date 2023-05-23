import sys
import os
import tkinter as tk
from tkinter import *
import tkinter.messagebox

# For Neo4j Connection
from neo4j import GraphDatabase
class Neo4jConnection:
    
    def _init_(self, uri, user, pwd):
        self.__uri = uri
        self.__user = user
        self.__pwd = pwd
        self.__driver = None
        try:
            self.__driver = GraphDatabase.driver(self.__uri, auth=(self.__user, self.__pwd))
        except Exception as e:
            print("Failed to create the driver:", e)
        
    def close(self):
        if self.__driver is not None:
            self.__driver.close()
        
    def query(self, query, db=None):
        assert self.__driver is not None, "Driver not initialized!"
        session = None
        response = None
        try: 
            session = self.__driver.session(database=db) if db is not None else self.__driver.session() 
            response = list(session.run(query))
        except Exception as e:
            print("Query failed:", e)
        finally: 
            if session is not None:
                session.close()
        return response
conn = Neo4jConnection(uri="bolt://localhost:7687", user="neo4j", pwd="TusharTushar")
# ^ Neo4j Connected


window = tk.Tk()
window.title("Neo4j Desktop App")
window.geometry("700x500")
window.configure(bg="grey")
blog=tk.StringVar()
blog_title=tk.StringVar()
direct_id1=tk.StringVar()
direct_id2=tk.StringVar()
recur_id1=tk.StringVar()
recur_id2=tk.StringVar()

#submitting query
def submit():
    query_string = blog_title.get()
    result = conn.query(query_string, db='neo4j')
    print(result)
    blog.set("")

def direct_check():
    id1=direct_id1.get()
    id2=direct_id2.get()
    query_string = '''MATCH p=(:Paper{id:"'''+id1+'''"})-[r:CITES]->(:Paper{id:"'''+id2+'''"}) RETURN p'''
    result = conn.query(query_string, db='neo4j')
    if(result):
        Label(window,text="YES", fg="blue",font=("Arial", 15),width=37).grid(row=160)
    else:
        Label(window,text="NO", fg="RED",font=("Arial", 15),width=37).grid(row=160)
    blog.set("")

def indirect_check():
    id1=recur_id1.get()
    id2=recur_id2.get()
    query_string = '''MATCH p=(:Paper{id:"'''+id1+'''"})-[r:CITES]->() MATCH q=(:Paper{id:"'''+id2+'''"}) RETURN q'''
    result = conn.query(query_string, db='neo4j')
    if(result):
        Label(window,text="YES", fg="blue",font=("Arial", 15),width=37).grid(row=220)
    else:
        Label(window,text="NO", fg="RED",font=("Arial", 15),width=37).grid(row=220)
    blog.set("")

#tkinter window 
Label(window,text="Neo4j Python Desktop Application", fg="black",font=("Arial", 25, 'bold'),width=37).grid(row=0,column=0)
name_label = tk.Label(window, text = 'Query', font=('calibre',10, 'bold')).grid(row=70)
name_entry = tk.Entry(window,textvariable = blog_title, font=('calibre',10,'normal'),width=70).grid(row=80)
sub_btn=tk.Button(window,text = 'Run Query', command = submit).grid(row=110)

name_label = tk.Label(window, text = 'Does Paper with id1 cites id2 directly?', font=('calibre',10, 'bold')).grid(row=120)
name_entry = tk.Entry(window,textvariable = direct_id1, font=('calibre',10,'normal')).grid(row=130)
name_entry = tk.Entry(window,textvariable = direct_id2, font=('calibre',10,'normal')).grid(row=140)
sub_btn=tk.Button(window,text = 'Check', command = direct_check).grid(row=150)

name_label = tk.Label(window, text = 'Does Paper with id1 cites id2 indirectly?', font=('calibre',10, 'bold')).grid(row=180)
name_entry = tk.Entry(window,textvariable = recur_id1, font=('calibre',10,'normal')).grid(row=190)
name_entry = tk.Entry(window,textvariable = recur_id2, font=('calibre',10,'normal')).grid(row=200)
sub_btn=tk.Button(window,text = 'Check', command = indirect_check).grid(row=210)

window.mainloop()