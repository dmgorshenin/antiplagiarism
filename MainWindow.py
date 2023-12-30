import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from AntiPlagiarism import AntiPlagiarismClass
from threading import Thread


class AntiPlagiarismApp(tk.Tk):
    """Графическое приложение для функционала по борьбе с плагиатом"""

    def __init__(self):
        """Инициализация AntiPlagiarismApp"""
        super().__init__()
        self.check_activation()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        window_width = 350
        window_height = 225
        self.x_position = (screen_width - window_width) // 2
        self.y_position = (screen_height - window_height) // 2
        self.geometry(
            f"{window_width}x{window_height}+{self.x_position}+{self.y_position}")
        self.title("Anti-Plagiarism Application")
        self.antiplagiarism_class = AntiPlagiarismClass()
        self.pattern_button = ttk.Button(
            self, text="Set Pattern", command=self.show_pattern_window)
        self.text_button = ttk.Button(
            self, text="Update Database Text", command=self.show_text_window)
        self.txt_file_button = ttk.Button(
            self, text="Update Database from TXT", command=self.update_database_from_txt)
        self.search_button = ttk.Button(
            self, text="Search Plagiarism", command=self.show_search_window)
        self.pattern_button.grid(row=0, column=0, padx=50, pady=10)
        self.text_button.grid(row=1, column=0, padx=50, pady=10)
        self.txt_file_button.grid(row=2, column=0, padx=50, pady=10)
        self.search_button.grid(row=3, column=0, pady=10)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)

    def show_pattern_window(self):
        """Отображает окно для установки паттерна."""
        pattern_window = tk.Toplevel(self)
        pattern_window.title("Set Pattern")
        pattern_window.geometry(f"500x450+{self.x_position}+{self.y_position}")
        pattern_window.bind("<Control-KeyPress>", self.keypress)
        pattern_window.lift()
        pattern_widget = tk.Text(pattern_window, wrap="word")
        pattern_widget.pack(expand=True, fill="both")
        set_pattern_button = ttk.Button(
            pattern_window, text="Set Pattern", command=lambda: self.set_pattern(pattern_widget.get("1.0", "end-1c"), pattern_window))
        set_pattern_button.pack(pady=10)

    def set_pattern(self, pattern, pattern_window):
        """Устанавливает паттерн для поиска плагиата.

        Args:
            pattern (str): Текст паттерна для установки.
            pattern_window (tk.Toplevel): Верхнее окно для установки паттерна.
        """
        if not pattern:
            pattern_window.destroy()
            self.show_warning(
                pattern_window, "Pattern is not installed because you did not enter anything.")
            return
        self.pattern_text = pattern
        self.antiplagiarism_class.set_pattern(pattern)
        pattern_window.destroy()
        self.show_message(pattern_window, "Pattern set successfully.")

    def show_text_window(self):
        """Отображает окно для обновления текста в базе данных."""
        text_window = tk.Toplevel(self)
        text_window.title("Update Database Text")
        text_window.geometry(f"500x450+{self.x_position}+{self.y_position}")
        text_window.bind("<Control-KeyPress>", self.keypress)
        text_window.lift()
        text_widget = tk.Text(text_window, wrap="word", )
        text_widget.pack(expand=True, fill="both")
        update_text_button = ttk.Button(
            text_window, text="Update Database Text", command=lambda: self.update_database_text(text_widget.get("1.0", "end-1c"), text_window))
        update_text_button.pack(pady=10)

    def update_database_text(self, new_text, text_window):
        """Обновляет базу данных новым текстом.

        Args:
            new_text (str): Новый текст для добавления в базу данных.
            text_window (tk.Toplevel): Верхнее окно для обновления текста в базе данных.
        """
        if not new_text:
            text_window.destroy()
            self.show_warning(
                text_window, "Text was not updated because you did not enter anything..")
            return
        self.antiplagiarism_class.update_database_text(new_text)
        text_window.destroy()
        self.show_message(text_window, "Text updated successfully.")

    def update_database_from_txt(self):
        """Обновляет базу данных из файла TXT."""
        file_path = filedialog.askopenfilename(
            title="Select TXT File", filetypes=[("TXT files", "*.txt")])
        if file_path:
            self.antiplagiarism_class.update_database_from_txt(file_path)
            self.show_message(self, "Database updated from TXT successfully.")

    def show_search_window(self):
        """Отображает окно для поиска плагиата."""
        search_window = tk.Toplevel(self)
        search_window.title("Search Plagiarism")
        search_window.geometry(f"300x200+{self.x_position}+{self.y_position}")
        search_window.lift()
        search_methods = ["Knuth-Morris-Pratt algorithm", "Rabin-Karp algorithm",
                          "Bad Boyer-Moore algorithm", "Good Boyer-Moore algorithm"]
        selected_method = tk.StringVar()
        selected_method.set(search_methods[0])
        method_menu = ttk.Combobox(
            search_window, textvariable=selected_method, values=search_methods, state="readonly")
        method_menu.pack(pady=30)
        method_menu.config(font=("Arial", 10))
        search_button = ttk.Button(
            search_window, text="Search", command=lambda: self.search_plagiarism(selected_method.get(), search_window))
        search_button.pack(pady=30)


    def search_plagiarism(self, method, search_window):
        """Инициирует поиск плагиата.

        Args:
            method (str): Выбранный метод поиска.
            search_window (tk.Toplevel): Верхнее окно для поиска плагиата.
        """
        progress_window = tk.Toplevel(search_window)
        progress_window.title("Searching Plagiarism...")
        progress_window.geometry(
            f"300x100+{self.x_position}+{self.y_position}")
        progress_window.lift()
        progress_bar = ttk.Progressbar(
            progress_window, length=150, mode="determinate")
        progress_bar.pack(pady=30)
        progress_bar.start()
        search_window.update_idletasks()
        search_thread = Thread(
            target=self.perform_search, args=(method, progress_bar, search_window))
        search_thread.start()

    def perform_search(self, method, progress_bar, search_window):
        """Выполняет поиск плагиата.

        Args:
            method (str): Выбранный метод поиска.
            progress_bar (ttk.Progressbar): Прогресс-бар, указывающий на ход поиска.
            search_window (tk.Toplevel): Верхнее окно для поиска плагиата.
        """
        if method == "Rabin-Karp algorithm":
            result, lst = self.antiplagiarism_class.search_plagiarism_RK()
        elif method == "Knuth-Morris-Pratt algorithm":
            result, lst = self.antiplagiarism_class.search_plagiarism_KMP()
        elif method == "Bad Boyer-Moore algorithm":
            result, lst = self.antiplagiarism_class.search_plagiarism_BM_bad()
        elif method == "Good Boyer-Moore algorithm":
            result, lst = self.antiplagiarism_class.search_plagiarism_BM_good()
        progress_bar.stop()
        progress_bar.destroy()
        search_window.destroy()
        self.show_message(
            self, f"Percentage of Uniqueness ({method}): {result:.2f}%")

    @staticmethod
    def keypress(event):
        """Обрабатывает события клавиш для копирования, вырезания и вставки."""
        if event.keycode == 86:
            event.widget.event_generate('<<Paste>>')
        elif event.keycode == 67:
            event.widget.event_generate('<<Copy>>')
        elif event.keycode == 88:
            event.widget.event_generate('<<Cut>>')
    
    def check_activation(self):
        """
        Проверяет активацию приложения.

        Если ключ активации недействителен, отображает предупреждение и
        закрывает приложение. В противном случае продолжается выполнение программы.
        """
        activation_key = self.get_activation_key()
        valid_key = "6837-E85F-16E41-B2BC"
        if activation_key != valid_key:
            self.show_warning(
                self, "Invalid activation key. The application will be closed.")
            self.destroy()

    def get_activation_key(self):
        """
        Отображает окно для ввода ключа активации.

        Возвращает:
            str: Ключ активации, введенный пользователем.
        """
        activation_window = tk.Toplevel(self)
        activation_window.title("Activation")
        activation_window.geometry(f"300x150")
        activation_window.lift()
        key_label = ttk.Label(activation_window, text="Enter Activation Key:")
        key_label.pack(pady=10)
        activation_entry = ttk.Entry(activation_window, show="*")
        activation_entry.pack(pady=10)
        activate_button = ttk.Button(
            activation_window, text="Activate", command=lambda: self.verify_activation_key(activation_entry.get(), activation_window))
        activate_button.pack(pady=20)
        activation_window.wait_window(activation_window)
        return self.activation_key

    def verify_activation_key(self, key, activation_window):
        """
        Проверяет введенный ключ активации.

        Args:
            key (str): Ключ активации, введенный пользователем.
            activation_window (tk.Toplevel): Окно активации.
        """
        self.activation_key = key
        activation_window.destroy()

    def show_message(self, window, message):
        """Отображает информационное сообщение.

        Args:
            window: Родительское окно для окна сообщения.
            message (str): Сообщение для отображения.
        """
        messagebox.showinfo("Info", message)

    def show_warning(self, window, message):
        """Отображает предупреждение.

        Args:
            window: Родительское окно для окна предупреждения.
            message (str): Текст предупреждения для отображения.
        """
        messagebox.showwarning("Warning", message)


if __name__ == "__main__":
    app = AntiPlagiarismApp()
    app.mainloop()
