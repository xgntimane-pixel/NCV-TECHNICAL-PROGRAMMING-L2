import random

def bubble_counts(values):
    data = values.copy()
    comparisons = 0
    swaps = 0

    for i in range(len(data) - 1):
        for j in range(len(data) - 1 - i):
            comparisons += 1

            if data[j] > data[j + 1]:
                data[j], data[j + 1] = data[j + 1], data[j]
                swaps += 1

    return comparisons, swaps

def selection_counts(values):
    data = values.copy()
    comparisons = 0
    swaps = 0

    for i in range(len(data) - 1):
        min_index = i

        for j in range(i + 1, len(data)):
            comparisons += 1

            if data[j] < data[min_index]:
                min_index = j

        if min_index != i:
            data[i], data[min_index] = data[min_index], data[i]
            swaps += 1

    return comparisons, swaps



random.seed(7)

for n in (8, 20, 100):
    values = [random.randint(0, 100) for _ in range(n)]

    print(n, "bubble", bubble_counts(values),
          "selection", selection_counts(values))
