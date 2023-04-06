# HeaFit - Flask Web Application

HeaFit is a web application built using Flask that generates personalized workout and nutrition plans for users based on their fitness goals and preferences. Users can also interact with a chatbot to get more information and ask questions about their plans.

## Features

- Personalized workout and nutrition plan generation
- User input validation
- Chatbot for user interaction and answering questions
- Responsive design for different devices

## Prerequisites

To run this project, you'll need the following installed:

- Python 3.6 or later
- pip (Python package manager)

## Installation

1. Clone the repository:
https://github.com/ymty2425/HeaFit.git


## Setup

1. If you don’t have Python installed, [install it from here](https://www.python.org/downloads/).

2. Clone this repository.

3. Navigate into the project directory:

   ```bash
   $ cd HeaFit
   ```

4. Create a new virtual environment:

   ```bash
   $ python -m venv venv
   $ . venv/bin/activate
   ```

5. Install the requirements:

   ```bash
   $ pip install -r requirements.txt
   ```

6. Make a copy of the example environment variables file:

   ```bash
   $ cp .env.example .env
   ```

7. Add your [API key](https://beta.openai.com/account/api-keys) to the newly created `.env` file.

8. Run the app:

   ```bash
   $ flask run
   ```

You should now be able to access the app at [http://localhost:5000](http://localhost:5000)! For the full context behind this example app, check out the [tutorial](https://beta.openai.com/docs/quickstart).
