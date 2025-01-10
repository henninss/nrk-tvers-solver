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
    <h2>Løsning:</h2>
    <p>{{ result }}</p>
    {% endif %}
</body>
<footer style="position: absolute; bottom: 0;">
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
    try:
        with open(wordlist_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        lines = [line.strip() for line in lines]
        # Five letter words only
        lines = [line for line in lines if len(line) == 5]
        wordlist = set(lines)

        letters = list(available_letters)

        # Permutates every combination. Creates two words from the permutation
        # where the third letter is the same. If both exist in the wordlist == match
        for perm in permutations(letters):
            word1 = ''.join(perm[:5])
            word2 = ''.join(list(perm[5:7]) + list(perm[2]) + list(perm[7:]))

            if word1 in wordlist and word2 in wordlist:
                result = f"{word1}, {word2}"
                return render_template_string(HTML_TEMPLATE, result=result)
        return render_template_string(HTML_TEMPLATE, result="Ingen løsning funnet.")

    except Exception as e:
        return render_template_string(HTML_TEMPLATE, result=f"Error: {e}")

if __name__ == "__main__":
    app.run(debug=True)

