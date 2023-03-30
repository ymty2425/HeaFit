import os
import openai
from flask import Flask, redirect, render_template, request, url_for, session, jsonify

# 124500 words allowed for training

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/personal-info', methods=['GET', 'POST'])
def personal_info():
    if request.method == 'POST':
        # Handle form submission and generate plan
        pass
    return render_template('personal-info.html')

@app.route('/api/generate-plan', methods=['POST'])
def generate_plan():
    # Extract the data from the request
    data = request.json

    # Generate the workout and nutrition plan using the OpenAI API (or any other API)
    # The code will depend on the specific API or service you are using
    # For example, you may call functions that use OpenAI API here

    # Mock plan for demonstration purposes
    plan = {
        'workout': 'Sample workout plan',
        'nutrition': 'Sample nutrition plan',
    }

    return jsonify(plan)

@app.route('/result')
def result():
    return render_template('result.html')

@app.route('/api/chat', methods=['POST'])
def chat_api():
    message = request.json.get('message')
    chatbot_response = openai.Completion.create(
        engine="davinci-codex",
        prompt=f"User: {message}\nAI:",
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.5,
    )
    response = chatbot_response.choices[0].text.strip()
    return jsonify(response=response)

if __name__ == '__main__':
    app.run(debug=True)

'''
@app.route('/generate_plan', methods=['POST'])
def generate_plan():
    fitness_goal = request.form.get('fitness_goal')
    fitness_level = request.form.get('fitness_level')
    dietary_requirements = request.form.get('dietary_requirements')

    response = openai.Comletion.create(
        model = "text-davinci-003",
        workout_plan = generate_prompt(fitness_goal, fitness_level, dietary_requirements),
        temperature = 0.6,
    )
    
    # can save the plan to the db
    # session["hea_fit_plan"] = workout_plan
    return redirect(url_for('plan', result = response.choices[0].text))

@app.route('/plan')
def plan():
    # can try to retreive from the db
    workout_plan = session.get("workout_plan", "")
    nutrition_plan = session.get("nutrition_plan", "")

    return render_template('plan.html', workout_plan=workout_plan, nutrition_plan=nutrition_plan)

def generate_prompt(goal, level, require):
    return """My fitness is {}, fitness level is {}, and dietary requirements are {}.
    Can you please help me generate a work out plan: """.format(
        goal.capitalize(), level.capitalize(), require.capitalize()
    )
'''

'''
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
    return render_template("index.html", result=result)
'''