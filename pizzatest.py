import pytest
import pizza as p
import re
import subprocess


def test_pickup(capsys):
    p.pickup(p.Margherita('XL'))
    captured = capsys.readouterr()
    assert re.match('🏠 Забрали за .с!\n', captured.out)


def test_deliver(capsys):
    p.deliver(p.Margherita('XL'))
    captured = capsys.readouterr()
    assert re.match('🛵 Доставили за .с!\n', captured.out)


def test_bake(capsys):
    p.bake(p.Margherita('XL'))
    captured = capsys.readouterr()
    assert re.match('👨‍🍳 Приготовили за .с!\n', captured.out)


def test_eq():
    assert p.Margherita('XL') != p.Margherita('L')


def test_dict():
    assert p.Pepperoni('L').dict() == {'tomato sauce': True, 'mozzarella': True, 'pepperoni': True}


def test_ex():
    with pytest.raises(Exception):
        p.bake('hello')


def test_menu():
    cmd = ['python', 'pizza.py', 'menu']
    captured = subprocess.Popen(cmd, stdout=subprocess.PIPE).communicate()[0]
    assert captured == b'- Margherita \xf0\x9f\xa7\x80(L/XL): tomato sauce, mozzarella, tomatoes\n- Pepperoni ' \
                       b'\xf0\x9f\x8d\x95(L/XL): tomato sauce, mozzarella, pepperoni\n- Hawaiian ' \
                       b'\xf0\x9f\x8d\x8d(' \
                       b'L/XL): tomato sauce, mozzarella, chicken, pineapples\n'


def test_order():
    cmd = ['python', 'pizza.py', 'order', 'pepperoni', 'xl']
    captured = subprocess.Popen(cmd, stdout=subprocess.PIPE).communicate()[0]
    assert re.match('👨\u200d🍳 Приготовили за .с!\n🏠 Забрали за .с!', captured.decode("utf-8"))


def test_order_del():
    cmd = ['python', 'pizza.py', 'order', 'pepperoni', 'l', '--delivery']
    captured = subprocess.Popen(cmd, stdout=subprocess.PIPE).communicate()[0]
    assert re.match('👨\u200d🍳 Приготовили за .с!\n🛵 Доставили за .с!', captured.decode("utf-8"))

