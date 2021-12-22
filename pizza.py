from random import randint
import click


class BasePizza:
    """базовый класс для пицц"""
    def __init__(self, size: str):
        self.size = size

    def dict(self):
        result = {}
        for ingredient in self.recipe:
            result[ingredient] = True
        return result

    def __eq__(self, other):
        return self.recipe == other.recipe and self.size == other.size


class Margherita(BasePizza):
    recipe = ('tomato sauce', 'mozzarella', 'tomatoes')
    icon = '🧀'


class Pepperoni(BasePizza):
    recipe = ('tomato sauce', 'mozzarella', 'pepperoni')
    icon = '🍕'


class Hawaiian(BasePizza):
    recipe = ('tomato sauce', 'mozzarella', 'chicken', 'pineapples')
    icon = '🍍'


def log(template: str):
    """декоратор, подставляющий результат фукнции в шаблон"""
    def decorator(function: callable):
        def wrapper(pizza):
            print(template.replace('{}', str(function(pizza))))
        return wrapper
    return decorator


@log('👨‍🍳 Приготовили за {}с!')
def bake(pizza):
    """готовит пиццу"""
    if pizza.size.lower() == 'l':
        return randint(1, 2)
    return randint(3, 5)


@log('🛵 Доставили за {}с!')
def deliver(pizza):
    """доставляет пиццу"""
    return randint(1, 9)


@log('🏠 Забрали за {}с!')
def pickup(pizza):
    """самовывоз"""
    return randint(1, 9)


@click.group()
def cli():
    pass


@cli.command()
@click.argument('pizza', nargs=1)
@click.argument('size', nargs=1)
@click.option('--delivery', is_flag=True)
def order(pizza: str, size: str, delivery: bool):
    """готовит и доставляет пиццу"""
    current_order = globals()[pizza.capitalize()](size)
    bake(current_order)
    if delivery:
        deliver(current_order)
    else:
        pickup(current_order)


@cli.command()
def menu():
    """выводит меню"""
    available = [Margherita, Pepperoni, Hawaiian]
    for pizza in available:
        print(f'- {pizza.__name__} {pizza.icon}(L/XL): ', end='')
        print(*pizza('L').dict().keys(), sep=', ')


if __name__ == '__main__':
    cli()
