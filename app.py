import os
import openai
from flask import Flask, redirect, render_template, request, url_for, session, jsonify
import logging

# Add this line after the imports at the top of the file
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")
app.secret_key = os.environ.get('SECRET_KEY', 'zhengyuan-yuyan')

def is_question_related_to_plan(question, plan):
    
    # key words related to the plan
    keywords = ['workout', 'nutrition', 'exercise', 'meal', 'plan', 'schedule']

    question_lower = question.lower()
    for keyword in keywords:
        if keyword in question_lower:
            return True
    return False

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/personal-info', methods=['GET', 'POST'])
def personal_info():
    if request.method == 'POST':
        pass     
    return render_template('personal-info.html')

@app.route('/api/generate-plan', methods=['POST'])
def generate_plan():
    height = request.json.get('height')
    weight = request.json.get('weight')
    gender = request.json.get('gender')
    fitness_goal = request.json.get('fitness_goal')
    fitness_level = request.json.get('fitness_level')
    dietary_requirements = request.json.get('dietary_requirements')

    # print("Received data:", request.json)

    try:
        prompt = f"Generate a workout and nutrition plan for a {gender} with the following details:\n" \
                 f"Height: {height} cm\n" \
                 f"Weight: {weight} kg\n" \
                 f"Fitness goal: {fitness_goal}\n" \
                 f"Fitness level: {fitness_level}\n" \
                 f"Dietary requirements: {dietary_requirements}\n\n" \
                 f"Workout plan:\n"

        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            temperature=0.7,
            max_tokens=500,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        plan = response.choices[0].text.strip()

        # store plan in the session
        session['plan'] = plan  

        return jsonify({'plan': plan})

    except Exception as e:
        logging.exception("Error occurred while generating the plan")
        return jsonify({'error': str(e)}), 500

@app.route('/result')
def result():
    return render_template('result.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    message = request.json.get('message')
    if not message:
        return jsonify({'error': 'No message provided'}), 400
    
    # get plan from session
    plan = session.get('plan', '')

    # check whether the user questions are related to the plan
    is_related_to_plan = is_question_related_to_plan(message, plan)

    # generate different prompt according to the input
    if is_related_to_plan:
        prompt = f"Workout and nutrition plan:\n{plan}\n\nUser: {message}\n\nAI:"
    else:
        prompt = f"{message}\n\nAI:"

    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            temperature=0.8,
            max_tokens=100,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        response_message = response.choices[0].text.strip()
        return jsonify({'response': response_message})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
