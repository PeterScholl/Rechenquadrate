import { evaluateExpression, bestimmeErgebnisse } from './hilfsmethoden.js';

let grid; // = document.getElementById("grid");
let layout = [
    ['n', 'o', 'n', 'o', 'n', '=', 'r'],
    ['o', 'g', 'o', 'g', 'o', 'g', 'b'],
    ['n', 'o', 'n', 'o', 'n', '=', 'r'],
    ['o', 'g', 'o', 'g', 'o', 'g', 'b'],
    ['n', 'o', 'n', 'o', 'n', '=', 'r'],
    ['=', 'g', '=', 'g', '=', 'g', 'b'],
    ['r', 'b', 'r', 'b', 'r', 'b', 'b']
];
let results = [20, 40, 76, 178, 2, 1];
let operators = "/+-*+-++/+++";

let inputValues = Array(9).fill("");
let numberCells = [];
let focusedIndex = 0;

function updateGrid() {
    //console.log("Updating grid. Focused index:", focusedIndex);
    grid.innerHTML = "";
    numberCells = [];
    let nr_idx = 0;
    let res_idx = 0;
    let op_idx = 0;
    layout.forEach(row => {
        row.forEach(cell => {
            let div = document.createElement("div");
            div.classList.add("cell");

            if (cell === 'n') {
                let value = inputValues[nr_idx] || "";
                div.dataset.index = nr_idx;
                numberCells.push(div);
                //div.addEventListener("click", () => setFocus(index));
                div.addEventListener("click", ((idx) => () => setFocus(idx))(nr_idx));

                if (nr_idx === focusedIndex) {
                    div.classList.add("focused");
                }

                if (value.length === 1) {
                    div.textContent = value;
                } else if (value.length > 1) {
                    let smallGrid = document.createElement("div");
                    smallGrid.classList.add("small-grid");
                    for (let i = 1; i <= 9; i++) {
                        let smallCell = document.createElement("div");
                        smallCell.textContent = value.includes(i.toString()) ? i : "";
                        smallGrid.appendChild(smallCell);
                    }
                    div.appendChild(smallGrid);
                }
                nr_idx++;
            } else if (cell === 'r') {
                div.textContent = results[res_idx] !== undefined ? results[res_idx] : '?';
                res_idx++;
            } else if (cell === 'g') {
                div.classList.add("gray-cell");
            } else if (cell === 'b') {
                div.classList.add("black-cell");
            } else if (cell === 'o') {
                div.textContent = operators[op_idx] !== undefined ? operators[op_idx] : '?';
                op_idx++;
            } else {
                div.textContent = cell;
            }
            grid.appendChild(div);
        });
    });
}

function setFocus(index) {
    //console.log("Setting focus to:", index);
    focusedIndex = index;
    updateGrid();
}

document.addEventListener("keydown", (event) => {
    if (focusedIndex === null) return;

    let currentValues = inputValues[focusedIndex] || "";

    if (event.key >= '1' && event.key <= '9') {
        if (currentValues.includes(event.key)) {
            inputValues[focusedIndex] = currentValues.replace(event.key, "");
        } else {
            inputValues[focusedIndex] += event.key;
        }
    } else if (event.key === "Backspace") {
        inputValues[focusedIndex] = "";
    } else if (event.key === "ArrowUp") {
        event.preventDefault(); // Verhindert das Scrollen des Fensters
        if (focusedIndex>2) setFocus(focusedIndex-3);
    } else if (event.key === "ArrowDown") {
        event.preventDefault(); // Verhindert das Scrollen des Fensters
        if (focusedIndex<6) setFocus(focusedIndex+3);
    } else if (event.key === "ArrowRight") {
        if (focusedIndex%3!=2) setFocus(focusedIndex+1);
    } else if (event.key === "ArrowLeft") {
        if (focusedIndex%3!=0) setFocus(focusedIndex-1);
    } else {
        console.log("Key pressed:", event.key);
    }
    updateGrid();
});

function tests() {
    console.log(evaluateExpression("10+5*2"));
    console.log(bestimmeErgebnisse("123456789","++++xx-+--÷x"));
}

window.onload = function () {
    grid = document.getElementById("grid");
    tests();
    operators="++++xx-+--÷x";
    results=[19,49,6,15,13,32]
    results=bestimmeErgebnisse("487965213",operators);
    updateGrid();
};
