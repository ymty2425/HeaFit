document.addEventListener('DOMContentLoaded', () => {
    const personalInfoForm = document.getElementById('personal-info-form');
    const planElement = document.getElementById('plan');
    const chatbotContainer = document.getElementById('chatbot-container');
  
    // Personal info form handling
    if (personalInfoForm) {
      personalInfoForm.addEventListener('submit', async (event) => {
        event.preventDefault();
  
        const formData = new FormData(personalInfoForm);
        const data = Object.fromEntries(formData.entries());
  
        const response = await fetch('/api/generate-plan', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(data),
        });
  
        if (response.ok) {
          const plan = await response.json();
          localStorage.setItem('plan', JSON.stringify(plan));
          window.location.href = '/result';
        } else {
          // Handle error, e.g., display an error message
        }
      });
    }
  
    // Display the workout and nutrition plan on the result page
    if (planElement) {
      const plan = JSON.parse(localStorage.getItem('plan'));
      localStorage.removeItem('plan');
  
      if (plan) {
        // Display the plan
        planElement.innerHTML = `
          <h2>Workout Plan</h2>
          <p>${plan.workout}</p>
          <h2>Nutrition Plan</h2>
          <p>${plan.nutrition}</p>
        `;
      } else {
        // Redirect the user back to the personal-info page if no plan is available
        window.location.href = '/personal-info';
      }
    }
  
    // Initialize the chatbot on the result page
    if (chatbotContainer) {
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
          
          // Add this function to handle sending and receiving messages in the chatbot UI
          function addMessageToChat(sender, message) {
            const messageElement = document.createElement('div');
            messageElement.classList.add(sender);
            messageElement.textContent = message;
            chatbotContainer.appendChild(messageElement);
          }
          
          // Add an event listener for the chatbot input form
          const chatbotForm = document.createElement('form');
          chatbotForm.innerHTML = `
            <input type="text" id="chatbot-input" placeholder="Type your message...">
            <button type="submit">Send</button>
          `;
          chatbotForm.addEventListener('submit', async (e) => {
            e.preventDefault();
          
            const input = chatbotForm.querySelector('#chatbot-input');
            const message = input.value.trim();
          
            if (message) {
              addMessageToChat('user', message);
              input.value = '';
          
              const response = await sendMessageToAPI(message);
              addMessageToChat('bot', response);
            }
          });
          
          chatbotContainer.appendChild(chatbotForm);
      }
      
  });
  