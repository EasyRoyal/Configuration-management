import argparse
import csv
from datetime import datetime

class Config:
    def __init__(self):
        self.vfs_path = None
        self.log_file = None
        self.script_path = None
        self.debug = False
    
    def parse_arguments(self):
        """Парсинг параметров командной строки"""
        parser = argparse.ArgumentParser(description='Эмулятор командной строки')
        parser.add_argument('--vfs', help='Путь к физическому расположению VFS')
        parser.add_argument('--log', help='Путь к лог-файлу')
        parser.add_argument('--script', help='Путь к стартовому скрипту')
        parser.add_argument('--debug', action='store_true', help='Включить отладочный вывод')
        
        args = parser.parse_args()
        
        self.vfs_path = args.vfs
        self.log_file = args.log
        self.script_path = args.script
        self.debug = args.debug
        
        # Отладочный вывод параметров
        if self.debug:
            self._print_debug_info()
    
    def _print_debug_info(self):
        """Отладочный вывод всех заданных параметров"""
        print("=== Отладочная информация ===")
        print(f"Путь к VFS: {self.vfs_path}")
        print(f"Путь к лог-файлу: {self.log_file}")
        print(f"Путь к стартовому скрипту: {self.script_path}")
        print("=============================")

class Logger:
    """Логирование событий вызова команд"""
    def __init__(self, log_file):
        self.log_file = log_file
    
    def log_command(self, command, success=True, error_msg=""):
        """Логирование команды в CSV формате"""
        if not self.log_file:
            return
            
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            with open(self.log_file, 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([timestamp, command, success, error_msg])
        except Exception as e:
            print(f"Ошибка логирования: {e}")