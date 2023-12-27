"""
Модуль для тестирования различных реализаций циклической очереди.

Этот модуль содержит классы тестов для проверки функционала различных реализаций циклической очереди, а так же их время на тестрирование:
TestCAQueue, TestCLLQueue, TestCDQueue.
"""
import sys

import setup
setup.setup() # доступ к родительскому каталогу


import unittest
import abc
import timeit
from typing import TypeVar

from cqueue import CAQueue,CLLQueue,CDQueue
from cqueue import QFullError,QEmptyError

T = TypeVar("T") # Обобщенный тип данных

class AbstractTestCQueue(abc.ABC):
    """
    Абстрактный класс для тестирования функционала очереди. 
    
    attr:
    queue (CAQueue|CDQueue|CLLQueue): Экзампляр класса очереди 
    
    method:
    setUp(): Установка начальных условий (абстрактный метод)
    tearDown(): Установка конечных условий (асбтрактный метод)
    
    test_empty(): Проверка метода empty()
    test_length(): Проверка метода length()
    test_clear(): Проверка метода clear()
    test_front_back(): Проверка методов front() и back()
    test_pop(): проверка метода pop()
    test_push(): Проверка метода push()
    test_push_replace(): Проверка метода push() с установкой второго параметра replace=True
    test_empty_error(): Проверка вызова исключения QEmptyError при попытке извлечения элемента из пустой очереди
    test_full_error(): Проверка вызова QFullError при попытке добавления элемента в полную очередь
    test_remove(): Проверка метода remove()
    test_insert(): Проверка метода insert()
    test_resize(): Проверка метода resize()
    
    test_stress_pop(): Проверка добавления большого количества элементов в очередь
    test_stress_push(): Проверка добавление большого количества элементов в очередь и их последовательное удаление
    test_stress_push_cycle(): Проверка цикличности очереди
    test_stress_push_replace_cycle(): Проверка добавления большого количества элементов в очередь c raplace=True
    test_stress_remove(): Проверка удаления элементов по значению из большой очереди
    test_stress_resize(): Проверка добавления элементов в большую очередь
    test_stress_insert(): Проверка изменения размерности большой очереди
    
    test_stress_push_another_class(): Проверка добавления большого количества Экземпляров класса в очередь
    """   
    
    @abc.abstractmethod
    def setUp(self):
        """
        Установка начальных условий перед каждым тестом.
        """
        self.queue: CAQueue[T]|CDQueue[T]|CLLQueue[T]
        self.start_time:float
    
    @abc.abstractmethod
    def tearDown(self):
        """
        Установка конечных условий после каждого теста.
        """
        
    # Методы тестрирования функционала очереди 
    
    def test_empty(self):
        """
        Проверка метода empty().
        """
        self.assertTrue(self.queue.empty())
        self.queue.push(1)
        self.assertFalse(self.queue.empty())

    def test_length(self):
        """
        Проверка метода length().
        """
        self.assertEqual(self.queue.length(), 0)
        self.queue.push(1)
        self.assertEqual(self.queue.length(), 1)

    def test_clear(self):
        """
        Проверка метода clear().
        """
        self.queue.push(1)
        self.queue.push(2)
        self.queue.push(3)
        self.queue.clear()
        self.assertEqual(self.queue.length(), 0)
        self.assertTrue(self.queue.empty())

    def test_front_back(self):
        """
        Проверка методов front() и back().
        """        
        self.queue.push(1)
        self.queue.push(2)
        self.queue.push(3)
        self.assertEqual(self.queue.front(), 1)
        self.assertEqual(self.queue.back(), 3)

    def test_pop(self):
        """
        Проверка метода pop().
        """
        self.queue.push(1)
        self.queue.push(2)
        self.queue.push(3)
        popped = self.queue.pop()
        self.assertEqual(popped, 1)
        self.assertEqual(self.queue.length(), 2)
        self.assertEqual(self.queue.front(), 2)

    def test_push(self):
        """
        Проверка метода push()
        """
        self.queue.push(1)
        self.queue.push(2)
        self.queue.push(3)
        self.assertEqual(self.queue.length(), 3)
        self.assertEqual(self.queue.back(), 3)
    
    def test_push_replace(self):
        """
        Проверка метода push() с установкой второго параметра replac=True
        """    
        self.queue.push(1)
        self.queue.push(2)
        self.queue.push(3)
        self.assertEqual(self.queue.length(), 3)
        self.queue.push(4,replace=True)  
        self.assertEqual(self.queue.length(), 3)
        self.assertEqual(self.queue.front(), 2)
        self.assertEqual(self.queue.back(), 4)
        
    def test_empty_error(self):
        """
        Проверка вызова исключения QEmptyError при попытке извлечения элемента из пустой очереди
        """
        with self.assertRaises(QEmptyError):
            self.queue.pop()

    def test_full_error(self):
        """
        Проверка вызова QFullError при попытке добавления элемента в полную очередь
        """
        while not self.queue.is_full():
            self.queue.push(1)
        with self.assertRaises(QFullError):
            self.queue.push(1)
    
    def test_insert(self):
        """
        Проверка метода insert
        """
        self.queue.push(1)
        self.queue.push(3)
        self.queue.pop()
        self.queue.push(4)
        self.queue.insert(1, 2)
        self.assertEqual(self.queue.aslist(), [3, 2,4])
        self.queue.pop()
        self.queue.pop()
        self.queue.insert(-3, 6)
        self.queue.insert(231,7)
        self.assertEqual(self.queue.aslist(), [6, 4,7])
        self.assertEqual(self.queue.front(), 6)
        self.assertEqual(self.queue.back(), 7)
        self.queue.pop()
        self.queue.insert(1, 2)
        self.assertEqual(self.queue.aslist(), [4,2,7])
        self.assertEqual(self.queue.front(), 4)
        self.assertEqual(self.queue.back(), 7)
        

    def test_remove(self):
        """
        Проверка метода remove()
        """
        self.queue.push(1)
        self.queue.push(2)
        self.queue.push(3)
        self.queue.remove(2)
        self.assertEqual(self.queue.aslist(), [1, 3])
        self.queue.remove(3)
        self.assertEqual(self.queue.aslist(), [1])
        self.assertEqual(self.queue.front(), 1)
        self.assertEqual(self.queue.back(), 1)
        self.queue.push(4)
        self.queue.push(5)
        self.assertEqual(self.queue.aslist(), [1,4,5])
        self.queue.remove(5)
        self.assertEqual(self.queue.aslist(), [1,4])
        self.assertEqual(self.queue.front(), 1)
        self.assertEqual(self.queue.back(), 4)
        self.queue.remove(1)
        self.queue.remove(4)
        self.assertEqual(self.queue.aslist(), [])

    def test_resize(self):
        """
        Проверка метода resize()
        """
        self.queue.push(1)
        self.queue.push(2)
        self.queue.push(3)
        self.queue.resize(10)
        self.assertEqual(self.queue.aslist(), [1, 2,3])
        self.queue.push(4)
        self.queue.push(5)
        self.queue.push(6)
        self.queue.push(7)
        self.queue.resize(2)
        self.assertEqual(self.queue.aslist(), [6,7])
        self.assertEqual(self.queue.front(), 6)
        self.assertEqual(self.queue.back(), 7)
        
    
    
    # Нагруженные тесты
    def test_stress_push(self):
        """
        Проверка добавления большого количества элементов в очередь
        """
        size = 1000000
        self.queue = self.queue.__class__[int](size)   
        for i in range(1,size+1):
            self.queue.push(i)
        self.assertEqual(self.queue.length(), size)
        self.assertEqual(self.queue.front(), 1)
        self.assertEqual(self.queue.back(), size)

    def test_stress_pop(self):
        """
        Добавление большого количества элементов в очередь и их последовательное удаление
        """
        size = 1000000
        self.queue = self.queue.__class__[int](size)   
        for i in range(1,size+1):
            self.queue.push(i)
        start = timeit.default_timer()
        for i in range(1,size+1):
            popped = self.queue.pop()
            self.assertEqual(popped, i)
        print(f"{self.id()}(only pop()): { round(timeit.default_timer() - start,3)}s")
        self.assertEqual(self.queue.length(), 0)
        self.assertTrue(self.queue.empty())

    def test_stress_push_cycle(self):
        """
        Проверка цикличности очереди
        """
        size = 1000000
        self.queue = self.queue.__class__[int](size)   
        for i in range(size):
            self.queue.push(i)
        for i in range(size):
            popped = self.queue.pop()
            self.assertEqual(popped, i)
        for i in range(size, 2*size):
            self.queue.push(i)
        for i in range(size, 2*size):
            popped = self.queue.pop()
            self.assertEqual(popped, i)
    
    def test_stress_push_replace_cycle(self):
        """
        Проверка добавления большого количества элементов в очередь c raplace=True
        """
        size = 100000
        self.queue = self.queue.__class__[int](size)   
        for i in range(1,size*2+1):
            self.queue.push(i,replace=True)
        self.assertEqual(self.queue.back(),200000)
        
    
    def test_stress_push_another_class(self):    
        """
        Проверка добавления большого количества Экземпляров класса в очередь
        """
        size = 1000000
        class TestAnotherClass:
            def __init__(self,el:int) -> None:
                self.el = el
                
        self.queue = self.queue.__class__[TestAnotherClass](size)   
        for i in range(1,size+1):
            self.queue.push(TestAnotherClass(i))
        self.assertEqual(self.queue.length(), size)
        self.assertEqual(self.queue.front().el, 1)
        self.assertEqual(self.queue.back().el, size)
        
    
    def test_stress_insert(self):
        """
        Проверка добавления элементов в большую очередь 
        """
        size = 1000000
        self.queue = self.queue.__class__[int](size)   
        for i in range(size-21):
            self.queue.push(i)
        
        start = timeit.default_timer()
        for i in range(21):
            self.queue.insert(i*(size//20), 9999)
        print(f"{self.id()}(only insert()): { round(timeit.default_timer() - start,3)}s")
        self.assertEqual(self.queue.front(), 9999)
        self.assertEqual(self.queue.back(), 9999)

    def test_stress_remove(self):
        """
        Проверка удаления элементов по значению из большой очереди
        """
        size = 1000000
        self.queue = self.queue.__class__[int](size)   
        for i in range(size):
            self.queue.push(i)        
        start = timeit.default_timer()
        for i in range(1,22):
            self.queue.remove(i+2000)
        print(f"{self.id()}(only remove()): { round(timeit.default_timer() - start,3)}s")
  
        self.assertEqual(self.queue.front(), 0)
        self.assertEqual(self.queue.back(), 999999)

    def test_stress_resize(self):
        """
        Проверка изменения размерности большой очереди
        """
        size = 1000000
        self.queue = self.queue.__class__[int](size)   
        for i in range(size):
            self.queue.push(i)
            
        start = timeit.default_timer()
        self.queue.resize(200000)
        self.assertEqual(self.queue.length(), 200000)
        self.queue.resize(20000)
        self.assertEqual(self.queue.length(), 20000)
        self.queue.resize(2000)
        self.assertEqual(self.queue.length(), 2000)
        self.queue.resize(200)
        self.assertEqual(self.queue.length(), 200)
        print(f"{self.id()}(only resize()): { round(timeit.default_timer() - start,3)}s")

        

        


class TestCAQueue(unittest.TestCase, AbstractTestCQueue):
    """
    Класс для тестирования функционала CAQueue.
    """
    def setUp(self):
        """
        Установка начальных условий перед каждым тестом CAQueue.
        """
        self.startTime = timeit.default_timer()
        self.queue = CAQueue[int](3)
        
    
    def tearDown(self):
        """
        Установка конечных условий после каждого теста CAQueue.
        """
        print(f"{self.id()}: { round(timeit.default_timer() - self.startTime,3)}s")



class TestCLLQueue(unittest.TestCase, AbstractTestCQueue):
    """
    Класс для тестирования функционала CLLQueue.
    """
    def setUp(self):
        """
        Установка начальных условий перед каждым тестом CLLQueue.
        """
        self.startTime = timeit.default_timer()
        self.queue = CLLQueue[int](3)
        
    
    def tearDown(self):
        """
        Установка конечных условий после каждого теста CLLQueue.
        """
        print(f"{self.id()}: { round(timeit.default_timer() - self.startTime,3)}s")
               

class TestCDQueue(unittest.TestCase, AbstractTestCQueue):
    """
    Класс для тестирования функционала CDQueue.
    """
    def setUp(self):
        """
        Установка начальных условий перед каждым тестом CDQueue.
        """
        self.startTime = timeit.default_timer()
        self.queue = CDQueue[int](3)
        
    
    def tearDown(self):
        """
        Установка конечных условий после каждого теста CDQueue.
        """
        print(f"{self.id()}: { round(timeit.default_timer() - self.startTime,3)}s")
        
if __name__ == '__main__':

   
    for TestQueue in [TestCLLQueue,TestCAQueue,TestCDQueue]:
        print(f"Running test {TestQueue.__name__}")
        suite = unittest.TestLoader().loadTestsFromTestCase(TestQueue)
        res = unittest.TextTestRunner(verbosity=0).run(suite)
        print()
    
    