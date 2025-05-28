function drawWinLine(cells) {
    line = document.getElementById('line');

    // default settings
    line.style.transform = "none";

    // horizontal
    if (JSON.stringify(cells) == JSON.stringify([3,4,5])) {}
    else if (JSON.stringify(cells) == JSON.stringify([0, 1, 2])) {
        line.style.top = 60 +'px';
    }
    else if (JSON.stringify(cells) == JSON.stringify([6, 7, 8])) {
        line.style.top = 240 +'px';
    }
    // diagonal
    else if (JSON.stringify(cells) == JSON.stringify([0, 4, 8])) {
        line.style.transform = "rotate(225deg)";
    }
    else if (JSON.stringify(cells) == JSON.stringify([2, 4, 6])){
        line.style.transform = "rotate(135deg)";
    }   
    // vertical
    else {
        line.style.transform = "rotate(90deg)";
        if (JSON.stringify(cells) == JSON.stringify([0, 3, 6])) {
            line.style.left = -60 +'px';
        }
        else if (JSON.stringify(cells) == JSON.stringify([2, 5, 8])) {
            line.style.left = 125 +'px';
        }
    }
    
}

function trainAiWarning() {
    window.alert("AI not trained. Please train AI before playing.");
}