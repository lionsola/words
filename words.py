def load_words():
    with open('english-words/words_alpha.txt') as word_file:
        valid_words = set(word_file.read().split())

    return valid_words


if __name__ == '__main__':
    import string
    import pprint
    english_words = load_words()
    # demo print
    words_7orless = [w for w in english_words if len(w) <= 7]
    freq = {l:0 for l in string.ascii_lowercase}
    for word in words_7orless:
        for letter in set(word):
            # print(f'word: {word}, letter {letter}: {word.count(letter)} times')
            freq[letter] += 1
    freq = {k:v/len(words_7orless) for k, v in freq.items()}
    pprint.pp(freq)

    occ_dist = {l:[0,0,0,0] for l in string.ascii_lowercase}

    # for word in words_7orless:
    #     for letter in set(word):
    #         # print(f'word: {word}, letter {letter}: {word.count(letter)} times')
    #         occ_dist[letter][word.count(letter)-1] += 1
    # occ_dist_prop = {l:[1,0,0,0] for l in string.ascii_lowercase}
    # for k, v in occ_dist.items():
    #     s = sum(v)
    #     for i in range(1,4):
    #         occ_dist_prop[k][i] = round(v[i]/s, 3)
    # pprint.pp(occ_dist_prop)

    co_occ_dist = {l:{l2:0 for l2 in string.ascii_lowercase if l2 != l} for l in string.ascii_lowercase}
    for word in words_7orless:
        for letter in set(word):
            # print(f'word: {word}, letter {letter}: {word.count(letter)} times')
            for letter2 in set(word):
                if letter2 != letter:
                    co_occ_dist[letter][letter2] += 1
    # pprint.pp(co_occ_dist)

    co_occ_dist_prop = {l:{} for l in string.ascii_lowercase}
    threshold = 0.055
    max_p = 0
    for k, v in co_occ_dist.items():
        v_norm = {l:o/(freq[l]*freq[k]) for l, o in v.items()}
        for i in v_norm:
            p = round(v_norm[i], 1)
            max_p = max(p, max_p)
            co_occ_dist_prop[k][i] = p
    co_occ_dist_prop = {l:{l2:p/max_p for l2, p in v.items()} for l, v in co_occ_dist_prop.items()}
    pprint.pp(co_occ_dist_prop)

    pair = {}
    for l, v in co_occ_dist_prop.items():
        for l2, p in v.items():
            if ord(l) < ord(l2):
                pair[f'{l}-{l2}'] = p
    keys = pair.keys()
    values = pair.values()
    sorted_keys = sorted(pair, key=lambda k: pair[k])
    pprint.pp({k:pair[k] for k in sorted_keys if pair[k] > 0.28})
    pprint.pp({k:pair[k] for k in sorted_keys if pair[k] < 0.1})