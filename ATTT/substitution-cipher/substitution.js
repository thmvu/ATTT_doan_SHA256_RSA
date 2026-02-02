const alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
let key = "";

// ============================
// GENERATE RANDOM KEY
// ============================
function generateKey() {

    let chars = alphabet.split("");

    for (let i = chars.length - 1; i > 0; i--) {
        let j = Math.floor(Math.random() * (i + 1));
        [chars[i], chars[j]] = [chars[j], chars[i]];
    }

    key = chars.join("");

    document.getElementById("plainKey").innerText = alphabet;
    document.getElementById("cipherKey").innerText = key;
    document.getElementById("keyInput").value = key;

    alert("Random Key Generated!");
}



function applyKey() {

    let inputKey = document.getElementById("keyInput").value.toUpperCase();

    if (inputKey.length !== 26) {
        alert("Key must contain exactly 26 letters!");
        return;
    }

    let unique = new Set(inputKey);

    if (unique.size !== 26) {
        alert("Key must not contain duplicate letters!");
        return;
    }

    key = inputKey;

    document.getElementById("plainKey").innerText = alphabet;
    document.getElementById("cipherKey").innerText = key;

    alert("Key Applied Successfully!");
}



function encrypt() {

    if (key === "") {
        alert("Generate or apply key first!");
        return;
    }

    let text = document.getElementById("plain").value.toUpperCase();
    let result = "";

    for (let c of text) {

        if (alphabet.includes(c)) {
            let index = alphabet.indexOf(c);
            result += key[index];
        } else {
            result += c;
        }
    }

    document.getElementById("result").value = result;
}


// ============================
// DECRYPT
// ============================
function decrypt() {

    if (key === "") {
        alert("Generate or apply key first!");
        return;
    }

    let text = document.getElementById("plain").value.toUpperCase();
    let result = "";

    for (let c of text) {

        if (key.includes(c)) {
            let index = key.indexOf(c);
            result += alphabet[index];
        } else {
            result += c;
        }
    }

    document.getElementById("result").value = result;
}
