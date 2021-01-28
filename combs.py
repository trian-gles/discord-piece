from itertools import combinations
from string import ascii_uppercase
from random import randrange



#print(performers)


class WeightedItem:
    def __init__(self, tag):
        self.tag = tag
        self.ms = 0

    def move_ms(self):
        self.ms += 1

    def __str__(self):
        return str(self.tag)

    def __repr__(self):
        return self.__str__()

def return_min_weight(step):
    min_weight = None
    min_pair = None
    for pair in step:
        weight = pair[0].ms + pair[1].ms
        if (min_weight == None) or (weight < min_weight):
            min_weight = weight
            min_pair = pair
    return min_pair



#print(combs)
#print(number_combs)


def build_steps(performers):
    weight_perfs = [WeightedItem(perf) for perf in performers]
    combs = list(combinations(weight_perfs, 2))
    number_combs = len(combs)
    num_rooms = int(len(performers) / 2)
    step_num = int(number_combs / num_rooms)
    steps = []
    for _ in range(step_num):
        current_step = []
        for c in combs:
            if not any(c[0] in cur for cur in current_step):
                if not any(c[1] in cur for cur in current_step):
                    current_step.append(c)
                    combs.remove(c)
        steps.append(current_step)
        combs.reverse()
    for step in steps:
        unused_perfs = []
        for p in weight_perfs:
            if not any(p in c for c in step):
                unused_perfs.append(p)
            if len(unused_perfs) == 2:
                step.append(tuple(unused_perfs))
                unused_perfs = []
        if len(unused_perfs) > 0:
            three_room = randrange(len(step))
            step[three_room] = (unused_perfs[0],) + step[three_room]

        least_ms = return_min_weight(step)
        for p in least_ms:
            p.move_ms()
        step.insert(0, step.pop(step.index(least_ms)))
    return steps

if __name__ == "__main__":
    num_perfs = 6

    performers = list(ascii_uppercase)[:num_perfs]

    steps = build_steps(performers)
    print(steps)

    mainstage_counts = {}

    mainstages = [step[0] for step in steps]

    for ms in mainstages:
        for p in ms:
            if p not in mainstage_counts.keys():
                mainstage_counts[p] = 1
            else:
                mainstage_counts[p] += 1



    print(mainstages)
    print(mainstage_counts)
