function drawWinLine(cells) {
    line = document.getElementById('line');

    // horizontal
    if (JSON.stringify(cells) == JSON.stringify([3,4,5])) {
      //idk why this was empty dog
      line.style.top = -130 +'px'
    }
    else if (JSON.stringify(cells) == JSON.stringify([0, 1, 2])) {
        line.style.top = 50 +'px';
    }
    else if (JSON.stringify(cells) == JSON.stringify([6, 7, 8])) {
        line.style.top = 230 +'px';
    }
    // diagonal
    else if (JSON.stringify(cells) == JSON.stringify([0, 4, 8])) {
        line.style.transform = "rotate(225deg)";
        line.style.width = '110%';
        line.style.top = 138 + 'px';
        line.style.left = -14 + 'px';
    }
    else if (JSON.stringify(cells) == JSON.stringify([2, 4, 6])){
        line.style.transform = "rotate(135deg)";
        line.style.width = '110%';
        line.style.top = 138 + 'px';
        line.style.left = -14 + 'px';
    }   
    // vertical
    else {
        line.style.transform = "rotate(90deg)";
        if (JSON.stringify(cells) == JSON.stringify([0, 3, 6])) {
            line.style.left = -75 +'px';
        }
        else if (JSON.stringify(cells) == JSON.stringify([2, 5, 8])) {
            line.style.left = 107 +'px';
        }
    }
    
}

function trainAiWarning() {
    window.alert("AI not trained. Please train AI before playing.");
}

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
