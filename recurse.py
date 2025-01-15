import time

cache = {}

def fib(n):
    if n <= 1:
        return n
    if n in cache:
        return cache[n]
    val = fib(n-1) + fib(n-2)
    cache[n] = val
    return val

for i in range(60):
    start = time.time()
    num = fib(i)

    difference = time.time() - start

    print(i, fib(i), f'{difference:.20f}')