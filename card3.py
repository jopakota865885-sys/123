# card2_gui.py - картотека с графическим интерфейсом на tkinter

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import csv
import os
from datetime import datetime

# Исходные данные
synonims = {"имя": "name", "возраст": "age", "город": "city", "рост": "height"}

# Имя файла для сохранения данных
DATA_FILE = "card_data.json"

# Начальные данные
default_data = [
    {"name": "магомед", "age": '53', "city": "париж", "height": 182},
    {"name": "даша", "age": '18', "city": "челябинск", "height": 165},
    {"name": "мария", "age": '23', "city": "челябинск", "height": 157},
    {"name": "мыкола", "age": '18', "city": "киев", "height": 176},
    {"name": "ван сай", "age": '18', "city": "токио", "height": 177},
    {"name": "сергей", "age": '18', "city": "москва", "height": 180},
    {"name": "влад", "age": '17', "city": "уфа", "height": 169},
    {"name": "вадим", "age": '27', "city": "минск", "height": 159},
    {"name": "таня", "age": '17', "city": "уфа", "height": 155},
    {"name": "вася", "age": '18', "city": "краснодар", "height": 168},
    {"name": "данила", "age": '45', "city": "уфа", "height": 171},
    {"name": "ольга", "age": '29', "city": "самара", "height": 163},
    {"name": "джон", "age": '34', "city": "лондон", "height": 170},
    {"name": "кэнди", "age": '21', "city": "чикаго", "height": 162},
    {"name": "данила", "age": '19', "city": "самара", "height": 193},
    {"name": "петр", "age": '54', "city": "новосибирск", "height": 172},
    {"name": "елена", "age": '31', "city": "екатеринбург", "height": 168},
    {"name": "карл", "age": '42', "city": "берлин", "height": 171},
    {"name": "мишель", "age": '26', "city": "москва", "height": 163},
    {"name": "сабина", "age": '22', "city": "баку", "height": 163},
    {"name": "руслан", "age": '33', "city": "алматы", "height": 174},
    {"name": "таня", "age": '28', "city": "москва", "height": 174},
    {"name": "анна", "age": '38', "city": "волгоград", "height": 171},
    {"name": "степан", "age": '41', "city": "ростов-на-дону", "height": 184},
    {"name": "нино", "age": '24', "city": "тбилиси", "height": 173},
    {"name": "дима", "age": '30', "city": "краснодар", "height": 182},
    {"name": "мария", "age": '35', "city": "рио-де-жанейро", "height": 159},
    {"name": "франсуа", "age": '47', "city": "марсель", "height": 172},
    {"name": "Лоуренс Уоткинс", "age": '27', "city": "лондон", "height": 180},
    {"name": "кирилл", "age": '20', "city": "Александровск-Сахалинский", "height": 189}
]


class CardCatalogApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Картотека")
        self.root.geometry("1000x650")

        self.li = self.load_data()
        self.current_list = self.li.copy()

        self.create_widgets()
        self.refresh_table()

    def load_data(self):
        """Загрузка данных из JSON файла"""
        try:
            if os.path.exists(DATA_FILE):
                with open(DATA_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if data:  # Если файл не пустой
                        return data
            return default_data.copy()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при загрузке данных: {str(e)}")
            return default_data.copy()

    def save_data(self):
        try:
            with open(DATA_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.li, f, ensure_ascii=False, indent=2)
            messagebox.showinfo("Успех", "Данные успешно сохранены!")
            return True
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при сохранении данных: {str(e)}")
            return False

    def export_to_txt(self):
        try:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
                title="Сохранить как текстовый файл"
            )
            if file_path:
                with open(file_path, 'w', encoding='utf-8') as f:
                    # Заголовок с датой
                    f.write(f"Экспорт картотеки\n")
                    f.write(f"Дата: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                    f.write(f"Всего записей: {len(self.li)}\n")
                    f.write("="*80 + "\n\n")

                    # Данные в виде таблицы
                    # Определение максимальной ширины колонок
                    max_name_len = max(len(person['name']) for person in self.li)
                    max_city_len = max(len(person['city']) for person in self.li)

                    # Заголовки таблицы
                    f.write(f"{'Город':<{max_city_len}} | {'Имя':<{max_name_len}} | {'Возраст':<6} | {'Рост':<4}\n")
                    f.write("-"*80 + "\n")

                    # Данные
                    for person in self.li:
                        f.write(f"{person['city']:<{max_city_len}} | {person['name']:<{max_name_len}} | {person['age']:<6} | {person['height']:<4}\n")

                messagebox.showinfo("Успех", f"Данные экспортированы в файл:\n{file_path}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при экспорте в TXT: {str(e)}")

    def export_to_csv(self):
        """Экспорт данных в CSV файл (для Excel)"""
        try:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
                title="Сохранить как CSV файл"
            )
            if file_path:
                with open(file_path, 'w', encoding='utf-8-sig', newline='') as f:
                    writer = csv.writer(f)
                    # Заголовки
                    writer.writerow(['Город', 'Имя', 'Возраст', 'Рост'])
                    # Данные
                    for person in self.li:
                        writer.writerow([person['city'], person['name'], person['age'], person['height']])

                messagebox.showinfo("Успех", f"Данные экспортированы в CSV файл:\n{file_path}\n\nФайл можно открыть в Excel")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при экспорте в CSV: {str(e)}")

    def create_widgets(self):
        # Меню
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # Меню "Файл"
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Файл", menu=file_menu)
        file_menu.add_command(label="Сохранить данные", command=self.save_data)
        file_menu.add_separator()
        file_menu.add_command(label="Экспорт в TXT", command=self.export_to_txt)
        file_menu.add_command(label="Экспорт в CSV (Excel)", command=self.export_to_csv)
        file_menu.add_separator()
        file_menu.add_command(label="Выход", command=self.root.quit)

        # Меню "Помощь"
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Помощь", menu=help_menu)
        help_menu.add_command(label="О программе", command=self.show_about)

        # Главный фрейм
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Левая часть - таблица
        left_frame = ttk.Frame(main_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Фрейм для поиска над таблицей
        search_frame = ttk.Frame(left_frame)
        search_frame.pack(fill=tk.X, pady=(0, 5))

        ttk.Label(search_frame, text="Быстрый поиск:").pack(side=tk.LEFT, padx=5)
        self.search_entry = ttk.Entry(search_frame)
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.search_entry.bind('<KeyRelease>', self.quick_search)

        # Создание таблицы Treeview
        columns = ("city", "name", "age", "height")
        self.tree = ttk.Treeview(left_frame, columns=columns, show="headings")

        # Настройка заголовков
        self.tree.heading("city", text="Город", command=lambda: self.sort_by_column("city"))
        self.tree.heading("name", text="Имя", command=lambda: self.sort_by_column("name"))
        self.tree.heading("age", text="Возраст", command=lambda: self.sort_by_column("age"))
        self.tree.heading("height", text="Рост", command=lambda: self.sort_by_column("height"))

        # Настройка ширины колонок
        self.tree.column("city", width=150)
        self.tree.column("name", width=150)
        self.tree.column("age", width=60)
        self.tree.column("height", width=60)

        # Скроллбар
        scrollbar = ttk.Scrollbar(left_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Правая часть - кнопки
        right_frame = ttk.Frame(main_frame, width=220)
        right_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=5)
        right_frame.pack_propagate(False)

        # Группа кнопок "Работа с данными"
        ttk.Label(right_frame, text="Работа с данными", font=("Arial", 10, "bold")).pack(pady=(0, 5))
        btn_print_all = ttk.Button(right_frame, text="Показать всех", command=self.print_all)
        btn_print_all.pack(fill=tk.X, pady=2)

        btn_search = ttk.Button(right_frame, text="Расширенный поиск", command=self.open_search_window)
        btn_search.pack(fill=tk.X, pady=2)

        btn_sort = ttk.Button(right_frame, text="Сортировка", command=self.open_sort_window)
        btn_sort.pack(fill=tk.X, pady=2)

        ttk.Separator(right_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)

        # Группа кнопок "Редактирование"
        ttk.Label(right_frame, text="Редактирование", font=("Arial", 10, "bold")).pack(pady=(0, 5))
        btn_add = ttk.Button(right_frame, text="Добавить запись", command=self.open_add_window)
        btn_add.pack(fill=tk.X, pady=2)

        btn_edit = ttk.Button(right_frame, text="Редактировать запись", command=self.open_edit_window)
        btn_edit.pack(fill=tk.X, pady=2)

        btn_delete = ttk.Button(right_frame, text="Удалить запись", command=self.delete_record)
        btn_delete.pack(fill=tk.X, pady=2)

        ttk.Separator(right_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)

        # Группа кнопок "Файл"
        ttk.Label(right_frame, text="Файловые операции", font=("Arial", 10, "bold")).pack(pady=(0, 5))
        btn_save = ttk.Button(right_frame, text="Сохранить в JSON", command=self.save_data)
        btn_save.pack(fill=tk.X, pady=2)

        btn_export_txt = ttk.Button(right_frame, text="Экспорт в TXT", command=self.export_to_txt)
        btn_export_txt.pack(fill=tk.X, pady=2)

        btn_export_csv = ttk.Button(right_frame, text="Экспорт в CSV", command=self.export_to_csv)
        btn_export_csv.pack(fill=tk.X, pady=2)

        ttk.Separator(right_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)

        # Кнопка сброса
        btn_reset = ttk.Button(right_frame, text="Сбросить фильтр", command=self.reset_filter)
        btn_reset.pack(fill=tk.X, pady=2)

        # Статусная строка
        self.status_var = tk.StringVar()
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        self.update_status()

    def update_status(self):
        """Обновление статусной строки"""
        if len(self.current_list) == len(self.li):
            self.status_var.set(f"Всего записей: {len(self.li)}")
        else:
            self.status_var.set(f"Показано: {len(self.current_list)} из {len(self.li)} записей")

    def sort_by_column(self, column):
        """Сортировка по клику на заголовок"""
        def sort_key(person):
            val = person[column]
            if column in ["age", "height"]:
                try:
                    return int(val)
                except:
                    return 0
            return str(val).lower()

        self.current_list.sort(key=sort_key)
        self.refresh_table()

    def quick_search(self, event=None):
        """Быстрый поиск по всем полям"""
        search_text = self.search_entry.get().strip().lower()
        if not search_text:
            self.current_list = self.li.copy()
        else:
            result = []
            for person in self.li:
                if (search_text in person['name'].lower() or
                    search_text in person['city'].lower() or
                    search_text in str(person['age']) or
                    search_text in str(person['height'])):
                    result.append(person)
            self.current_list = result
        self.refresh_table()

    def refresh_table(self):
        """Обновление таблицы"""
        for item in self.tree.get_children():
            self.tree.delete(item)

        for person in self.current_list:
            self.tree.insert("", tk.END, values=(
                person["city"],
                person["name"],
                person["age"],
                person["height"]
            ))

        self.update_status()

    def print_all(self):
        """Показать все записи"""
        self.current_list = self.li.copy()
        self.search_entry.delete(0, tk.END)
        self.refresh_table()

    def reset_filter(self):
        """Сбросить фильтр"""
        self.print_all()

    def get_selected_person(self):
        """Получить выбранную запись"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Пожалуйста, выберите запись!")
            return None

        # Получаем данные из выбранной строки
        values = self.tree.item(selected[0])['values']
        # Находим оригинальную запись в self.li
        for person in self.li:
            if (person['name'] == values[1] and
                person['city'] == values[0] and
                str(person['age']) == str(values[2]) and
                person['height'] == values[3]):
                return person
        return None

    def delete_record(self):
        """Удаление выбранной записи"""
        person = self.get_selected_person()
        if not person:
            return

        if messagebox.askyesno("Подтверждение", f"Удалить запись о {person['name']} из {person['city']}?"):
            self.li.remove(person)
            self.print_all()  # Обновляем отображение
            self.update_status()
            messagebox.showinfo("Успех", "Запись удалена!")

    def open_search_window(self):
        """Открыть окно расширенного поиска"""
        search_window = tk.Toplevel(self.root)
        search_window.title("Расширенный поиск")
        search_window.geometry("450x350")
        search_window.resizable(False, False)

        ttk.Label(search_window, text="Поиск записей", font=("Arial", 12, "bold")).pack(pady=10)

        # Создаем поля для всех критериев
        fields = {
            "city": ("Город:", tk.StringVar()),
            "name": ("Имя:", tk.StringVar()),
            "age": ("Возраст:", tk.StringVar()),
            "height": ("Рост:", tk.StringVar())
        }

        entries = {}
        for key, (label_text, var) in fields.items():
            frame = ttk.Frame(search_window)
            frame.pack(fill=tk.X, padx=20, pady=5)
            ttk.Label(frame, text=label_text, width=10).pack(side=tk.LEFT)
            entry = ttk.Entry(frame, textvariable=var)
            entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
            entries[key] = var

        def do_search():
            result = []
            for person in self.li:
                match = True
                for key, var in entries.items():
                    value = var.get().strip()
                    if value:
                        if key == "age" or key == "height":
                            if str(person[key]) != value:
                                match = False
                                break
                        else:
                            if value.lower() not in person[key].lower():
                                match = False
                                break
                if match:
                    result.append(person)

            if result:
                self.current_list = result
                self.refresh_table()
                search_window.destroy()
                messagebox.showinfo("Результат", f"Найдено записей: {len(result)}")
            else:
                messagebox.showinfo("Результат", "Ничего не найдено")

        ttk.Button(search_window, text="Найти", command=do_search).pack(pady=15)
        ttk.Button(search_window, text="Отмена", command=search_window.destroy).pack()

    def open_sort_window(self):
        """Открыть окно сортировки"""
        sort_window = tk.Toplevel(self.root)
        sort_window.title("Сортировка")
        sort_window.geometry("350x250")
        sort_window.resizable(False, False)

        ttk.Label(sort_window, text="Выберите поле для сортировки:", font=("Arial", 10, "bold")).pack(pady=10)

        fields = ["город", "имя", "возраст", "рост"]
        sort_var = tk.StringVar()
        sort_var.set(fields[0])

        order_var = tk.StringVar()
        order_var.set("по возрастанию")

        for field in fields:
            ttk.Radiobutton(sort_window, text=field.capitalize(),
                           variable=sort_var, value=field).pack(anchor=tk.W, padx=30, pady=2)

        ttk.Label(sort_window, text="Порядок сортировки:", font=("Arial", 10, "bold")).pack(pady=(10, 5))
        ttk.Radiobutton(sort_window, text="По возрастанию", variable=order_var, value="по возрастанию").pack(anchor=tk.W, padx=30)
        ttk.Radiobutton(sort_window, text="По убыванию", variable=order_var, value="по убыванию").pack(anchor=tk.W, padx=30)

        def do_sort():
            field = sort_var.get()
            key = synonims.get(field, field)
            reverse = (order_var.get() == "по убыванию")

            def sort_key(person):
                val = person[key]
                if key == "age" or key == "height":
                    try:
                        return int(val)
                    except ValueError:
                        return 0
                return val.lower()

            self.current_list.sort(key=sort_key, reverse=reverse)
            self.refresh_table()
            sort_window.destroy()
            messagebox.showinfo("Сортировка", f"Отсортировано по полю: {field}\nПорядок: {order_var.get()}")

        ttk.Button(sort_window, text="Сортировать", command=do_sort).pack(pady=15)

    def open_add_window(self):
        """Открыть окно добавления записи"""
        add_window = tk.Toplevel(self.root)
        add_window.title("Добавить запись")
        add_window.geometry("400x350")
        add_window.resizable(False, False)

        ttk.Label(add_window, text="Добавление новой записи", font=("Arial", 12, "bold")).pack(pady=10)

        entries = {}
        fields = [
            ("Имя:", "name", True),
            ("Возраст:", "age", True),
            ("Город:", "city", True),
            ("Рост:", "height", True)
        ]

        for label_text, key, required in fields:
            frame = ttk.Frame(add_window)
            frame.pack(fill=tk.X, padx=20, pady=5)
            ttk.Label(frame, text=label_text, width=10).pack(side=tk.LEFT)
            entry = ttk.Entry(frame)
            entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
            entries[key] = entry

        def do_add():
            new_person = {}
            try:
                new_person["name"] = entries["name"].get().strip()
                new_person["age"] = entries["age"].get().strip()
                new_person["city"] = entries["city"].get().strip()
                height = entries["height"].get().strip()
                new_person["height"] = int(height) if height else 0

                if not new_person["name"]:
                    messagebox.showerror("Ошибка", "Имя обязательно для заполнения!")
                    return

                if not new_person["age"]:
                    messagebox.showerror("Ошибка", "Возраст обязателен для заполнения!")
                    return

                self.li.append(new_person)
                self.print_all()
                add_window.destroy()
                messagebox.showinfo("Успех", "Запись добавлена!")

            except ValueError:
                messagebox.showerror("Ошибка", "Рост должен быть числом!")
            except Exception as e:
                messagebox.showerror("Ошибка", str(e))

        ttk.Button(add_window, text="Добавить", command=do_add).pack(pady=15)
        ttk.Button(add_window, text="Отмена", command=add_window.destroy).pack()

    def open_edit_window(self):
        """Открыть окно редактирования записи"""
        person = self.get_selected_person()
        if not person:
            return

        edit_window = tk.Toplevel(self.root)
        edit_window.title("Редактировать запись")
        edit_window.geometry("400x350")
        edit_window.resizable(False, False)

        ttk.Label(edit_window, text="Редактирование записи", font=("Arial", 12, "bold")).pack(pady=10)

        entries = {}
        fields = [
            ("Имя:", "name"),
            ("Возраст:", "age"),
            ("Город:", "city"),
            ("Рост:", "height")
        ]

        for label_text, key in fields:
            frame = ttk.Frame(edit_window)
            frame.pack(fill=tk.X, padx=20, pady=5)
            ttk.Label(frame, text=label_text, width=10).pack(side=tk.LEFT)
            entry = ttk.Entry(frame)
            entry.insert(0, str(person[key]))
            entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
            entries[key] = entry

        def do_edit():
            try:
                person["name"] = entries["name"].get().strip()
                person["age"] = entries["age"].get().strip()
                person["city"] = entries["city"].get().strip()
                height = entries["height"].get().strip()
                person["height"] = int(height) if height else 0

                if not person["name"]:
                    messagebox.showerror("Ошибка", "Имя обязательно для заполнения!")
                    return

                self.refresh_table()
                edit_window.destroy()
                messagebox.showinfo("Успех", "Запись обновлена!")

            except ValueError:
                messagebox.showerror("Ошибка", "Рост должен быть числом!")
            except Exception as e:
                messagebox.showerror("Ошибка", str(e))

        ttk.Button(edit_window, text="Сохранить", command=do_edit).pack(pady=15)
        ttk.Button(edit_window, text="Отмена", command=edit_window.destroy).pack()

    def show_about(self):
        """Информация о программе"""
        about_text = """Картотека - программа для управления базой данных

Версия: 2.0
Разработчик: Python + Tkinter

Функции:
• Просмотр и редактирование записей
• Поиск и сортировка
• Сохранение в JSON
• Экспорт в TXT и CSV

Поддерживаемые форматы:
• JSON - внутренний формат
• CSV - совместим с Excel
• TXT - текстовый файл

Для работы программы не требуются дополнительные модули.
"""
        messagebox.showinfo("О программе", about_text)


if __name__ == "__main__":#проверяет имя текущего модуля и начинат выполнение
    root = tk.Tk() #главное окно программы
    app = CardCatalogApp(root) 
    root.mainloop()
