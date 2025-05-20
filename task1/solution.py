import inspect
from functools import wraps
from typing import Callable, ParamSpec, TypeVar

T = TypeVar("T")
P = ParamSpec("P")


def strict(func: Callable[P, T]) -> Callable[P, T]:
    """
    Проверка типов аргументов функции согласно аннотациям.

    :param func: Функция, к которой применяется декоратор
    :return: Обёрнутая функция с проверкой типов
    :raises TypeError: Если тип аргумента не совпадает с аннотацией

    Пример:
        @strict
        def greet(name: str) -> str:
            return f"Hello, {name}"

        greet("Alice")  # Ок
        greet(123)      # Вызывает TypeError
    """
    signature = inspect.signature(func)

    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        passed_values = signature.bind(*args, **kwargs).arguments

        for parameter_name, parameter_value in passed_values.items():
            parameter = signature.parameters[parameter_name]
            annotation = parameter.annotation

            # Пропускаем проверку, если нет аннотации типа
            if annotation is inspect.Parameter.empty:
                continue

            if type(parameter_value) != annotation:
                raise TypeError

        return func(*args, **kwargs)

    return wrapper
