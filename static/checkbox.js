function sendCheckboxState(checkbox) {
  fetch('/update_qvalues', {
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
