const aiInputForm = document.getElementById('ai-inputs');

function sendCheckboxState() {
  // retrieve checkbox information
  checkbox = document.getElementById('show_qvalues');

  fetch('/update_qvalues', {
    // Run function
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ qvalues: checkbox.checked })
  }).then(response => {
    if (response.ok) {
      // Then fetch the updated board
      return fetch('/get_board');
    } else {
      throw new Error("Failed to update qvalues");
    }
  }).then(response => response.json())
    .then(data => {
      // Replace the board HTML
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
aiInputForm.addEventListener('submit', submitAiInputs);

function submitAiInputs(event) {
  const inputs = document.querySelectorAll('#ai-inputs input');
  let isNumb = true;

  // last input must be integer
  const episodes = inputs[3].value;
  if (!Number.isInteger(Number(episodes)) || episodes < 0) {
    isNumb = false;
    inputs[3].style.borderColor = 'red';
    window.alert("Input must be a positive integer.");
  }
  else {
    inputs[3].style.borderColor ='#2C1E1B';
  }

  // other inputs must be between 0 and 1
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

// disable buttons while page is loading
window.addEventListener('beforeunload', () => {
  document.querySelectorAll('button').forEach(btn => {
    btn.disabled = true;
  });
});