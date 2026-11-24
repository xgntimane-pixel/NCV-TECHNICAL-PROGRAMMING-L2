
data = [48, 72, 90, 60, 54, 72, 54, 72]


def total_of(data):
    return sum(data)

def mean_of(data):
    return sum(data) / len(data)

def max_of(data):
    return max(data)

def min_of(data):
    return min(data)

def find_first(data, value):
    if value in data:
        return data.index(value)
    return -1

def find_all(data, value):
    positions = []

    for i in range(len(data)):
        if data[i] == value:
            positions.append(i)

    return positions

def count_of(data, value):
    return data.count(value)


def mode_of(data):
    frequencies = {}

    for value in data:
        if value in frequencies:
            frequencies[value] += 1
        else:
            frequencies[value] = 1

    highest_frequency = max(frequencies.values())

    modes = []

    for value in frequencies:
        if frequencies[value] == highest_frequency:
            modes.append(value)

    return sorted(modes)

print("Total  :", total_of(data))
print("Mean   :", mean_of(data))
print("Highest:", max_of(data))
print("Lowest :", min_of(data))
print("First 72 at:", find_first(data, 72))
print("All 72 at  :", find_all(data, 72))
print("Count of 72:", count_of(data, 72))
print("Mode   :", mode_of(data))
print("Mode (tie):", mode_of([1, 2, 2, 3, 3]))
