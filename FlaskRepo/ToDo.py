class Task:
    def __init__(self, task_id, description, due_date=None, completed=False):
        self.task_id = task_id
        self.description = description
        self.due_date = due_date
        self.completed = completed

    def __str__(self):
        status = "✔️" if self.completed else "❌"
        due = f" (Due: {self.due_date})" if self.due_date else ""
        return f"[{self.task_id}] {self.description}{due} - Status: {status}"

class TodoList:
    def __init__(self):
        self.tasks = []

    def add_task(self, description, due_date=None):
        task_id = len(self.tasks) + 1  # Simple auto-increment for task IDs
        new_task = Task(task_id, description, due_date)
        self.tasks.append(new_task)
        print(f"Task added: {new_task}")

    def view_tasks(self):
        if not self.tasks:
            print("No tasks found.")
            return
        for task in self.tasks:
            print(task)

    def update_task(self, task_id, description=None, due_date=None, completed=None):
        for task in self.tasks:
            if task.task_id == task_id:
                if description is not None:
                    task.description = description
                if due_date is not None:
                    task.due_date = due_date
                if completed is not None:
                    task.completed = completed
                print(f"Task updated: {task}")
                return
        print("Task not found.")

    def delete_task(self, task_id):
        for task in self.tasks:
            if task.task_id == task_id:
                self.tasks.remove(task)
                print(f"Task deleted: {task_id}")
                return
        print("Task not found.")

def main():
    todo_list = TodoList()

    while True:
        print("\nTo-Do List Menu:")
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Update Task")
        print("4. Delete Task")
        print("5. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            description = input("Enter task description: ")
            due_date = input("Enter due date (optional): ")
            todo_list.add_task(description, due_date if due_date else None)
        elif choice == '2':
            todo_list.view_tasks()
        elif choice == '3':
            task_id = int(input("Enter task ID to update: "))
            description = input("Enter new description (leave blank to keep current): ")
            due_date = input("Enter new due date (leave blank to keep current): ")
            completed_input = input("Mark as completed? (y/n): ").lower()
            completed = True if completed_input == 'y' else False
            todo_list.update_task(task_id, description if description else None,
                                  due_date if due_date else None,
                                  completed)
        elif choice == '4':
            task_id = int(input("Enter task ID to delete: "))
            todo_list.delete_task(task_id)
        elif choice == '5':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
