def zadanie1(n):
    if n < 3:
        if n == 1:
            return 1
        return 3
    return zadanie1(n-1) * n + zadanie1(n-2) * (n-1)


def zadanie3(n):
    if n < 3:
        if n == 1:
            return 1
        return 2
    return zadanie3(n-1) - zadanie3(n-2) + 2 * n


def zadanie5(n):
    if n == 1:
        return 1
    if n % 2 == 0:
        return n * zadanie5(n-1)
    return n + zadanie5(n-2)


def zadanie7(n):
    if n < 3:
        return 1
    summ = 0
    for i in range(1, n):
        summ += zadanie7(i, True)
    return summ


def zadanie9(n):
    if n >= 1000:
        return 1000
    if n % 2 == 0:
        return n * zadanie9(n+1) / 2
    return n * zadanie9(n+1)


def zadanie10(n, isRecurring=False):
    if isRecurring:
        if reclist[n] > 0:
            return reclist[n]
        if n == 0:
            return 0
        if n % 2 == 0:
            a = zadanie10(n//10, True) + n % 10
            reclist[n] = a
            return a
        a = zadanie10(n//10, True)
        reclist[n] = a
        return a
    if len(reclist) < 100:
        for i in range(2 * n + 1):
            if i % 10000_000 == 0:
                print(i // 10000000)
            reclist.append(-1)
        print(0)
    return zadanie10(n, True)


reclist = []
counter = 0
for k in range(1000000000, 2000000000):
    if zadanie10(k) == 0:
        counter += 1
print(counter)