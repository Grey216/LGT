"""
Пакет для работы с цикличсечкими очередями.

Пакет содержит следующие модули и классы:
- CDQueue: Реализация циклической очереди на основе deque из модуля collections.
- CAQueue: Реализация циклической очереди на основе массива.
- CLLQueue: Реализация циклической очереди на основе связанного списка (не проинициализированная связь).
- QEmptyError: Исключение, возникающее при попытке выполнить операции с пустой очередью.
- QFullError: Исключение, возникающее при попытке вставки элемента в заполненную очередь.

"""


from .cdqueue import CDQueue
from .caqueue import CAQueue
from .qexception import QEmptyError, QFullError
from .cllqueue import CLLQueue




__all__ = ['CDQueue', 'CAQueue', 'QEmptyError', 'QFullError','CLLQueue']
