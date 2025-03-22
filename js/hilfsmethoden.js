export function evaluateExpression(expression) {
    /**
     * Diese Funktion wertet einen mathematischen Ausdruck in Stringform von links nach rechts aus.
     *
     * @param {string} expression - Der String mit dem Rechenausdruck.
     * @returns {[number, boolean, boolean, boolean]} - result (int Value), resultIsInt, alwaysInteger, alwaysPositive
     */

    let tokens = [];
    let currentToken = "";

    //console.log("Expression to evaluate",expression);

    // Schritt 1: Token aus dem Ausdruck extrahieren
    for (let char of expression) {
        if (!isNaN(char)) {
            currentToken += char;
        } else {
            if (currentToken) {
                tokens.push(currentToken);
            }
            tokens.push(char);
            currentToken = "";
        }
    }
    if (currentToken) {
        tokens.push(currentToken);
    }

    // Schritt 2: Ausdruck auswerten
    let result = parseFloat(tokens[0]); // Der erste Wert ist immer eine Zahl
    let pureInteger = true;
    let alwaysPositive = result > 0;
    let operator = null;

    for (let token of tokens.slice(1)) {
        if ("+-*/÷x".includes(token)) {
            operator = token;
        } else {
            let num = parseInt(token);
            if (operator === "+") {
                result += num;
            } else if (operator === "-") {
                result -= num;
            } else if (operator === "*" || operator === "x") {
                result *= num;
            } else if (operator === "/" || operator === "÷") {
                if (num === 0) {
                    throw new Error("Division durch Null ist nicht erlaubt.");
                }
                result /= num;
            }
            pureInteger &&= Number.isInteger(result);
            alwaysPositive &&= result > 0;
        }
    }

    return [Math.floor(result), Number.isInteger(result), pureInteger, alwaysPositive];
}

export function bestimmeErgebnisse(ziffern, rechenzeichen) {
    /**
     * Diese Funktion bestimmt die 6 Ergebnisse der Zeilen und Spalten eines Rechenquadrates.
     *
     * @param {string} ziffern - Der String mit den neuen Ziffern des Quadrates (1. Zeile, 2. Zeile, 3. Zeile).
     * @param {string} rechenzeichen - Der String mit den Rechenzeichen: 
     *        - Die ersten beiden sind die Operatoren der ersten Zeile,
     *        - Die nächsten drei sind die Operatoren der ersten, zweiten und dritten Spalte.
     * @returns {[number, number, number, number, number, number]} - Ergebnisse der 3 Zeilen und 3 Spalten.
     */

    function berechne(a, op1, b, op2, c) {
        return evaluateExpression(`${a}${op1}${b}${op2}${c}`)[0]; // Nur das Ergebnis zurückgeben
    }

    // Zahlen extrahieren
    let zahlen = ziffern.split("").map(Number);

    // Operatoren extrahieren
    let op = rechenzeichen.split("");

    // Zeilen berechnen
    let erg1Zeile = berechne(zahlen[0], op[0], zahlen[1], op[1], zahlen[2]);
    let erg2Zeile = berechne(zahlen[3], op[5], zahlen[4], op[6], zahlen[5]);
    let erg3Zeile = berechne(zahlen[6], op[10], zahlen[7], op[11], zahlen[8]);

    // Spalten berechnen
    let erg1Spalte = berechne(zahlen[0], op[2], zahlen[3], op[7], zahlen[6]);
    let erg2Spalte = berechne(zahlen[1], op[3], zahlen[4], op[8], zahlen[7]);
    let erg3Spalte = berechne(zahlen[2], op[4], zahlen[5], op[9], zahlen[8]);

    return [erg1Zeile, erg2Zeile, erg3Zeile, erg1Spalte, erg2Spalte, erg3Spalte];
}

