import random


def random_int(start, end):
    min = end
    for _ in range(start+2):
        result = random.randint(start, end)
        if min >= result:
            min = result
    return min



from collections import Counter

counter = Counter()
for _ in range(2000):
    result = random_int(1, 5)
    counter.update(str(result))
    
print(counter)