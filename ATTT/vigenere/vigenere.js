function vigenereEncrypt(plaintext, key) {
    plaintext = plaintext.toUpperCase().replace(/[^A-Z]/g, '');
    key = key.toUpperCase().replace(/[^A-Z]/g, '');

    let ciphertext = '';
    let keyIndex = 0;

    for (let i = 0; i < plaintext.length; i++) {
        const shift = key.charCodeAt(keyIndex % key.length) - 65;
        const charCode = plaintext.charCodeAt(i) - 65;
        ciphertext += String.fromCharCode((charCode + shift) % 26 + 65);
        keyIndex++;
    }
    return ciphertext;
}

function vigenereDecrypt(ciphertext, key) {
    ciphertext = ciphertext.toUpperCase().replace(/[^A-Z]/g, '');
    key = key.toUpperCase().replace(/[^A-Z]/g, '');

    let plaintext = '';
    let keyIndex = 0;

    for (let i = 0; i < ciphertext.length; i++) {
        const shift = key.charCodeAt(keyIndex % key.length) - 65;
        const charCode = ciphertext.charCodeAt(i) - 65;
        plaintext += String.fromCharCode((charCode - shift + 26) % 26 + 65);
        keyIndex++;
    }
    return plaintext;
}

// ====== KẾT NỐI UI ======

function maHoa() {
    const text = document.getElementById("inputText").value;
    const key = document.getElementById("key").value;

    if (!text || !key) {
        alert("Vui lòng nhập văn bản và khóa!");
        return;
    }

    document.getElementById("outputText").value =
        vigenereEncrypt(text, key);
}

function giaiMa() {
    const text = document.getElementById("inputText").value;
    const key = document.getElementById("key").value;

    if (!text || !key) {
        alert("Vui lòng nhập văn bản và khóa!");
        return;
    }

    document.getElementById("outputText").value =
        vigenereDecrypt(text, key);
}

function taiFile() {
    const content = document.getElementById("outputText").value;
    const blob = new Blob([content], { type: "text/plain" });
    const a = document.createElement("a");

    a.href = URL.createObjectURL(blob);
    a.download = "vigenere_result.txt";
    a.click();
}
