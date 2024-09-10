import random
import itertools
from time import time

def load_words():
    with open('longman_3000.txt') as word_file:
        words1 = set(word_file.read().split())
    with open('oxford_5000.txt') as word_file:
        words2 = set(word_file.read().split())
    return words1.union(words2)

def same_dice(l1, l2, dice_set):
    count = 0
    for die in dice_set['white']:
        if l1 in die and l2 in die:
            count += 1
    if l1 in die and l2 in dice_set['yellow']:
            count += 1
    if l1 in die and l2 in dice_set['red']:
            count += 1
    return count

def score(frn_threshold, enm_threshold, pairs, freq, dice_set):
    friends = {k:pairs[k] for k in sorted_keys if pairs[k] > frn_threshold}
    enemies = {k:pairs[k] for k in sorted_keys if pairs[k] < enm_threshold}
    # pprint.pp(friends)
    # pprint.pp(enemies)
    points = 0
    for pair in friends:
        pts = (friends[pair] - frn_threshold) * freq[pair[0]] * freq[pair[1]]
        cnt = same_dice(*pair, dice_set)
        if cnt:
            points -= pts * cnt
            # print(f'NO! Friends {pair} co-occurence {friends[pair]} but on the same die!')
        else:
            points += pts
            # print(f'YAY! Friends {pair} co-occurence {friends[pair]} and on different die!')
    for pair in enemies:
        pts = (enm_threshold - enemies[pair]) * freq[pair[0]] * freq[pair[1]]
        cnt = same_dice(*pair, dice_set)
        if cnt:
            points += pts * cnt
            # print(f'YAY! Enemies {pair} co-occurence {enemies[pair]} and on the same die!')
        else:
            points -= pts
            # print(f'NO! Enemies {pair} co-occurence {enemies[pair]} and on different dice!')
    print(f'dice analysis: {points}')

def roll_dice(dice_set):
    dice = [random.choice(die) for die in dice_set["white"]]
    dice.append(random.choice(dice_set["yellow"]))
    dice.append(random.choice(dice_set["red"]))
    return sorted(dice)

def find_words_list(roll, word_list):
    words = []
    len_dist = [0, 0, 0, 0, 0, 0]
    for word in word_list:
        if len(word) > 1 and check(roll, word):
            words.append(word)
            len_dist[len(word)-2] += 1
    return words, len_dist

def make_faces(roll):
    faces = {}
    for l in roll:
        faces[l] = faces.get(l, 0) + 1
    return faces

def check(roll, word):
    faces = make_faces(roll)
    for l in word:
        if l not in faces or faces[l] == 0:
            return False
        else:
            faces[l] -= 1
    return True

def contain_double(word):
    for i, letter in enumerate(word[:-1]):
        if letter == word[i+1]:
            return True
    return False

def build_tree(word_list):
    tree = {}
    for word in word_list:
        cur = tree
        for l in word:
            if l not in cur:
                cur[l] = {}
            cur = cur[l]
        cur[0] = True
    return tree

def find_words_tree_perm(roll, tree):
    words = set()
    len_dist = [0, 0, 0, 0, 0, 0]
    for perm in itertools.permutations(roll):
        cur = tree
        for i, l in enumerate(perm):
            if l not in cur:
                break
            cur = cur[l]
            if i > 0 and 0 in cur:
                words.add(''.join(perm[:i+1]))
                len_dist[i-1] += 1
    return words, len_dist

def find_words_tree(roll, tree):
    len_dist = [0, 0, 0, 0, 0, 0]
    faces = make_faces(roll)
    words = traverse(tree, "", faces)
    for word in words:
        len_dist[len(word)-2] += 1
    return words, len_dist

def traverse(node, prefix, faces_left):
    words = set()
    for l in node:
        if l != 0 and l in faces_left and faces_left[l] > 0:
            fl = faces_left.copy()
            fl[l] -= 1
            words.update(traverse(node[l], prefix + l, fl))
    if len(prefix) > 1 and 0 in node:
        words.add(prefix)
    return words

SCORE_MAP = {2: 1, 3: 2, 4: 4, 5: 6, 6: 8, 7: 11, 8: 15}

def calc_score(word, dice_set):
    length = len(word)
    for l in word:
        if l in dice_set['red']:
            length += 1
            break
    score = SCORE_MAP[length]
    for l in word:
        if l in dice_set['yellow']:
            score += 1
            break
    return score

