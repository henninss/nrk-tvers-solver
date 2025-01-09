from flask import Flask, request, render_template_string

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
        # 5-letter words only
        lines = [line for line in lines if len(line) == 5]

        letters = list(available_letters)
        legal_words = []

        for line in lines:
            line_of_dic = list(line)
            if all(line_of_dic.count(char) <= letters.count(char) for char in line_of_dic):
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
                        except ValueError:
                            pass
                    if combination[0] == word_one[2] and len(combination) == 1:
                        result = f"{word_one}, {word_two}"
                        return render_template_string(HTML_TEMPLATE, result=result)
        return render_template_string(HTML_TEMPLATE, result="No solution found.")

    except Exception as e:
        return render_template_string(HTML_TEMPLATE, result=f"Error: {e}")

if __name__ == "__main__":
    app.run(debug=True)

