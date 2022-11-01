from __future__ import annotations
import click
import random
import functools
from typing import Set
from typing import Callable
from typing import Optional
from typing import Generator
from typing import Tuple
from typing import Any


class Pizza:
    """Родительский класс для пиццы """

    def __init__(self, size: str = 'L') -> None:
        """ Инициализирует экземпляр класса."""
        self._size = size
        self.recipe: Set[str] = set()

    def __iter__(self) -> Generator[Tuple[str, Set[str]], None, None]:
        """Переопределяет dict()"""
        yield from {self.__class__.__name__: self.recipe}.items()

    def __eq__(self, other: object) -> bool:
        """
        Позволяет сравнить два экземпляра класса.
        Пиццы равны, если у них совпадают рецепты и размер.
        """
        if not isinstance(other, Pizza):
            return NotImplemented
        return (self.recipe == other.recipe) & (self.size == other.size)

    @property
    def size(self) -> str:
        """
        Проверяет корректно ли задан размер пиццы
        при создании экземпляра класса
        """
        if self._size in ['L', 'XL']:
            return self._size
        else:
            raise ValueError('Размер пиццы может быть только L или XL')


class Margherita(Pizza):
    """Реализация конкретного типа пиццы - Маргарита"""

    def __init__(self, size: str = 'L') -> None:
        """Инициализирует экземпляр. Задаёт рецепт."""
        super().__init__(size)
        self.recipe = {'tomato sauce', 'mozzarella', 'tomatoes'}


class Pepperoni(Pizza):
    """Реализация конкретного типа пиццы - Пепперони"""

    def __init__(self, size: str = 'L') -> None:
        """Инициализирует экземпляр. Задаёт рецепт."""
        super().__init__(size)
        self.recipe = {'tomato sauce', 'mozzarella', 'pepperoni'}


class Hawaiian(Pizza):
    """Реализация конкретного типа пиццы - Гавайская"""

    def __init__(self, size: str = 'L') -> None:
        """Инициализирует экземпляр. Задаёт рецепт."""
        super().__init__(size)
        self.recipe = {'tomato sauce', 'mozzarella', 'chicken', 'pineapples'}


@click.group()
def cli() -> object:
    pass


@cli.command()
@click.option('--pickup', default=False, is_flag=True)
@click.option('--delivery', default=False, is_flag=True)
@click.argument('pizza', nargs=1)
def order(pizza: str, delivery: bool, pickup: bool) -> None:
    """Готовит и доставляет пиццу"""
    cls_dict = {
        'margherita': Margherita,
        'pepperoni': Pepperoni,
        'hawaiian': Hawaiian
    }
    ordered_pizza = cls_dict[pizza]()
    bake(ordered_pizza)
    if delivery:
        delivery_(ordered_pizza)
    if pickup:
        pickup_(ordered_pizza)


@cli.command()
def menu() -> None:
    """Выводит меню"""
    pizza_instances = [Margherita(), Pepperoni(), Hawaiian()]
    for pizza in pizza_instances:
        for key, value in dict(pizza).items():
            click.echo(f'- {key}: {", ".join(product for product in value)}')


def log(_func: Optional[Callable[..., Any]] = None, *,
        output: str = 'default') -> Callable[..., Any]:
    """
    Декоратор.
    Если использовать как непараметрический,
        выводит имя функции и время выполнения.
    В качестве параметра можно добавить шаблон,
        подставит время и выведет.
    """

    def outer_wrapper(func: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(func)
        def inner_wrapper(*args: Any, **kwargs: Any) -> None:
            result = func(*args, **kwargs)
            if result.size == 'L':
                time = random.randint(1, 11)
            else:
                time = random.randint(11, 21)
            if output == 'default':
                print('{name} - {time}c!'.format(name=func.__name__,
                                                 time=time))
            else:
                print(output.format(time))

        return inner_wrapper

    if _func is None:
        return outer_wrapper
    else:
        return outer_wrapper(_func)


@log(output='Приготовили за {}c!')
def bake(pizza: object) -> object:
    """Готовит пиццу"""
    ordered_pizza = pizza
    return ordered_pizza


@log(output='Доставили за {}с!')
def delivery_(pizza: object) -> object:
    """Доставляет пиццу"""
    ordered_pizza = pizza
    return ordered_pizza


@log(output='Забрали за {}с!')
def pickup_(pizza: object) -> object:
    """Самовывоз"""
    ordered_pizza = pizza
    return ordered_pizza


if __name__ == '__main__':
    cli()
