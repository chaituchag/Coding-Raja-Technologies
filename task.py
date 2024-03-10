import json
from datetime import datetime, date
import tkinter as tk
from tkinter import messagebox

class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        return super().default(obj)

class ToDoList:
    def __init__(self, filename="tasks.json"):
        self.filename = filename
        self.tasks = []
        self.load_tasks()

    def load_tasks(self):
        try:
            with open(self.filename, 'r') as file:
                self.tasks = json.load(file)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            self.tasks = []

    def save_tasks(self):
        with open(self.filename, 'w') as file:
            json.dump(self.tasks, file, indent=2, cls=DateTimeEncoder)

    def add_task(self, title, priority="medium", due_date=None):
        task = {"title": title, "priority": priority, "due_date": due_date, "completed": False}
        self.tasks.append(task)
        self.save_tasks()

    def remove_task(self, index):
        if 0 <= index < len(self.tasks):
            del self.tasks[index]
            self.save_tasks()

    def mark_completed(self, index):
        if 0 <= index < len(self.tasks):
            self.tasks[index]["completed"] = True
            self.save_tasks()

    def get_tasks(self):
        return self.tasks

class ToDoApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("To-Do List App")
        self.geometry("600x400")
        self.configure(bg="gray") 

        self.todo_list = ToDoList()

        self.create_widgets()

    def create_widgets(self):
        self.task_listbox = tk.Listbox(self, width=80, height=15, font=("boulder", 12), selectbackground="teal", selectmode=tk.SINGLE)
        self.task_listbox.pack(pady=10, padx=10)

        self.refresh_tasks()

        add_button = tk.Button(self, text="Add Task", command=self.add_task, font=("boulder", 12), bg="aqua", fg="black")
        add_button.pack(pady=5)

        remove_button = tk.Button(self, text="Remove Task", command=self.remove_task, font=("boulder", 12), bg="navy", fg="black")
        remove_button.pack(pady=5)

        complete_button = tk.Button(self, text="Mark as Completed", command=self.mark_completed, font=("boulder", 12), bg="darkred", fg="black")
        complete_button.pack(pady=5)

    def refresh_tasks(self):
        self.task_listbox.delete(0, tk.END)
        tasks = self.todo_list.get_tasks()
        for task in tasks:
            title = task.get("title", "No Title")
            priority = task.get("priority", "No Priority")
            due_date = task.get("due_date", "No Due Date")
            completed_status = "Done" if task.get("completed", False) else "Not Done"
            task_info = f"Title: {title:<30} | Priority: {priority:<15} | Due Date: {due_date:<15} | {completed_status}"
            self.task_listbox.insert(tk.END, task_info)

    def add_task(self):
        add_window = tk.Toplevel(self)
        add_window.title("Add Task")

        title_label = tk.Label(add_window, text="Enter task title:", font=("Arial", 12))
        title_label.pack(pady=5)

        title_entry = tk.Entry(add_window, font=("Arial", 12))
        title_entry.pack(pady=5)

        priority_label = tk.Label(add_window, text="Enter task priority (high/medium/low):", font=("Arial", 12))
        priority_label.pack(pady=5)

        priority_entry = tk.Entry(add_window, font=("Arial", 12))
        priority_entry.pack(pady=5)

        due_date_label = tk.Label(add_window, text="Enter due date (YYYY-MM-DD):", font=("Arial", 12))
        due_date_label.pack(pady=5)

        due_date_entry = tk.Entry(add_window, font=("Arial", 12))
        due_date_entry.pack(pady=5)

        add_button = tk.Button(add_window, text="Add Task", command=lambda: self.add_task_from_entry(add_window, title_entry, priority_entry, due_date_entry), font=("Arial", 12), bg="green", fg="white")
        add_button.pack(pady=5)

    def add_task_from_entry(self, add_window, title_entry, priority_entry, due_date_entry):
        title = title_entry.get()
        priority = priority_entry.get()
        due_date_str = due_date_entry.get()
        due_date = datetime.strptime(due_date_str, "%Y-%m-%d") if due_date_str else None

        self.todo_list.add_task(title, priority, due_date)
        self.refresh_tasks()
        add_window.destroy()

    def remove_task(self):
        selected_index = self.task_listbox.curselection()
        if selected_index:
            index = selected_index[0]
            self.todo_list.remove_task(index)
            self.refresh_tasks()
        else:
            messagebox.showinfo("Error", "Please select a task to remove.")

    def mark_completed(self):
        selected_index = self.task_listbox.curselection()
        if selected_index:
            index = selected_index[0]
            self.todo_list.mark_completed(index)
            self.refresh_tasks()
        else:
            messagebox.showinfo("Error", "Please select a task to mark as completed.")

if __name__ == "__main__":
    app = ToDoApp()
    app.mainloop()
