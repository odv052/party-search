import csv
import time
from collections import defaultdict


def solve(likes, min_group=3):
    s = time.time()
    assert min_group > 1
    likes_map = defaultdict(set)
    for u1, u2 in map(lambda p: (int(p[0]), int(p[1])), likes):
        likes_map[u1].add(u2)

    # filter out not mutual likes
    for u1, u2_set in tuple(likes_map.items()):  # for u1, u2_set in likes_map.items():
        for u2 in tuple(u2_set):
            if u1 not in likes_map[u2]:
                u2_set.discard(u2)

    # remove small sets
    for u1, u2_set in tuple(likes_map.items()):
        if len(u2_set) < min_group - 1:
            likes_map.pop(u1)

    groups = set()

    def traverse(ls, rs, restriction):
        if not rs and len(ls) >= min_group:
            group = tuple(sorted(list(ls)))
            groups.add(group)
        for v in rs:
            if v not in likes_map:  # because of [remove small sets] section
                continue
            traverse(ls | {v}, (likes_map[v] - (ls | {v}) & restriction), likes_map[v] & restriction)

    for u1, u2_set in likes_map.items():
        traverse({u1}, u2_set, u2_set)

    # remove subsets
    g_list = sorted(list(set(g) for g in groups), key=lambda g: len(g))
    _g_list = list(g_list)
    for g in g_list:
        for _g in _g_list:
            if g.issubset(_g) and g is not _g:
                g_list.discard(g)

    # print groups
    if not groups:
        print('No groups =(')

    groups = sorted([sorted(list(g)) for g in groups])
    print(f'Groups: {len(groups)} in {round(time.time() - s, 2)}')
    for group in groups:
        print(', '.join((str(u)) for u in sorted(list(group))))

    # validation
    for g in groups:
        for i in g:
            if not (set(g) - {i}).issubset(likes_map[i]):
                1/0

    return groups


if __name__ == '__main__':
    with open('likes.csv') as f:
        likes = list(csv.reader(f))
        solve(likes)
