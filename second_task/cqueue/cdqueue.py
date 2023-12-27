"""
Модуль cdqueue, реализует структуру данных циклической очереди в основе которой deque из модуля collections.

Класса CDQueue, представляет циклическую очередь.
Очередь предоставляет возможности: 
- добавления элемента
- удаления элемента и его возврат
- возвращение ссылки на первый элемент
- возвращение ссылки на последний элемент
- проверка на пустоту
- проверка на заполненость
- колличество элементов
- очищение очереди
- преобразование очереди в список
- вставка элемента по индексу
- удаление конкретного элемента
- изменение размерности очереди   
"""
from dataclasses import dataclass,field
from typing import Optional,TypeVar,Generic,Generator,Any
import sys
from collections import deque
try:
    from qexception import QFullError,QEmptyError
except ImportError:
    from .qexception import QFullError,QEmptyError

T = TypeVar("T") # Обобщенный тип данных

class CDQueue(Generic[T]):
    
    """
    Реализация циклической структуры данных FIFO на основе deque из модуля collections.
    
    attr:
    _buf (deque[T]): Контейнер Очереди
    
    method:
    empty()->None: Возращает True, если очередь пустая иначе False
    is_full()->bool: Возращает True, если очередь полная иначу False
    length()->int: Возвращает количество элементов в очереди
    clear()->None: Очищение очереди
    front()->T: Возращает ссылку на первый элемент в очереди
    back()->T: Возращает ссылку на последний элемент в очереди
    pop()->T: Удаляет и возращает первый элемент в очереди
    push(value:T,raplace:bool=False)->None: Добавляет элемент в конец очереди
    aslist()->list[T]: Возращает очередь в виде списка
    resize(new_size:int)->None: Увеличивает размер очереди
    insert(index:int, value:T)->None: Вставляет элемент в очередь по индексу
    remove(value:T)->None: Удаляет первое вхождение значения из очереди
    """
    
    def __init__(self,max_size:int) -> None:
        """
        Инициализация пустой очереди
        
        param:
        max_size (int): Размер очереди
        """
        assert max_size>0,"Очередь не может быть отрицательной или равной 0"
        self._buf:deque[T] = deque(maxlen=max_size)
    
    def empty(self)->bool:
        """
        Проверяет, пуста ли очередь.

        return:
        (bool): True, если очередь пуста, иначе False.
        """
        return len(self._buf)==0
    
    def is_full(self)->bool:
        """
        Проверяет, полная ли очередь
        
        return:
        (bool): True, если очередь полная, иначе False.
        """
        return len(self._buf) == self._buf.maxlen
    
    def length(self)->int:
        """
        Возвращает количество элементов в очереди.

        return:
        (int): Количество элементов в очереди.
        """
        return len(self._buf)
    
    def clear(self)->None:
        """
        Очищает очередь, удаляя все элементы.
        
        return:
        (None)
        """
        self._buf.clear()
    
    def __len__(self)->int:
        """
        Возвращает количество элементов в очереди (магический метод).

        return:
        (int): Количество элементов в очереди.
        """
        return self.length()
    
    def front(self)->T:
        """
        Возвращает ссылку на первый элемент очереди без его удаления.

        raise:
        (QEmptyError): Если очередь пуста.

        return:
        (T): Первый элемент очереди.
        """
        if self.empty():
            raise QEmptyError()
        return self._buf[0]
    
    def back(self)->T:
        """
        Возвращает ссылку на последний элемент очереди без его удаления.

        raise:
        (QEmptyError): Если очередь пуста.

        return:
        (T): Последний элемент очереди.
        """
        if self.empty():
            raise QEmptyError()
        return self._buf[-1]
    
    def pop(self)->T:
        """
        Удаляет и возвращает первый элемент очереди.

        raise:
        (QEmptyError): Если очередь пуста.

        return:
        (T) : Удаленный первый элемент очереди.
        """
        if self.empty():
            raise QEmptyError()
        
        return self._buf.popleft()
    
    def push(self,value:T,replace:bool = False)->None:
        """
        Добавляет элемент в конец очереди. 
        1)Если очередь переполнена и replace= False, то поднимаем исключение. 
        2)Если очередь переполнена и replace= True, то удаляем первый элемент очереди и вставляем новый. 

        raise:
        (QFullError): Если очередь заполнена.
        
        param:
        value (T): Элемент для добавления в очередь.
        replace (bool): Указывает на то, что нужно ли удалять первый элемент при переполнении
        """
        if self.is_full() and not replace:
            raise QFullError()
        self._buf.append(value)
    
    def resize(self,new_size:int)->None:
        """
        Увеличивает размер очереди.
        
        raise:
        (ValueError): Если размер отрицательный
        
        param:
        new_size (int): Размер очереди                 
        """
        if new_size<=0:
            raise ValueError("Размер очереди должен быть больше 0")
        self._buf = deque(self._buf,maxlen=new_size) 

    
    def insert(self,index:int, value:T)->None:
        """ 
        Вставляет элемент в очередь по индексу.
        
        Если индекс отрицательный, то элемент вставляется в начало очереди.
        Если индекс больше кол-ва находящихся элементов в очереди, то  
        элемент вставляется в конец очереди. 
        
        raise:
        (QFullError): Если очередь заполнена.
        
        param:
        index (int): Вставка элемента в позициию указаным индексом.
        value (T): Элемент для добавления в очередь.        
        """
        if self.is_full():
            raise QFullError()
           
        self._buf.insert(index,value)
    
    def remove(self,value:T)->None:
        """ 
        Удаляет первое вхождение значения из очереди
        
        raise:
        (QEmptyError): Если очередь пуста.  
        (ValueError): Если очередь не имеет элемент с указаным значением
        
        param:
        value (T): Элемент для удаления из очереди.        
        """
        if self.empty():
            raise QEmptyError()
        
        try:
            self._buf.remove(value)
        except ValueError:
            raise ValueError("Очередь не имеет элемент с указаным значением")
        
        
    
    def aslist(self)->list[T]:
        """
        Возвращает список всех элементов очереди.

        return:
        (list[T]): Список элементов очереди.
        """
        return list(self._buf)
    
    def __iter__(self)->Generator[T,None,None]:
        """
        Генератор, который позволяет итерировать по элементам очереди (магический метод).

        return:
        (Generator[T,None,None]): Генератор, который возвращает элементы очереди один за другим.
        """
        for el in self._buf:
            yield el
            
    def __repr__(self) -> str:
        """
        Представляет очередь в виде строки для печати (магический метод).

        return:
        (str): Строковое представление очереди.
        """
        return f"CDQueue{str(self._buf)[5:]}"
        
    def __del__(self)->None:
        """
        Очищает очередь перед уничтожением.
        """
        self.clear()

if __name__ == "__main__":
    a = CDQueue[int](10)
    a.push(1)
    a.push(2)
    a.remove(2)
    
    print(a)
    print(a.front())
    print(a.back())
    # a.pop()
    # a.pop()
    # a.push(5)
    # a.push(6)
    # print(a)
    # a.resize(8)
    # print(a)
    # a.insert(2,9)
    # print(a)
    

    
    



    
    
    
    
    
    
    
        