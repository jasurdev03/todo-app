import tkinter as tk
from tkinter import messagebox, simpledialog
import sqlite3
from datetime import datetime

# Vazifalarni IDlarini saqlash uchun ro'yxat
task_ids = []

# SQLite bazasini yaratish
def create_db():
    try:
        conn = sqlite3.connect("todo.db")
        c = conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY,
                task TEXT NOT NULL,
                completed BOOLEAN NOT NULL DEFAULT 0,
                completed_at TEXT
            )
        """)
        conn.commit()
        conn.close()
    except Exception as e:
        messagebox.showerror("Database Error", f"Error creating database: {str(e)}")

# Vazifalarni yuklash
def load_tasks():
    try:
        task_list.delete(0, tk.END)
        completed_list.delete(0, tk.END)
        task_ids.clear()
        
        conn = sqlite3.connect("todo.db")
        c = conn.cursor()
        c.execute("SELECT id, task, completed, completed_at FROM tasks")
        tasks = c.fetchall()
        conn.close()

        for task in tasks:
            task_id, task_name, is_completed, completed_at = task
            if is_completed:
                completed_list.insert(tk.END, f"{task_name} (Completed at: {completed_at})")
            else:
                task_list.insert(tk.END, task_name)
                task_ids.append(task_id)  # IDlarni saqlash
    except Exception as e:
        messagebox.showerror("Database Error", f"Error loading tasks: {str(e)}")

# Vazifani qo'shish
def add_task():
    try:
        task = task_entry.get().strip()
        if task:
            conn = sqlite3.connect("todo.db")
            c = conn.cursor()
            c.execute("INSERT INTO tasks (task) VALUES (?)", (task,))
            conn.commit()
            conn.close()
            task_entry.delete(0, tk.END)
            load_tasks()
        else:
            messagebox.showwarning("Input Error", "Please enter a task.")
    except Exception as e:
        messagebox.showerror("Database Error", f"Error adding task: {str(e)}")

# Vazifani o'chirish
def delete_task():
    try:
        selected_index = task_list.curselection()[0]
        task_id = task_ids[selected_index]
        
        conn = sqlite3.connect("todo.db")
        c = conn.cursor()
        c.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        conn.commit()
        conn.close()
        load_tasks()
    except IndexError:
        messagebox.showwarning("Selection Error", "Please select a task to delete.")
    except Exception as e:
        messagebox.showerror("Database Error", f"Error deleting task: {str(e)}")

# Vazifani tahrirlash
def edit_task():
    try:
        selected_index = task_list.curselection()[0]
        task_id = task_ids[selected_index]
        old_task = task_list.get(selected_index)
        
        new_task = simpledialog.askstring("Edit Task", "Enter new task:", initialvalue=old_task)
        if new_task:
            conn = sqlite3.connect("todo.db")
            c = conn.cursor()
            c.execute("UPDATE tasks SET task = ? WHERE id = ?", (new_task, task_id))
            conn.commit()
            conn.close()
            load_tasks()
    except IndexError:
        messagebox.showwarning("Selection Error", "Please select a task to edit.")
    except Exception as e:
        messagebox.showerror("Database Error", f"Error editing task: {str(e)}")

# Vazifani bajarildi sifatida belgilash
def mark_completed():
    try:
        selected_index = task_list.curselection()[0]
        task_id = task_ids[selected_index]
        completed_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        conn = sqlite3.connect("todo.db")
        c = conn.cursor()
        c.execute("UPDATE tasks SET completed = 1, completed_at = ? WHERE id = ?", (completed_at, task_id))
        conn.commit()
        conn.close()
        load_tasks()
    except IndexError:
        messagebox.showwarning("Selection Error", "Please select a task to mark as completed.")
    except Exception as e:
        messagebox.showerror("Database Error", f"Error marking task as completed: {str(e)}")

# Tkinter oynasi
root = tk.Tk()
root.title("To-Do List with Completion Time")

# Ma'lumotlar bazasini yaratish
create_db()

# Qo'shish maydoni va tugmasi
task_entry = tk.Entry(root, font=("Arial", 16), width=50)
task_entry.place(x=50, y=50)

add_button = tk.Button(root, text="Add Task", font=("Arial", 14), bg="#4CAF50", fg="white", command=add_task)
add_button.place(x=800, y=45, width=150, height=40)

# Vazifalar ro'yxati
task_list = tk.Listbox(root, font=("Arial", 14), width=40, height=15, selectmode=tk.SINGLE)
task_list.place(x=50, y=150)

# Bajarilgan vazifalar ro'yxati
completed_list = tk.Listbox(root, font=("Arial", 14), width=40, height=15, selectmode=tk.SINGLE)
completed_list.place(x=500, y=150)

# Belgilar
tk.Label(root, text="Pending tasks", font=("Arial", 14, "bold"), fg="#5E35B1").place(x=50, y=120)
tk.Label(root, text="Completed tasks", font=("Arial", 14, "bold"), fg="#5E35B1").place(x=500, y=120)

# Tugmalar (o'ng tomondan boshlanadi)
delete_button = tk.Button(root, text="Delete", font=("Arial", 14), bg="#D32F2F", fg="white", command=delete_task)
delete_button.place(x=800, y=600, width=150, height=40)

completed_button = tk.Button(root, text="Completed", font=("Arial", 14), bg="#00C853", fg="white", command=mark_completed)
completed_button.place(x=600, y=600, width=150, height=40)

edit_button = tk.Button(root, text="Edit", font=("Arial", 14), bg="#FFC107", fg="black", command=edit_task)
edit_button.place(x=400, y=600, width=150, height=40)

# Vazifalarni yuklash
load_tasks()

# Tkinter siklini boshlash
root.geometry("1000x700")
root.mainloop()
