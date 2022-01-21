import csv
import random
from itertools import permutations

import numpy as np


def rand_gen(users_num=15, like_possibility=0.5):
    users = [u for u in range(users_num)]

    c = 0
    with open('likes.csv', 'w') as f:
        w = csv.writer(f)
        for u1, u2 in permutations(users, 2):
            if random.random() - 1 + like_possibility > 0:
                w.writerow((u1, u2))
                c += 1
    print(c)


def smart_gen(users_num=10000, groups_num=300, min_group=3):
    users = [u for u in range(users_num)]
    random.shuffle(users)

    group_sizes = np.abs(np.floor(np.random.normal(0, 2, groups_num))).astype('int') + min_group
    groups = []
    for g_size in group_sizes:
        group = []
        _u = list(users)
        for i in range(g_size):
            group.append(_u.pop(random.randint(0, users_num - i -1)))
        groups.append(group)

    with open('groups.csv', 'w') as f:
        w = csv.writer(f)
        w.writerows(sorted(list(map(lambda g: sorted(g), groups))))

    c = 0
    with open('likes.csv', 'w') as f:
        w = csv.writer(f)
        for g in groups:
            p = list(permutations(g, 2))
            w.writerows(p)
            c += len(p)

    print('total likes: ', c)
    return


if __name__ == '__main__':
    smart_gen()
