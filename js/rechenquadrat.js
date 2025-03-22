import { evaluateExpression, bestimmeErgebnisse } from './hilfsmethoden.js';
import { closePuzzleModal, handleTouchModal, openPuzzleModal, showMessageModal, showAnleitung } from './modals.js';

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
let operators = "++++xx-+--÷x";
let solutions = "487965213";
let results = [19, 49, 6, 15, 13, 32];
let checked = false;
let running = true;

export let inputValues = Array(9).fill("");
let numberCells = [];
let focusedIndex = 0;

export function setFocusedIndex(idx) {
    focusedIndex = idx;
}

export function updateGrid() {
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
                div.addEventListener("touchstart", ((idx) => (event) => handleTouchModal(idx, event))(nr_idx));

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
    checkSolution();
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
        if (focusedIndex > 2) setFocus(focusedIndex - 3);
    } else if (event.key === "ArrowDown") {
        event.preventDefault(); // Verhindert das Scrollen des Fensters
        if (focusedIndex < 6) setFocus(focusedIndex + 3);
    } else if (event.key === "ArrowRight") {
        if (focusedIndex % 3 != 2) setFocus(focusedIndex + 1);
    } else if (event.key === "ArrowLeft") {
        if (focusedIndex % 3 != 0) setFocus(focusedIndex - 1);
    } else if (event.key === "o") {
        openPuzzleModal();
    } else if (event.key === "c") {
        clearFields();
    } else if (event.key === "a") {
        uncoverRandomField();
    } else if (event.key === "h") {
        showAnleitung();
    } else {
        console.log("Key pressed:", event.key);
    }
    updateGrid();
});

function tests() {
    console.log(evaluateExpression("10+5*2"));
    console.log(bestimmeErgebnisse("123456789", "++++xx-+--÷x"));
}

function toggleMenu() {
    let menu = document.getElementById("menu");
    menu.style.display = (menu.style.display === "flex") ? "none" : "flex";
}

function initMenu() {
    const menu = document.getElementById("menu");
    const menuItems = [
        { text: "Anleitung (h)", action: showAnleitung },
        { text: "Feld aufdecken (a)", action: uncoverRandomField },
        //{ text: "Prüfen", action: tests },
        //{ text: "Einstellungen", action: tests },
        { text: "Puzzle leeren (c)", action: clearFields},
        { text: "Puzzle wählen (o)", action: openPuzzleModal }
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

export function loadBookOptions() {
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

function uncoverRandomField() {
    let candidates = [];

    inputValues.forEach((value, idx) => {
        if (value.length !== 1) {
            candidates.push(idx);
        }
    });

    if (candidates.length > 0) {
        let randomIdx = candidates[Math.floor(Math.random() * candidates.length)];
        inputValues[randomIdx] = solutions[randomIdx]; // Richtige Ziffer eintragen
        updateGrid(); // Grid aktualisieren


        // Zelle hervorheben
        let cell = document.querySelector(`.cell[data-index='${randomIdx}']`);
        if (cell) {
            cell.style.transition = "background-color 2s ease-in-out";
            cell.style.backgroundColor = "yellow";
            setTimeout(() => {
                cell.style.backgroundColor = ""; // Langsames Ausfaden
            }, 100);
        }
    }
}

function clearFields() {
    inputValues = Array(9).fill("");
    updateGrid();
}

function checkSolution() {
    if (!inputValues.every(val => val.length === 1)) {
        checked = false;
        return; // Nur prüfen, wenn alle Felder eine Ziffer enthalten
    }
    if (checked) return; //Wurde schon geprüft
    checked = true;

    let incorrectCount = 0;
    let allCorrect = true;

    for (let idx = 0; idx < 9; idx++) {
        let userInput = inputValues[idx] || "";
        let correctValue = solutions[idx];

        if (userInput !== correctValue) {
            incorrectCount++;
            allCorrect = false;
        }
    }

    if (allCorrect) {
        showMessageModal("Glückwunsch! Alle Lösungen sind richtig.", "green");
    } else {
        showMessageModal(`Es gibt ${incorrectCount} falsche Eingabe(n).`, "red");
    }

    if (allCorrect) {
        running = false;
    }
}


function selectPuzzle() {
    let book = document.getElementById("book-select").value;
    let puzzleIndex = document.getElementById("puzzle-select").value;
    let puzzle = puzzles[book][puzzleIndex];

    console.log("Puzzle",puzzle,"Ziffern", puzzle.numbers);
    solutions = puzzle.numbers;
    operators = puzzle.operators;
    results = bestimmeErgebnisse(solutions, operators);
    inputValues = Array(9).fill("");
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
    operators = "++++xx-+--÷x";
    solutions = "487965213";
    results = [19, 49, 6, 15, 13, 32];
    results = bestimmeErgebnisse(solutions, operators);
    updateGrid();
};

