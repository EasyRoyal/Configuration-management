import tkinter as tk
from tkinter import scrolledtext
import os
import sys
import getpass
import shlex

class Shell:
    """Обработчик команд shell"""
    def __init__(self):
        self.commands = {
            'ls': self._cmd_ls,
            'cd': self._cmd_cd,
            'exit': self._cmd_exit
        }
        self.running = True
    
    def execute(self, command_line):
        """Выполнение команды"""
        if not command_line.strip():
            return ""
            
        try:
            # Раскрытие переменных окружения
            command_line = self._expand_env_vars(command_line)
            
            # Разделение на команду и аргументы
            parts = shlex.split(command_line)
            if not parts:
                return ""
                
            cmd_name = parts[0]
            args = parts[1:]
            
            if cmd_name in self.commands:
                return self.commands[cmd_name](args)
            else:
                return f"Ошибка: неизвестная команда '{cmd_name}'"
                
        except Exception as e:
            return f"Ошибка выполнения: {str(e)}"
    
    def _expand_env_vars(self, text):
        """Раскрытие переменных окружения типа $HOME"""
        import re
        def replace_var(match):
            var_name = match.group(1)
            return os.environ.get(var_name, f'${var_name}')
        
        return re.sub(r'\$([a-zA-Z_][a-zA-Z0-9_]*)', replace_var, text)
    
    def _cmd_ls(self, args):
        """Заглушка для команды ls"""
        return f"ls: аргументы {args}"
    
    def _cmd_cd(self, args):
        """Заглушка для команды cd"""
        return f"cd: аргументы {args}"
    
    def _cmd_exit(self, args):
        """Команда выхода"""
        self.running = False
        return "Выход из эмулятора"
    def execute_script(self, script_path):
        """Выполнение стартового скрипта"""
        try:
            with open(script_path, 'r', encoding='utf-8') as f:
                output = []
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):  # Пропуск комментариев
                        output.append(f"> {line}")
                        result = self.execute(line)
                        if result:
                            output.append(result)
                        if not self.running:
                            break
                return "\n".join(output)
        except Exception as e:
            return f"Ошибка выполнения скрипта: {str(e)}"

class ShellGUI:
    """Графический интерфейс эмулятора"""
    def __init__(self):
        self.shell = Shell()
        
        # Создание главного окна
        self.root = tk.Tk()
        self._setup_gui()
    
    def _setup_gui(self):
        """Настройка графического интерфейса"""
        # Заголовок окна на основе данных ОС
        username = getpass.getuser()
        hostname = os.uname().nodename if hasattr(os, 'uname') else os.environ.get('COMPUTERNAME', 'localhost')
        self.root.title(f"Эмулятор - [{username}@{hostname}]")
        self.root.geometry("800x600")
        
        # Текстовое поле для вывода
        self.output_text = scrolledtext.ScrolledText(
            self.root,
            wrap=tk.WORD,
            width=80,
            height=25,
            bg='black',
            fg='white',
            insertbackground='white',
            font=('Courier New', 10)
        )
        self.output_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        self.output_text.config(state=tk.DISABLED)
        
        # Фрейм для ввода команды
        input_frame = tk.Frame(self.root)
        input_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Поле ввода команды
        self.input_entry = tk.Entry(input_frame, font=('Courier New', 10))
        self.input_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.input_entry.bind('<Return>', self._on_command_enter)
        self.input_entry.focus()
        
        # Кнопка выполнения
        tk.Button(input_frame, text="Выполнить", command=self._execute_command).pack(side=tk.RIGHT, padx=5)
        
        # Приветственное сообщение
        self._print_output("Добро пожаловать в эмулятор командной строки!\n")
        self._print_output("Введите 'exit' для выхода.\n\n")
    
    def _on_command_enter(self, event=None):
        """Обработчик нажатия Enter в поле ввода"""
        self._execute_command()
    
    def _execute_command(self):
        """Выполнение команды"""
        command = self.input_entry.get().strip()
        self.input_entry.delete(0, tk.END)
        
        if command:
            self._print_output(f"> {command}\n")
            result = self.shell.execute(command)
            if result:
                self._print_output(f"{result}\n")
            
            # Проверка на выход
            if not self.shell.running:
                self.root.quit()
    
    def _print_output(self, text):
        """Вывод текста в консоль"""
        self.output_text.config(state=tk.NORMAL)
        self.output_text.insert(tk.END, text)
        self.output_text.see(tk.END)
        self.output_text.config(state=tk.DISABLED)
    
    def run(self):
        """Запуск приложения"""
        self.root.mainloop()

def main():
    """Основная функция"""
    app = ShellGUI()
    app.run()

if __name__ == "__main__":
    main()