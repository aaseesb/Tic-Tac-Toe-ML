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

// when reset button is clicked, check for q value box before resetting
function resetGame() {
  sendCheckboxState();
  document.getElementById("resetForm").submit();
}

function trainAiWarning() {
    window.alert("AI not trained. Please train AI before playing.");
}