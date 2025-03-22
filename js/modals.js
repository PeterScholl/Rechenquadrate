import { setFocusedIndex, inputValues, loadBookOptions, updateGrid } from './rechenquadrat.js';

export function showMessageModal(message, color = "white", duration = 10000, wide = false) {
    let modal = document.getElementById("messageModal");
    let overlay = document.getElementById("messageModal-overlay");

    if (!modal) return; // Falls das Modal nicht existiert, nichts tun
    let newModal = modal.cloneNode(true);
    modal.parentNode.replaceChild(newModal, modal);
    modal = newModal; // Neue Referenz setzen
    let newOverlay = overlay.cloneNode(true);
    overlay.parentNode.replaceChild(newOverlay, overlay);
    overlay = newOverlay; // Neue Referenz setzen

    if (wide) {
        modal.classList.add("messageModal-wide");
    } else {
        modal.classList.remove("messageModal-wide");
    }


    modal.textContent = message;
    modal.style.background = color;
    modal.style.display = "block";
    modal.style.display = "block";
    overlay.style.display = "block";
    setTimeout(() => {
        modal.style.opacity = "1";
    }, 10);

    // Schließen bei Klick
    modal.onclick = closeMessageModal;
    overlay.onclick = closeMessageModal;

    setTimeout(closeMessageModal, duration);
}

export function closeMessageModal() {
    let modal = document.getElementById("messageModal");
    let overlay = document.getElementById("messageModal-overlay");

    if (modal) {
        modal.style.opacity = "0";
        setTimeout(() => {
            modal.style.display = "none";
            overlay.style.display = "none";
        }, 500);
    }
}
// Funktion zum Schließen des Modals
export function closePuzzleModal() {
    document.getElementById('choose-puzzle-modal').style.display = 'none';
}
// Funktion zum Öffnen des Modals
export function openPuzzleModal() {
    document.getElementById('choose-puzzle-modal').style.display = 'block';
    loadBookOptions();
}
export function handleTouchModal(index, event) {
    console.log("Touch erkannt");
    event.preventDefault(); // Verhindert, dass der Touch-Event weitergereicht wird

    let modal = document.getElementById("messageModal");
    let newModal = modal.cloneNode(true);
    modal.parentNode.replaceChild(newModal, modal);
    modal = newModal; // Neue Referenz setzen
    let overlay = document.getElementById("messageModal-overlay");
    let newOverlay = overlay.cloneNode(true);
    overlay.parentNode.replaceChild(newOverlay, overlay);
    overlay = newOverlay; // Neue Referenz setzen

    modal.innerHTML = "";
    modal.removeAttribute("style"); // Setzt alle inline-Stile zurück
    modal.style.display = "block";
    modal.style.opacity = "1";
    overlay.removeAttribute("style"); // Setzt alle inline-Stile zurück
    overlay.style.display = "block";

    let grid = document.createElement("div");
    grid.style.display = "grid";
    grid.style.gridTemplateColumns = "repeat(3, 1fr)";
    grid.style.gap = "10px";
    grid.style.padding = "10px";

    let selectedValues = new Set(inputValues[index]?.split("") || []);

    for (let i = 1; i <= 9; i++) {
        let btn = document.createElement("div");
        btn.textContent = i;
        btn.style.padding = "15px";
        btn.style.textAlign = "center";
        btn.style.border = "1px solid black";
        btn.style.cursor = "pointer";
        btn.style.background = selectedValues.has(i.toString()) ? "yellow" : "white";

        btn.addEventListener("click", () => {
            if (selectedValues.has(i.toString())) {
                selectedValues.delete(i.toString());
                btn.style.background = "white";
            } else {
                selectedValues.add(i.toString());
                btn.style.background = "yellow";
            }
        });
        grid.appendChild(btn);
    }

    let closeButton = document.createElement("button");
    closeButton.textContent = "OK";
    closeButton.style.marginTop = "10px";
    closeButton.addEventListener("click", (event) => closeHandleTouchModal(index, selectedValues, event));

    modal.appendChild(grid);
    modal.appendChild(closeButton);

    overlay.addEventListener("click", (event) => closeHandleTouchModal(index, selectedValues, event));
}
export function closeHandleTouchModal(index, selectedValues, event) {
    event.preventDefault();
    console.log(event, index, selectedValues);
    event.stopPropagation(); // Stoppt das Event-Bubbling

    inputValues[index] = Array.from(selectedValues).sort().join("");
    closeMessageModal();
    setFocusedIndex(index);
    updateGrid();
}

export function showAnleitung() {
    const text = `Es werden alle Ziffern von 1 bis 9 so eingetragen, 
    dass die Rechnung schlüssig wird. Keine Zahl darf zweimal vorkommen. 
    Es gilt nicht die Regel "Punkt-vor Strichrechnung", sondern es wird 
    von oben nach unten bzw. von links nach rechts gerechnet`;
    showMessageModal(text, "white", 20000, true);
}

