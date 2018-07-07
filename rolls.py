from random import randint


def multiple_roll(dice, quantity):
    x = []
    for i in range(quantity):
        x.append(randint(1, dice))
    s = sum(x)
    return x, s


def generate_name():
    name = open('names_and_surnames\\names.txt', 'r', encoding='utf-8')
    sur = open('names_and_surnames\\surnames.txt', 'r', encoding='utf-8')
    names = name.read().strip().split(' ')
    surnames = list(map(str.strip, filter(None, sur.read().strip().split(','))))
    n = names[randint(0, len(names) - 1)]
    surname = surnames[randint(0, len(surnames) - 1)]
    name.close()
    sur.close()
    end = '{} {}'.format(n, surname)
    print(end)
    return end


def add_name(text):
    text = text.strip().title()
    name = open('names_and_surnames\\names.txt', 'a', encoding='utf-8')
    add = ' ' + text
    print('added name' + add)
    name.write(add)
    name.close()
    return add


def add_sur(text):
    sur = open('names_and_surnames\\surnames.txt', 'a', encoding='utf-8')
    add = ' ' + text.strip().title() + ','
    print('added surname' + add)
    sur.write(add)
    sur.close()
    return add
