from itertools import permutations

wordlist_path = './nsf2022.txt'

with open(wordlist_path, 'r', encoding='utf-8') as file:
    lines = file.readlines()

print('Words in list:', len(lines))
lines = [line.strip() for line in lines]
# Five letter words only
lines = [line for line in lines if len(line) == 5]
wordlist = set(lines)

available_letters = input('Skriv inn bokstaver som er tilgjengelige: ')
letters = list(available_letters)


solutions = set()
# Permutates every combination. Creates two words from the permutation
# where the third letter is the same. If both exist in the wordlist == match
for perm in permutations(letters):
    word1 = ''.join(perm[:5])
    word2 = ''.join(list(perm[5:7]) + list(perm[2]) + list(perm[7:]))

    if word1 in wordlist and word2 in wordlist:
        solutions.add(tuple(sorted([word1, word2])))

solutions = sorted(solutions, key=lambda x: x[0]+x[1])
for solution in solutions:
    print(f'{solution[0]}, {solution[1]}')



