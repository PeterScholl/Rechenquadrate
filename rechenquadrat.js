import { evaluateExpression, bestimmeErgebnisse } from './hilfsmethoden.js';

let puzzles = {};
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

function toggleMenu() {
    let menu = document.getElementById("menu");
    menu.style.display = (menu.style.display === "flex") ? "none" : "flex";
}

function initMenu() {
    const menu = document.getElementById("menu");
    const menuItems = [
        { text: "Anleitung", action: tests },
        { text: "Feld aufdecken", action: tests },
        { text: "Prüfen", action: tests },
        { text: "Einstellungen", action: tests },
        { text: "Puzzle wählen", action: openPuzzleModal}
    ];

    // Bestehende Menüeinträge leeren und neu befüllen
    menu.innerHTML = "";
    menuItems.forEach(item => {
        let menuItem = document.createElement("div");
        menuItem.classList.add("menu-item");
        menuItem.textContent = item.text;
        menuItem.onclick = () => {
            item.action();  // Aktion ausführen
            toggleMenu();   // Menü schließen
        };
        menu.appendChild(menuItem);
    });
}

// Funktion zum Laden der Rätsel aus der JSON-Datei
async function loadPuzzles() {
    try {
        let response = await fetch("library.json");
        puzzles = await response.json();
        //console.log("Geladene Puzzles:", puzzles);  // Debugging
    } catch (error) {
        console.error("Fehler beim Laden der Rätsel:", error);
    }
}

// Funktion zum Öffnen des Modals
function openPuzzleModal() {
    document.getElementById('choose-puzzle-modal').style.display = 'block';
    loadBookOptions();
}

// Funktion zum Schließen des Modals
function closePuzzleModal() {
    document.getElementById('choose-puzzle-modal').style.display = 'none';
}

function loadBookOptions() {
    let bookSelect = document.getElementById("book-select");
    bookSelect.innerHTML = "";  
    
    for (let book in puzzles) {
        let option = document.createElement("option");
        option.value = book;
        option.textContent = book;
        bookSelect.appendChild(option);
    }
    updatePuzzleList();  
}

function updatePuzzleList() {
    let book = document.getElementById("book-select").value;
    let puzzleSelect = document.getElementById("puzzle-select");
    puzzleSelect.innerHTML = "";  

    //console.log("Book",book);
    puzzles[book].forEach((_, index) => {
        let option = document.createElement("option");
        option.value = index;
        option.textContent = `Rätsel ${index + 1}`;
        puzzleSelect.appendChild(option);
    });
}

function selectPuzzle() {
    let book = document.getElementById("book-select").value;
    let puzzleIndex = document.getElementById("puzzle-select").value;
    let puzzle = puzzles[book][puzzleIndex];

    //console.log("Puzzle",puzzle,"Ziffern", puzzle.numbers);
    operators = puzzle.operators;
    results = bestimmeErgebnisse(puzzle.numbers,operators);
    closePuzzleModal();
    updateGrid();
}

loadPuzzles();
window.onload = function () {
    //toggle-Menu im HTML verfügbar machen, obwohl module
    window.toggleMenu = toggleMenu;
    window.closePuzzleModal = closePuzzleModal;
    window.updatePuzzleList = updatePuzzleList;
    window.selectPuzzle = selectPuzzle;
    initMenu();
    grid = document.getElementById("grid");
    tests();
    operators="++++xx-+--÷x";
    results=[19,49,6,15,13,32]
    results=bestimmeErgebnisse("487965213",operators);
    updateGrid();
    
};
