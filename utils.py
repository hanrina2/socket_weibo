import random
import time


def log(*args, **kwargs):
    time_format = '%Y/%m/%d %H:%M:%S'
    localtime = time.localtime(int(time.time()))
    formatted = time.strftime(time_format, localtime)
    with open('log.top.txt', 'a', encoding='utf-8') as f:
        print('[Log:]', formatted, *args, **kwargs)
        print('[Log:]', formatted, *args, file=f, **kwargs)


def random_string():
    seed = 'bdjsdlkgjsklgelgjelgjsegker234252542342525g'
    s = ''
    for i in range(16):
        random_index = random.randint(0, len(seed) - 2)
        s += seed[random_index]
    return s
