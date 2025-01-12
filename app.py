from flask import Flask, request, render_template_string
from itertools import permutations

app = Flask(__name__)

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Tvers-løser</title>
</head>
<body>
    <h1>Løser for NRK Tvers :)</h1>
    <form method="post" action="/solve">
        <label for="letters">Skriv inn alle tilgjengelige bokstaver:</label>
        <input type="text" id="letters" name="letters" required>
        <button type="submit">Solve</button>
    </form>
    {% if result %}
    <div>{{ result | safe }}</div>
    {% endif %}
</body>
<footer style="position: fixed; bottom: 0; right: 0; padding: 10px;">
Laget med ❤️  |  <a href="https://github.com/henninss/nrk-tvers-solver">GitHub</a>
</footer
</html>
'''

@app.route("/", methods=["GET"])
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route("/solve", methods=["POST"])
def solve():
    available_letters = request.form.get("letters")

    wordlist_path = './nsf2022.txt'
    easy_wordlist_path = './ordliste_aspell.txt'
    try:
        with open(wordlist_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        with open(easy_wordlist_path, 'r', encoding='iso-8859-1') as file:
            easy_lines = file.readlines()

        lines = [line.strip() for line in lines]
        # Five letter words only
        lines = [line for line in lines if len(line) == 5]
        wordlist = set(lines)

        easy_lines = [line.strip() for line in easy_lines]
        # Five letter words only
        easy_lines = [line for line in easy_lines if len(line) == 5]
        easy_wordlist = set(easy_lines)

        letters = list(available_letters)
        easy_solutions = set()
        solutions = set()
        # Permutates every combination. Creates two words from the permutation
        # where the third letter is the same. If both exist in the wordlist == match
        for perm in permutations(letters):
            word1 = ''.join(perm[:5])
            word2 = ''.join(list(perm[5:7]) + list(perm[2]) + list(perm[7:]))

            if word1 in wordlist and word2 in wordlist:
                solutions.add(tuple(sorted([word1, word2])))
            if word1 in easy_wordlist and word2 in easy_wordlist:
                easy_solutions.add(tuple(sorted([word1, word2])))

        if len(solutions) == 0:
            return render_template_string(HTML_TEMPLATE, result="Ingen løsning funnet.")

        solutions = sorted(solutions, key=lambda x: x[0]+x[1])
        easy_solutions = sorted(easy_solutions, key=lambda x: x[0]+x[1])
        printer = ''
        if len(easy_solutions) > 0:
            printer += '<h2>Mest sannsynlige løsninger:</h2><p>'
            for solution in easy_solutions:
                printer += f'{solution[0]}, {solution[1]}<br>'
        else:
            printer += '<p>'
        printer += '<h2>Mulige løsninger:</h2>'
        for solution in solutions:
            printer += f'{solution[0]}, {solution[1]}<br>'

        printer += '</p>'

        return render_template_string(HTML_TEMPLATE, result=printer)
    except Exception as e:
        return render_template_string(HTML_TEMPLATE, result=f"Error: {e}")

if __name__ == "__main__":
    app.run()