def simulate(dice_set, no_runs, word_tree):
    dice_set_list = { 'red': list(dice_set['red']),
                    'yellow': list(dice_set['yellow']),
                    'white': [list(die) for die in dice_set['white']]}
    avg_score = 0
    avg_max_score = 0
    for i in range(no_runs):
        score = 0
        max_score = 0
        roll = roll_dice(dice_set_list)
        # print(roll)
        words, len_dist = find_words_tree(roll, word_tree)
        for word in words:
            w_score = calc_score(word, dice_set)
            score += w_score
            max_score = max(max_score, w_score)
        if words:
            avg_score += score / len(words)
            avg_max_score += max_score
    print(f'average: {round(avg_score)}, max: {avg_max_score}')

vowels = {'e', 'a', 'i', 'o', 'u', 'y'}
dice_sets = [
            {"white": [ {'e', 'a', 's', 'i', 't', 'o'},
                        {'e', 'a', 'i', 'o', 'u', 'y'},
                        {'e', 'r', 'n', 's', 'l', 'c'},
                        {'e', 'r', 't', 'l', 'd', 'm'}],
            "yellow":   {'p', 'h', 'g', 'b', 'f', 'v'},
            "red":      {'w', 'j', 'k', 'x', 'z', 'q'}}
]

if __name__ == '__main__':
    import string
    import pprint
    english_words = load_words()
    # demo print
    # preprocess words
    words_7orless = []
    for w in english_words:
        if len(w) <= 7:
            processed = w.lower().replace("qu", 'q').replace('-', '')
            words_7orless.append(''.join(filter(str.isalpha, processed)))
    
    letters = [l for l in string.ascii_lowercase]
    print(contain_double("hello"))
    no_doubles = sum([1 for word in words_7orless if contain_double(word)])
    print(f'Number of word (<=7 letters) with double letters: {no_doubles} / {len(words_7orless)}')

    vowel_dist = [0,0,0,0,0]
    occ = {l:0 for l in letters}
    for word in words_7orless:
        for letter in set(word):
            # print(f'word: {word}, letter {letter}: {word.count(letter)} times')
            occ[letter] += 1

        no_vowels = 0
        for letter in word:
            if letter in vowels:
                no_vowels += 1
        vowel_dist[no_vowels] += 1
        if no_vowels == 4 and len(word)==6:
            print(word)
    vowel_dist = [c/len(words_7orless) for c in vowel_dist]
    # print(vowel_dist)
    
    # pprint.pp(occ)
    
    freq = {k:v/len(words_7orless) for k, v in occ.items()}
    # pprint.pp({k:round(v, 2) for k, v in freq.items()})

    # occ_dist = {l:[0,0,0,0] for l in letters}
    # for word in words_7orless:
    #     for letter in set(word):
    #         # print(f'word: {word}, letter {letter}: {word.count(letter)} times')
    #         occ_dist[letter][word.count(letter)-1] += 1
    # pprint.pp(occ_dist)
    # occ_dist_prop = {l:[0,0,0,0] for l in letters}
    # for k, v in occ_dist.items():
    #     s = sum(v)
    #     for i in range(0,4):
    #         occ_dist_prop[k][i] = round(v[i]/len(words_7orless), 3)
    # pprint.pp(occ_dist_prop)

    co_occ_dist = {l:{l2:0 for l2 in letters if l2 != l} for l in letters}
    for word in words_7orless:
        for letter in set(word):
            # print(f'word: {word}, letter {letter}: {word.count(letter)} times')
            for letter2 in set(word):
                if letter2 != letter:
                    co_occ_dist[letter][letter2] += 1
                    co_occ_dist[letter2][letter] += 1
                    
    # pprint.pp(co_occ_dist)

    co_occ_dist_prop = {l:{} for l in letters}
    max_p = 0
    for k, v in co_occ_dist.items():
        # v_norm = {l:o/(freq[l]*freq[k]) for l, o in v.items()}
        v_norm = v
        for i in v_norm:
            p = round(v_norm[i], 1)
            max_p = max(p, max_p)
            co_occ_dist_prop[k][i] = p
    co_occ_dist_prop = {l:{l2:p/max_p for l2, p in v.items()} for l, v in co_occ_dist_prop.items()}
    # pprint.pp(co_occ_dist_prop)

    tree = build_tree(words_7orless)

    pairs = {}
    for l1, v in co_occ_dist_prop.items():
        for l2, p in v.items():
            if ord(l1[0]) < ord(l2[0]):
                pairs[(l1, l2)] = p
    keys = pairs.keys()
    values = pairs.values()
    sorted_keys = sorted(pairs, key=lambda k: pairs[k])
    pairs = {k:pairs[k] for k in sorted_keys}
    # pprint.pp(pairs)
    frn_threshold = 0.25
    enm_threshold = 0.12
    
    for i, dice in enumerate(dice_sets):
        print(f'--- dice set {i} ---')
        score(frn_threshold=0.25, enm_threshold=0.12, pairs=pairs, freq=freq, dice_set=dice)
        simulate(dice, 10000, tree)

    
    
    
    
    

