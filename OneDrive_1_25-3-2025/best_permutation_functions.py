def get_spread(graph, S):

    text_seed = [str(x) for x in S]
    file1 = open('temp.txt', 'w')
    file1.writelines(text_seed)
    file1.close()

    output = os.popen(f'./infection {graph} ./temp.txt')
    spread = float(output.read().strip().split('\n')[3].split(' ')[1])

    return spread


def get_best_permutation(graph, seed_set):

    best_spread = get_spread(graph, seed_set)
    best_permutation = seed_set.copy()

    for i in tqdm(range(0, 1000)):
        random.shuffle(seed_set)
        spread = get_spread(graph, seed_set)
        if(spread > best_spread):
            best_spread = spread
            best_permutation = seed_set.copy()
    
    return best_permutation