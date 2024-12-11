import heapq
import json
import os

class TaskManager:
    def __init__(self, filename="tasks.json"):
        # Inicializa el gestor de tareas con un archivo para persistir los datos
        self.tasks = []  # Lista que actuará como heap de tareas pendientes
        self.completed_tasks = set()  # Conjunto para almacenar tareas completadas
        self.filename = filename  # Nombre del archivo donde se guardan las tareas
        self.load_tasks()  # Carga las tareas desde el archivo

    def load_tasks(self):
        # Carga las tareas desde un archivo JSON, si existe
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as file:
                data = json.load(file)  # Carga los datos del archivo JSON
                self.tasks = data.get("tasks", [])  # Tareas pendientes
                self.completed_tasks = set(data.get("completed_tasks", []))  # Tareas completadas
                heapq.heapify(self.tasks)  # Convierte la lista de tareas en un heap válido

    def save_tasks(self):
        # Guarda las tareas pendientes y completadas en un archivo JSON
        with open(self.filename, 'w') as file:
            json.dump({"tasks": self.tasks, "completed_tasks": list(self.completed_tasks)}, file)

    def add_task(self, name, priority, dependencies=None, due_date=None):
        # Añade una nueva tarea al sistema
        if not name.strip():  # Verifica que el nombre de la tarea no esté vacío
            raise ValueError("El nombre de la tarea no puede estar vacío.")
        if not isinstance(priority, int):  # Verifica que la prioridad sea un número entero
            raise ValueError("La prioridad debe ser un número entero.")
        dependencies = dependencies or []  # Asegura que las dependencias sean una lista

        task = {
            "name": name,  # Nombre de la tarea
            "priority": priority,  # Prioridad de la tarea
            "dependencies": dependencies,  # Lista de dependencias
            "due_date": due_date  # Fecha de vencimiento opcional
        }
        heapq.heappush(self.tasks, (priority, task))  # Añade la tarea al heap
        self.save_tasks()  # Guarda los cambios en el archivo

    def show_tasks(self):
        # Muestra todas las tareas pendientes, ordenadas por prioridad y fecha de vencimiento
        sorted_tasks = sorted(self.tasks, key=lambda x: (x[0], x[1]["due_date"] or ""))
        for priority, task in sorted_tasks:
            print(f"Tarea: {task['name']}, Prioridad: {priority}, Fecha de vencimiento: {task['due_date']}, Dependencias: {task['dependencies']}")

    def complete_task(self, task_name):
        # Marca una tarea como completada, eliminándola del heap y actualizando las dependencias
        remaining_tasks = []  # Lista temporal para almacenar tareas no completadas
        task_found = False  # Bandera para verificar si se encontró la tarea

        while self.tasks:
            priority, task = heapq.heappop(self.tasks)  # Extrae la tarea con mayor prioridad
            if task["name"] == task_name:
                task_found = True  # Marca que se encontró la tarea
                self.completed_tasks.add(task_name)  # Añade la tarea al conjunto de completadas
            else:
                remaining_tasks.append((priority, task))  # Guarda las tareas no completadas

        if not task_found:
            print(f"La tarea '{task_name}' no se encontró.")

        for task in remaining_tasks:
            heapq.heappush(self.tasks, task)  # Restaura las tareas al heap

        self.save_tasks()  # Guarda los cambios en el archivo

    def next_task(self):
        # Obtiene la siguiente tarea de mayor prioridad si es ejecutable
        if self.tasks:
            priority, task = self.tasks[0]  # Consulta la tarea con mayor prioridad
            if self.is_executable(task):  # Verifica si todas las dependencias están completadas
                return task
            else:
                print("La siguiente tarea no es ejecutable debido a dependencias no completadas.")
        else:
            print("No hay tareas pendientes.")

    def is_executable(self, task):
        # Verifica si todas las dependencias de una tarea están completadas
        return all(dep in self.completed_tasks for dep in task["dependencies"])

# Ejemplo de uso
def main():
    manager = TaskManager()  # Crea una instancia del gestor de tareas

    while True:
        # Menú interactivo para gestionar tareas
        print("\nGestor de Tareas")
        print("1. Añadir tarea")
        print("2. Mostrar tareas pendientes")
        print("3. Completar tarea")
        print("4. Obtener siguiente tarea de mayor prioridad")
        print("5. Salir")

        try:
            choice = int(input("Seleccione una opción: "))  # Solicita al usuario una opción

            if choice == 1:
                # Añadir una nueva tarea
                name = input("Nombre de la tarea: ")
                priority = int(input("Prioridad de la tarea (número, menor significa mayor prioridad): "))
                dependencies = input("Dependencias (separadas por comas, si las hay): ").split(',')
                dependencies = [dep.strip() for dep in dependencies if dep.strip()]
                due_date = input("Fecha de vencimiento (opcional, formato YYYY-MM-DD): ") or None
                manager.add_task(name, priority, dependencies, due_date)

            elif choice == 2:
                # Mostrar todas las tareas pendientes
                manager.show_tasks()

            elif choice == 3:
                # Completar una tarea
                task_name = input("Nombre de la tarea a completar: ")
                manager.complete_task(task_name)

            elif choice == 4:
                # Obtener la tarea de mayor prioridad
                task = manager.next_task()
                if task:
                    print(f"Siguiente tarea de mayor prioridad: {task}")

            elif choice == 5:
                # Salir del programa
                break

            else:
                print("Opción inválida.")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()