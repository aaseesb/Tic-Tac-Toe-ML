const form = document.getElementById('ai-inputs');
const loader = document.querySelector('.loading-screen');
const text = document.querySelector('.params')

function sendCheckboxState() {
  checkbox = document.getElementById('show_qvalues');

  fetch('/update_qvalues', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ qvalues: checkbox.checked })
  }).then(response => {
    if (response.ok) {
      return fetch('/get_board');
    } else {
      throw new Error("Failed to update qvalues");
    }
  }).then(response => response.json())
    .then(data => {
      document.getElementById('board-container').innerHTML = data.html;
    })
    .catch(error => {
      console.error("Error:", error);
    });
}

function trainAiWarning() {
  window.alert("AI not trained. Please train AI before playing.");
}

// check and function for ai input submission, needed to check if inputs are numbers
form.addEventListener('submit', submitAiInputs);

function submitAiInputs(event) {
  const inputs = document.querySelectorAll('#ai-inputs input');
  let isNumb = true;

  const episodes = inputs[3].value;
  if (!Number.isInteger(Number(episodes)) || episodes < 0) {
    isNumb = false;
    inputs[3].style.borderColor = 'red';
    window.alert("Input must be a positive integer.");
  }
  else {
    inputs[3].style.borderColor ='#2C1E1B';
  }

  [...inputs].slice(0,3).forEach(input => {
    if (isNaN(input.value) || input.value < 0 || input.value > 1) {
      isNumb = false;
      input.style.borderColor = 'red';
      window.alert("Input must be between 0 and 1.");
    }
    else {
      input.style.borderColor ='#2C1E1B';
    }
  });

  if (!isNumb) {
    event.preventDefault();
  }
}

document.getElementById('resetForm').addEventListener('submit', (event) => {
    sendCheckboxState();
});

// disable buttons while page is loading
window.addEventListener('beforeunload', () => {
  document.querySelectorAll('button').forEach(btn => {
    btn.disabled = true;
  });
});

window.addEventListener('load', () => {
  // ensure checkbox state is retained on load
  if (!gameOver && document.getElementById('show_qvalues').checked) {
    sendCheckboxState();
  }
  // hide text when loading screen appears
  
});

// hide parameters and show loading screen every time parameters are submitted
document.addEventListener('DOMContentLoaded', () => {
    if (form && loader) {
        form.addEventListener('submit', (e) => {
            loader.style.display = 'block';
            text.classList.add('hidden');
        });
    }
});