document.addEventListener('DOMContentLoaded', () => {
    const personalInfoForm1 = document.getElementById('personal-info-form');
    const planElement = document.getElementById('plan');
    const chatbotContainer = document.getElementById('chatbot-container');
    const chatbotContent = document.getElementById('chatbot-content');
    const messages = document.getElementById('messages');
    const messageInput = document.getElementById('message-input');
    const personalInfoForm = document.querySelector('#personal-info-form');
    
    if (personalInfoForm) {
      personalInfoForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const formData = new FormData(personalInfoForm);
        const data = Object.fromEntries(formData);

        console.log("Form data:", data);

        try {
          const response = await fetch('/api/generate-plan', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data),
          });
          if (response.ok) {
            const plan = await response.json();
    
            // Save the generated workout plan in the local storage to access it on the result page
            localStorage.setItem('workoutPlan', plan.plan);
    
            // Redirect to the result page
            window.location.href = "/result";
          } else {
            alert('Error generating the workout plan. Please try again.');
          }
        } catch (error) {
          console.error('Error:', error);
          alert('Error generating the workout plan. Please try again.');
        }
      });
    }

    // Display the workout and nutrition plan on the result page
    if (planElement) {
      const plan = localStorage.getItem('workoutPlan');
      localStorage.removeItem('workoutPlan');
  
      if (plan) {
        // Replace newline characters with <br> tags
        const formattedWorkoutPlan = plan.replace(/\n/g, '<br>');

        // Display the plan
        planElement.innerHTML = `
          <h2>Workout Plan</h2>
          <p>${formattedWorkoutPlan}</p>
        `;
      } else {
        // Redirect the user back to the personal-info page if no plan is available
        planElement.innerHTML = "<p>Error loading the generated workout plan. Please go back and try again.</p>";
        //window.location.href = '/result';
      }
    }

    // Toggle chatbot visibility when the icon is clicked
    const chatbotIcon = document.getElementById('chatbot-icon');
    if (chatbotIcon) {
      chatbotIcon.addEventListener('click', () => {
        chatbotContainer.classList.remove('collapsed');
        chatbotIcon.style.display = 'none';
      });
    }

    // Close the chatbot when the close button is clicked and show the icon again
    const chatbotClose = document.getElementById('chatbot-close');
    if (chatbotClose) {
      chatbotClose.addEventListener('click', () => {
        chatbotContainer.classList.add('collapsed');
        chatbotIcon.style.display = 'block';
      });
    }
  
    // Initialize the chatbot on the result page
    if (chatbotContent) {
      // Function to send a message to the API and receive a response
      async function sendMessageToAPI(message) {
        const response = await fetch('/api/chat', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ message }),
        });
        const data = await response.json();
        return data.response;
      }

      // Function to add a message to the chat UI
      function addMessageToChat(sender, message) {
        const messageElement = document.createElement('div');
        messageElement.classList.add(sender);
        messageElement.textContent = message;
        messages.appendChild(messageElement);
      }

      // Event listener for the message input field
      messageInput.addEventListener('keydown', async (e) => {
        if (e.key === 'Enter') {
          e.preventDefault();

          const message = messageInput.value.trim();
          if (message) {
            addMessageToChat('user', message);
            messageInput.value = '';

            const response = await sendMessageToAPI(message);
            addMessageToChat('bot', response);
          }
        }
      });
    }
      
  });
  