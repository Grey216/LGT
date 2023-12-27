"""
Модуль caqueue, реализует структуру данных циклической очереди на основе массива (Array).

Класса CAQueue, представляет циклическую очередь.
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

from typing import Optional,TypeVar,Generic,Generator,Any
import sys
try:
    from qexception import QFullError,QEmptyError
except ImportError:
    from .qexception import QFullError,QEmptyError
T = TypeVar("T") # Обобщенный тип данных

class BArray(Generic[T]):
    """
    Класс BArray представляет собой массив фиксированного размера.

    Attr:
    _array (List[Optional[T]]): Массив значений

    Methods:
    __init__(size: int) -> None: Инициализация массива заданного размера
    __getitem__(index: int) -> Optional[T]: Получение элемента по индексу
    __setitem__(index: int, value: T) -> None: Установка значения элемента по индексу
    clear() -> None: Очистка массива, устанавливает все элементы в None
    __len__() -> int: Размер массива
    __del__() -> None: Метод удаления объекта, вызывает метод clear()
    """
    def __init__(self,size:int) -> None:
        """
        Инициализирует массива
        
        param:
        size (int): Размер массива
        """
        self._array:list[Optional[T]] = [None]*size
    
    def __getitem__(self, index: int) -> Optional[T]:
        """Получение элемента по индексу."""
        return self._array[index]

    def __setitem__(self, index: int, value: T) -> None:
        """Установка значения элемента по индексу."""
        self._array[index] = value
    
    def clear(self) -> None:
        """Очистка массива, устанавливает все элементы в None."""
        self._array = [None] * len(self._array)

    def __del__(self) -> None:
        """Метод удаления объекта, вызывает метод clear()."""
        self.clear()

class CAQueue(Generic[T]):
    
    """
    Реализация циклической структуры данных FIFO на основе массива(Array)
    
    attr:
    _count (int): количество элементов в очереди
    _max_size (int): максимальное количество элементов в очереди 
    _front (Optional[Node[T]]): Индекс первого элемента в очереди
    _back (Optional[Node[T]]): Индекс последнего элемента в очереди
    _buf (BArray[T]): Контейнер очереди
    
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
        self._count: int = 0
        self._max_size: int = max_size
        self._buf:BArray[T] = BArray(max_size)        
        self._front: Optional[int] = None
        self._back: Optional[int] = None
        
    def empty(self)->bool:
        """
        Проверяет, пуста ли очередь.

        return:
        (bool): True, если очередь пуста, иначе False.
        """
        return self._count==0
    
    def is_full(self)->bool:
        """
        Проверяет, полная ли очередь
        
        return:
        (bool): True, если очередь полная, иначе False.
        """
        return self._count==self._max_size
    
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
        return self._buf[self._front]
    
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
        return self._buf[self._back]
    
    def push(self,value:T,replace:bool = False)->None:
        """
        Добавляет элемент в конец очереди. 
        1)Если очередь переполнена и replace= False, то поднимаем исключение. 
        2)Если очередь переполнена и replace= True, то удаляем первый элемент очереди и вставляем новый. 

        raise:
        (QFullError): Если очередь заполнена.
        
        param:
        value (T): Элемент для добавления в очередь.
        replace (bool): Указывает на то, что нужно ли удалять первый элемент при переполнении или поднять исключение
        """
        if self.is_full():
            if replace:
                self._buf[self._front] = None
                self._front = (self._front+1)%self._max_size 
                self._count-=1
            else: 
                raise QFullError()
        
        if self.empty():
            self._front,self._back = 0,0
            self._buf[self._front] = value
        else:
            self._back = (self._back+1)%self._max_size
            self._buf[self._back] = value
        self._count+=1 
        
    def pop(self)->T:
        """
        Удаляет и возвращает первый элемент очереди.

        raise:
        (QEmptyError): Если очередь пуста.

        return:
        value (T) : Удаленный первый элемент очереди.
        """
        if self.empty():
            raise QEmptyError()
        
        value:T = self._buf[self._front]
        self._buf[self._front] = None
        self._count-=1
        if self._count == 0:
            self._front,self._back = None,None
        else:
            self._front = (self._front+1)%self._max_size            
        
        return value
    
    def length(self)->int:
        """
        Возвращает количество элементов в очереди.

        return:
        (int): Количество элементов в очереди.
        """
        return self._count
    
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
        
        new_buf:BArray[T] = BArray[T](new_size)
        offset = max(0,self._count-new_size) # Если новый размер меньше, то смещаем 
        cur = (self._front + offset)%self._max_size
        
        for i in range(min(self._count,new_size)):
            new_buf[i] =self._buf[cur]
            cur = (cur+1)%self._max_size
        
        # Обновляем данные
        self._count = min(self._count,new_size)
        self._max_size=new_size
        self._buf = new_buf
        self._front = 0
        self._back = self._count-1
        
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
        
        if self.empty():
            self.push(value)
        else:
            #Нормализуем индекс
            index = self._count if index>self._count else 0 if index<0 else index 
            norm_index = (self._front+index)% self._max_size  
            
            
            ### ОПТИМИЗАЦИЯ (ВЫБОР СТОРОНЫ ДЛЯ СДВИГА) ###
            #Сотрим куда ближе всего сдвигать
            if abs(self._front-norm_index)<abs(self._back -norm_index):
                #Делаем сдвиг влево
                self._front = (self._front-1)% self._max_size
                cur = self._front
                next = (cur+1)%self._max_size
                norm_index = (norm_index-1)%self._max_size # Из-за логики сдвига элементов вправо 
                while cur != norm_index:
                    self._buf[cur] = self._buf[next]
                    cur = next
                    next = (next+1)%self._max_size                    
            else:  
                #Делаем сдвиг вправо     
                self._back = (self._back+1)% self._max_size   
                rcur = self._back
                rnext = (rcur-1)%self._max_size
                while rcur != norm_index:
                    self._buf[rcur] = self._buf[rnext]
                    rcur = rnext
                    rnext = (rcur-1)%self._max_size
            ##################################################
                    
            self._buf[norm_index] = value
            self._count+=1
    
    
    
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
        
        index:int = None
        
        for i, el in enumerate(self):
            if el == value:
                index = (self._front+i)%self._max_size
                break
        
        if index is None:
            raise ValueError("Очередь не имеет элемент с указаным значением")
        
        cur = index
        
        
        ### ОПТИМИЗАЦИЯ (ВЫБОР СТОРОНЫ ДЛЯ СДВИГА) ###
        # Сотрим куда ближе всего сдвигать
        if abs(self._front-index)<abs(self._back -index):
            # Cдвиг влево
            while cur!=self._front:
                self._buf[cur] = self._buf[(cur-1)%self._max_size]
                cur = (cur-1)%self._max_size
            
            self._front = (self._front+1)% self._max_size
        else:
            # Сдвиг вправо
            while cur!=self._back:
                self._buf[cur] = self._buf[(cur+1)%self._max_size]
                cur = (cur+1)%self._max_size     
                       
            self._back = (self._back-1)% self._max_size
            
        ##################################################
        self._count-=1 
        self._buf[cur] = None
        
        
    
    def __len__(self)->int:
        """
        Возвращает количество элементов в очереди (магический метод).

        return:
        (int): Количество элементов в очереди.
        """
        return self.length()
    
    def __iter__(self)->Generator[T,None,None]:
        """
        Генератор, который позволяет итерировать по элементам очереди (магический метод).

        return:
        (Generator[T,None,None]): Генератор, который возвращает элементы очереди один за другим.
        """
        cur = self._front
        for _ in range(self._count):
            yield self._buf[cur]
            cur = (cur+1)%self._max_size      
        
    def aslist(self)->list[T]:
        """
        Возвращает список всех элементов очереди.

        return:
        (list[T]): Список элементов очереди.
        """
        
        return [i for i in self]
    
    def __repr__(self) -> str:
        """
        Представляет очередь в виде строки для печати (магический метод).

        return:
        (str): Строковое представление очереди.
        """
        return f"CAQueue({self.aslist()}, max_size={self._max_size})"
    
    
    def clear(self)->None:
        """
        Очищает очередь, удаляя все элементы.
        
        return:
        (None)
        """
        self._count = 0
        self._back = None
        self._front = None
        self._buf.clear()
    
    def __del__(self)->None:
        """
        Очищает очередь перед уничтожением.
        """
        self.clear()
    


if __name__ == "__main__":
    a = CAQueue[int](5)
    a.push(1)
    a.remove(1)
    print(a)
    a.push(4)
    print(a)
    a.pop()
    print(a.front())
    print(a.back())

    # for i in range(6):
    #     a.push(i)
    # a.pop()
    # a.pop()
    # print(a)
    # a.insert(0,100)
    # print(a)
    # a.remove(100)
    # print(a)
   
    # a.push(3)
    # a.push(4)
    # a.pop()
    # a.pop()
    # a.push(5)
    # a.push(6)
    # print(a)
    # a.resize(8)
    # print(a)
    # a.insert(2,9)
    # print(a)


    