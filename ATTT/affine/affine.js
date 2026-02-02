function encrypt() {
    let text = document.getElementById("inputText").value;
    let a = parseInt(document.getElementById("a").value);
    let b = parseInt(document.getElementById("b").value);

    if (isNaN(a) || isNaN(b)) {
        alert("Please enter a and b");
        return;
    }

    let result = "";

    for (let char of text) {
        if(char >='A' && char <= 'Z') {
            let x = char.charCodeAt(0) - 65;
            let y = (a * x + b) % 26;
            result += String.fromCharCode(y + 65);
        } else if (char >= 'a' && char <= 'z') {
            let x = char.charCodeAt(0) - 97;
            let y = (a * x + b) % 26;
            result += String.fromCharCode(y + 97); 
        }
        else {
            result += char;
        }
    }

    document.getElementById("outputText").value = result;
}
function decrypt() {
    let text = document.getElementById("inputText").value;
    let a = parseInt(document.getElementById("a").value);
    let b = parseInt(document.getElementById("b").value);
    if (isNaN(a) || isNaN(b)) {
        alert("Please enter a and b");
        return;
    }
    function modInverse(a, m) {
        a = a % m;
        for (let x = 1; x < m; x++) {
            if ((a * x) % m === 1) {
                return x;
            }
        }
        return null;
    }
    let a_inv = modInverse(a, 26);
    if (a_inv === null) {
        alert("Multiplicative inverse for a does not exist. Decryption not possible.");
        return;
    }
    let result = "";

    for (let char of text) {
        if (char >= 'A' && char <= 'Z') {
            let y = char.charCodeAt(0) - 65;
            let x = (a_inv * (y - b + 26)) % 26;
            result += String.fromCharCode(x + 65);
        } else if (char >= 'a' && char <= 'z') {
            let y = char.charCodeAt(0) - 97;
            let x = (a_inv * (y - b + 26)) % 26;
            result += String.fromCharCode(x + 97); 
        }
        else {
            result += char;
        }
    }
    document.getElementById("outputText").value = result;       
}
document.getElementById("fileInput").addEventListener("change", function () {
    let file = this.files[0];
    if (!file) return;

    let reader = new FileReader();
    reader.onload = function (e) {
        document.getElementById("inputText").value = e.target.result;
    };
    reader.readAsText(file);
}); 