"""
Модуль cllqueue, реализует структуру данных циклической очереди на основе связного списка (Linked List).
Данный связный список заранее не проинициализирован!

Класса CLLQueue, представляет циклическую очередь.
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
try:
    from qexception import QFullError,QEmptyError
except ImportError:
    from .qexception import QFullError,QEmptyError

T = TypeVar("T") # Обобщенный тип данных
  

@dataclass
class Node(Generic[T]):
    """
    Узел для использования в очереди (односвязный список)
    
    attr:
    value (T): Значение элемента узла
    next (Optional[Node[T]): Ссылка на следующий узел (Node/None)    
    """
    value: T
    next: Optional['Node[T]'] = field(default=None,init=False,repr=False)
    

class CLLQueue(Generic[T]): 
    
    """
    Реализация циклической структуры данных FIFO на основе связного списка (Linked List)
    
    Связный список заранее не проинициализирован. 
    Инициалищация Node происходит по мере добавления элемента в очередь. 
    
    attr:
    _count (int): количество элементов в очереди
    _max_size (int): максимальное количество элементов в очереди 
    _back (Optional[Node[T]]): Ссылка на последний элемент в очереди
    
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
        self._count:int = 0
        self._max_size:int = max_size
        self._back: Optional[Node[T]] = None
    
        
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
    
    def length(self)->int:
        """
        Возвращает количество элементов в очереди.

        return:
        (int): Количество элементов в очереди.
        """
        return self._count
    
    def clear(self)->None:
        """
        Очищает очередь, удаляя все элементы.
        
        return:
        (None)
        """
        self._count = 0
        self._back = None

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
        return self._back.next.value
    
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
        return self._back.value
    
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
        
        front = self._back.next # Это начало 
        value:T = front.value      
        self._count-=1
        
        if self._count==0:
            self._back = None
        else:
            self._back.next = front.next  # Конец указывает на начало
        return value
        
    
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
        if self.is_full():
            if replace:
                front = self._back.next
                self._back.next = front.next                             
                self._count -=1            
            else: 
                raise QFullError()
            
        newNode:Node[T] = Node[T](value)
        if self.empty():
            self._back = newNode
            self._back.next = self._back
        else: 
            front = self._back.next 
            self._back.next = newNode
            self._back = self._back.next
            self._back.next = front
        self._count+=1 
        
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
        
        if self._max_size <=new_size:
            self._max_size = new_size
        else:
            # Удаляем старые значения 
            offset = max(0,self._count - new_size)
            front = self._back.next
            for i in range(offset):
                front = front.next
            self._count = min(self._count,new_size)
            self._max_size = new_size
            self._back.next = front
                
            
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
            index = self._count if index>self._count else 0 if index<0 else index
            newNode:Node[T] = Node[T](value)
            if index == 0:
                front = self._back.next
                self._back.next = newNode
                newNode.next = front
            elif index == self._count:
                front = self._back.next
                self._back.next = newNode
                self._back = self._back.next
                self._back.next = front
            else:
                cur = self._back
                for i in range(index):
                   cur = cur.next 
                newNode.next = cur.next
                cur.next = newNode
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
        
        flag:bool = False
        prevNode:Node[T] = self._back
        nextNode:Node[T] = self._back.next
        
        for el in self:
            if el == value:
                flag = True
                break
            prevNode = nextNode
            nextNode = nextNode.next        
        
        if not flag:
            raise ValueError("Очередь не имеет элемент с указаным значением")
        
        prevNode.next = nextNode.next
        if self._back is nextNode:
            self._back = prevNode
        self._count-=1
               
    
    def aslist(self)->list[T]:
        """
        Возвращает список всех элементов очереди.

        return:
        (list[T]): Список элементов очереди.
        """
        return [i for i in self]
        
        
    def __iter__(self)->Generator[T,None,None]:
        """
        Генератор, который позволяет итерировать по элементам очереди (магический метод).

        return:
        (Generator[T,None,None]): Генератор, который возвращает элементы очереди один за другим.
        """
        if not self.empty():
            current = self._back.next
            while True:
                yield current.value
                current = current.next
                if current is self._back.next: # Если указывают на одну и ту же ячейку памяти
                    break

    
   
    def __repr__(self) -> str:
        """
        Представляет очередь в виде строки для печати (магический метод).

        return:
        (str): Строковое представление очереди.
        """
        return f"CLLQueue({self.aslist()}, max_size={self._max_size})"
    
    def __del__(self)->None:
        """
        Очищает очередь перед уничтожением.
        """
        self.clear()





if __name__ == "__main__":
    from random import randint
    

    a = CLLQueue[int](6)
    a.push(1)
    a.push(2)
    a.push(3)
    a.remove(3)
    
    print(a)
    print(a.front())
    print(a.back())


    # print(a.aslist())
    # try:
    #     a.push(5)
    # except QFullError as er:
    #     print(er)
    # print(a)
    # a.push(5,True)



    

