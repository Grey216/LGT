import sys 
import os

def setup():
    """
    Функция добавляет родительский каталог текущего каталога в sys.path для поиска модулей.
    """
    current_dir = os.path.dirname(__file__)  # Получаем путь к текущему каталогу
    parent_dir = os.path.dirname(current_dir)  # Получаем путь к родительскому каталогу
    sys.path.append(parent_dir)  # Добавляем путь к родительскому каталогу в sys.path для поиска модулей
