import os
import openai
from flask import Flask, redirect, render_template, request, url_for, session, jsonify
import logging

# Add this line after the imports at the top of the file
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")
app.secret_key = os.environ.get('SECRET_KEY', 'zhengyuan-yuyan')

# this is a function that takes in two parameters, a question and a plan.
def is_question_related_to_plan(question, plan):
    
    # key words related to the plan
    keywords = ['workout', 'nutrition', 'exercise', 'meal', 'plan', 'schedule']

    question_lower = question.lower()

    # loop through each keyword in the list.
    for keyword in keywords:
        if keyword in question_lower:
            return True
    return False

@app.route('/')
# this function is executed when the root URL is requested
def home():
    return render_template('index.html')

# this function is executed when a GET or POST request is made to '/personal-info'
@app.route('/personal-info', methods=['GET', 'POST'])
def personal_info():
    if request.method == 'POST':
        pass     
    return render_template('personal-info.html')


@app.route('/api/generate-plan', methods=['POST'])
# this function is executed when a POST request is made to '/api/generate-plan'
def generate_plan():
    # Retrieve the height, weight, gender, fitness goal, fitness level, and dietary requirements from the JSON data in the request
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
        # Use OpenAI's text generation API to generate the plan
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

        # Return the generated plan as a JSON object
        return jsonify({'plan': plan})

    except Exception as e:
        logging.exception("Error occurred while generating the plan")
        return jsonify({'error': str(e)}), 500

@app.route('/result')
# this function is executed when the "/result" URL is requested
def result():
    return render_template('result.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    # Get the user's message from the request
    message = request.json.get('message')
    # If no message is provided, return an error
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
        # Generate a response from the GPT API based on the prompt
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            temperature=0.8,
            max_tokens=100,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        # Extract the generated response message from the API response and return it as a JSON object
        response_message = response.choices[0].text.strip()
        return jsonify({'response': response_message})

    except Exception as e:
        # If an error occurs during the API call, return an error message as a JSON object
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
