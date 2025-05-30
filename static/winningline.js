function drawWinLine(cells) {
    line = document.getElementById('line');
    // horizontal
    if (JSON.stringify(cells) == JSON.stringify([3,4,5])) {} // empty bc it's default settings
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