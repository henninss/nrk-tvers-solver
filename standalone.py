wordlist_path = './nsf2022.txt'

with open(wordlist_path, 'r', encoding='utf-8') as file:
    lines = file.readlines()

lines = [line.strip() for line in lines]
# Five letter words only
lines = [line for line in lines if len(line) == 5]

available_letters = input('Skriv inn bokstaver som er tilgjengelige: ')
letters = list(available_letters)

legal_words = []
for line in lines:
    line_of_dic = list(line)
    # If all characters in the word exist in the dictionary
    if all(line_of_dic.count(char) == letters.count(char) for char in line_of_dic):
        legal_words.append(''.join(line_of_dic))

for word_one in legal_words:
    for word_two in legal_words:
        if word_one == word_two:
            continue
        if word_one[2] == word_two[2]:
            letters_verify = letters.copy()
            combination = list(word_one) + list(word_two)
            for char in letters_verify:
                try:
                    combination.remove(char)
                # Catch error if combination does not have letter
                except ValueError:
                    pass
                if (combination[0] == word_one[2]) and (len(combination) == 1):
                    print(word_one, word_two)
                    exit()
                

