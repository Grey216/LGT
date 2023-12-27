"""
Скрипт first_task сравнивает две реализации(фукции) определения четности целого числа 

"""


import timeit

def isEven_mod(value:int)->bool:  
    """
    Проверяет четность целого числа с помощью операции по модулю
    
    :param 
    value(int): Входное значение для проверки 
    
    :return 
    (bool): Возращает true если число четное, а иначе false
    """   
    return value % 2 == 0

def isEven_bitwise(value:int)->bool:  
    """
    Проверяет четность целого числа с помощью побитовой опреации И
    
    :param 
    value(int): Входное значение для проверки 
    
    :return 
    (bool): Возращает true если число четное, а иначе false
    """   
    return value & 1 == 0


if __name__ == "__main__":
    num = 50_000_000 # Кол-во итераций
    time_1 = timeit.timeit(lambda : isEven_mod(123456789),number=num)
    time_2 = timeit.timeit(lambda : isEven_bitwise(123456789),number=num)
    print(time_1)
    print(time_2)