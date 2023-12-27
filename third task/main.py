from clssort import AbcSort,ListSort,NpQuickSort,NpStableSort,QuickSort
import numpy as np


def sorting_time(sort_classes:list[AbcSort],data:list[int],sorted_flag:int = 0)->dict:
    """
    Функция сортирует массивы классов различной размерностью.
    
    param:
    sort_classes(list[AbcSort]): Список классов сортировок
    data (list[int]): Список значений размерности массива
    sorted_flag: Указывает как отсортирован массив (0-Неотсортирован, 1-Отсортирован, 2-Полуотсортирован)
    
    return:
    best_res (dict[int,list[tuple[str,float]]]): Возрщает словарь в котором в порядке убывания отоброжены лучшие реализации для конктретной размерности 
    """
    best_res:dict[int,list[tuple[str,float]]] = {}
    for size in data:
        arr:np.ndarray[int|float] = np.random.randint(0,1_000_000,size)
        if sorted_flag==1:
            arr.sort()
        elif sorted_flag==2:
            arr[:len(arr)//2] = np.sort(arr[:len(arr)//2])        
        for sort_class in sort_classes:
            obj_class:AbcSort = sort_class(arr.copy())
            time = obj_class.timesort()
            best_res.setdefault(size,[]).append((sort_class.__name__,time))
        best_res[size].sort(key=lambda x:x[1])
    
    return best_res
        
            
def print_best_res(best_res:dict[int,list[tuple[str,float]]]):
    """ Фнкция для вывода результатов сортировки.     
        Результаты сортировки отображаются в порядке от наилучшего времени к наихудшему
        
    """
    for size,values in best_res.items():
        print(f"Размер массива: {size}")
        for index,(class_name,time) in enumerate(values):
            print(f"{index}) {class_name}: {time:.6f} s")
        print()


if __name__ == "__main__":
    
    data_sizes = [10, 100, 1000, 10_000,100_000,1_000_000,10_000_000]
    sorting_classes = [ListSort,  NpQuickSort, NpStableSort,QuickSort]
    
    print("***Не отсортированный масиив***")
    best_res = sorting_time(sorting_classes,data_sizes)    
    print_best_res(best_res)
    
    print("***Отсортированный масиив***")
    best_res = sorting_time(sorting_classes,data_sizes,1)    
    print_best_res(best_res)
    
    print("***Полуотсортированный масиив***")
    best_res = sorting_time(sorting_classes,data_sizes,1)    
    print_best_res(best_res)