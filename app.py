import random
import string
from hashlib import md5
from flask import Flask, request, render_template_string

app = Flask(__name__)

def get_adjectives(p: str = "adjectives.txt") -> list:
    with open(p, "r") as fp:
        content = fp.readlines()
    return content

def get_nouns(p: str = "nouns.txt") -> list:
    with open(p, "r") as fp:
        content = fp.readlines()
    return content

def create_customer_nr(name:str) -> str:
    md5_hash = md5(name.encode()).hexdigest()
    first_2_bytes_hex = md5_hash[:4]
    decimal = int(first_2_bytes_hex, 16)
    formatted = f"{decimal:05d}" # Prepend with zeros if smaller than 10 000
    return formatted

def create_new_project_name(cust_name:str) -> str:
    cust_name = cust_name.lower()
    cust_nr = create_customer_nr(cust_name)
    random_letter = random.choice(string.ascii_lowercase)
    adjective_list = get_adjectives()
    nouns_list = get_nouns()

    adjectives_random_letter_list = [word for word in adjective_list if word.startswith(random_letter)]
    nouns_random_letter_list = [word for word in nouns_list if word.startswith(random_letter)]

    random_adjective = random.choice(adjectives_random_letter_list)
    random_noun = random.choice(nouns_random_letter_list)

    return f"{cust_nr}: {random_adjective.capitalize()} {random_noun.capitalize()}"


def get_template(p:str) -> str:
    with open(p, "r") as fp:
        content = fp.read()
    return content

@app.route("/", methods=["GET", "POST"])
def home():
    result = ""
    if request.method == "POST":
        user_input = request.form["user_input"]
        result = create_new_project_name(user_input)
    return render_template_string(get_template("home_template.html"), result=result)


if __name__ == "__main__":
    app.run(debug=True)