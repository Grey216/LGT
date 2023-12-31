# third_task (Предложить алгоритм, который быстрее всего (по процессорным тикам) отсортирует данный ей массив чисел)

## Пояснение
В решении данного задания использовался ресурс, от туда брал учтонения и мне был важен псевдокод: [Ссылка](https://neerc.ifmo.ru/wiki/index.php?title=%D0%A1%D0%BE%D1%80%D1%82%D0%B8%D1%80%D0%BE%D0%B2%D0%BA%D0%B8). 

Так как нужно было отсортировать массив чисел, числа будут храниться в numpy массивах

При выборе алгоритма сортировки, С УЧЕТОМ ЗАДАНИЯ, нужно учесть несколько факторов:
1) Нам неважна устойчивость 
2) Нам не важна память выделяемая для сортировки(наверно грубо сказано, но в задании нету уточнения)
3) Нам нужен алгоритм с наилучшим временем для массивов любой размерности
4) Нам нужен алгоритм с наилучшим временем для таких массивов как: не отсортированные, полуотсортированные и отсортированные
5) Числа могут быть как вещественные так и целые 

Исходя из этого некоторые сортировки сразу отпадают. 

Для более быстрой работы нам нунжо рассматривать встроенные сортировки, а так же использование jit-компилятора, а иначе любамая реализация сортировки в любом случае будет медленее, чем встроенаа sorted() из-за, того что она реализована и оптимизирована на языке Cи.

(Про использоваие доп. пакетов ограничений не было. Так же можно расмотреть сортировку с помощью распрараллеливания на cpu при помощи библиотеки taichi, так есть алгоритмы которые предлагает компания NVidia для сортировки)

Данная реализация сравнивает нужные нам сортировки с УЧЕТОМ ЗАЛАДАНИЯ. 

В документации NumPy написано, что по умолчанию используется 'quicksort'. ‘stable’ and ‘mergesort’ используют 'timsort' или 'radix sort' , и, как правило, фактическая реализация будет зависеть от типа данных. По этому мы бдуем использовать 'stable'.

Для тестов мы использовали такие сортировки как:
1) ListSort - Метод списка sort() (он использует сортировку 'timsort')
2) NpQuickSort- Метод np.array sort() с ключем kind='quicksort'
3) NpStableSort - Метод np.array sort() с ключем kind='stable'
4) QuickSort - Реализованный алгоритм сортировки 'quicksort' с использованием jit-компилятора



По резльльтам видно, что (main.py):
1) Реализованный алгоритм сортировки QuickSort показывает резултат лучше, чем ListSort только на "Не отсортированных данных" и то только на массивах размерность > 1_000_000
2) Для неотсортированных данных лучше всех подходит NpQuickSort-
3) Для отсортированных данных лучше всех подходит NpStableSort
4) Для полуотсортированных данных лучше всех подходит NpStableSort
5) ListSort хорошо себя показывает, только на маллых размерах


## Вывод:
Наилучшим вариантом для сортировки данных будет сортировка NpStableSort, даже не смотря на то, что NpQuickSort хорошо сортирует неотсортированные данныне, но у негоесть нюанс: если колличество рекурсий слишком велико, то он переходит на другой алгоритм сортировки ( сортировка кучей) и при слишком огромных данных время сортировки будет больше чем у NpStableSort. 
