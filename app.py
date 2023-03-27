import os
import openai
from flask import Flask, redirect, render_template, request, url_for

# 124500 words allowed for training

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")


@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        premise = request.form["premise"]
        argument = request.form["argument"]
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=generate_prompt(premise, argument),
            temperature=0.6,
        )
        return redirect(url_for("index", result=response.choices[0].text))

    result = request.args.get("result")
    print(result)
    return render_template("index.html", result=result)

def generate_prompt(premise, argument):
    return """Suggest three names for an animal that is a superhero.

Animal: Cat
Names: Captain Sharpclaw, Agent Fluffball, The Incredible Feline
Animal: Dog
Names: Ruff the Protector, Wonder Canine, Sir Barks-a-Lot
Animal: {}
Names:""".format(
        premise.capitalize(), argument.capitalize()
    )