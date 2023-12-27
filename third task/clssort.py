import numpy as np
import timeit


from numba import njit

from typing import Iterable
from abc import ABC,abstractmethod
import multiprocessing




class AbcSort(ABC):
    """
    Абстрактный класс для вывода времени сортировки. 
    
    attr:
    _ls (np.ndarray[int|float]): Массив для сортировки.
    
    method:
    _sort()-None: Абстрактный метод для сортировки массива.
    timesort() -> float: Возвращает время выполнения сортировки.
    getarray() -> np.ndarray[int|float]: Возвращает массив.
    """
    
    def __init__(self, ls: np.ndarray[int | float]) -> None:
        """
        Инициализация массива
        
        param:
        _ls (np.ndarray[int | float]): Массив 
        """
        self._ls: np.ndarray[int | float] = ls
    
    @abstractmethod
    def _sort(self):
        "Абстрактный метод сортирвоки."
        pass
    
    def timesort(self) -> float:
        """
        Сортирует массив и вывод время сортирвоки.
        
        return:
        (float): Время сортировки
        """
        return timeit.timeit(self._sort, number=1)
        
    def getarray(self) -> np.ndarray[int | float]:
        """
        Возращает массив.
        
        return:
        (np.ndarray[int | float]): Массив 
        """
        return self._ls
        
class ListSort(AbcSort):
    """
    Класс для сортировки массива с использованием метода sort().
    """
    
    def __init__(self,ls:np.ndarray[int|float]) -> None:
        self._ls:list[int|float] = list(ls)
    
    def _sort(self):
        self._ls.sort()

        
class NpQuickSort(AbcSort):
    """
    Класс для сортировки массива с использованием быстрой сортировки NumPy.
    """    
    def _sort(self):
        self._ls.sort(kind='quicksort')
        
        
class NpStableSort(AbcSort):
    """
    Класс для сортировки массива с использованием  стабильной сортировки NumPy.
    """  
    def _sort(self):
        self._ls.sort(kind='stable')

class QuickSort(AbcSort):
    """Класс для сортировки массива с использованием быстрой сортировки"""
    
    def _sort(self):
        @njit
        def partition(arr:np.ndarray[int|float],l:int,r:int):
            pivot:int|float = arr[(l+r)//2]
            i = l - 1
            j = r + 1
            while True:
                i += 1
                while arr[i] < pivot:
                    i += 1

                j -= 1
                while arr[j] > pivot:
                    j -= 1

                if i >= j:
                    return j

                arr[i], arr[j] = arr[j], arr[i]
        
        @njit
        def qsort(arr:np.ndarray[int|float],l:int,r:int):
            if l<r:
                pivot_index: int = partition(arr,l,r)
                qsort(arr,l,pivot_index)
                qsort(arr,pivot_index+1,r)
                
        qsort(self._ls,0,len(self._ls)-1)
            


    
    

    
    
        

    




    
    
    
    


        