function encryptDES() {

    let text = document.getElementById("text").value;
    let key = document.getElementById("key").value;

    if (key.length !== 8) {
        alert("Key must be exactly 8 characters!");
        return;
    }

    let encrypted = CryptoJS.DES.encrypt(
        text,
        CryptoJS.enc.Utf8.parse(key),
        {
            mode: CryptoJS.mode.ECB,
            padding: CryptoJS.pad.Pkcs7
        }
    );

    document.getElementById("result").innerText =
        "Encrypted (Cipher Text):\n" + encrypted.toString();
}

function decryptDES() {

    let text = document.getElementById("text").value;
    let key = document.getElementById("key").value;

    if (key.length !== 8) {
        alert("Key must be exactly 8 characters!");
        return;
    }

    let decrypted = CryptoJS.DES.decrypt(
        text,
        CryptoJS.enc.Utf8.parse(key),
        {
            mode: CryptoJS.mode.ECB,
            padding: CryptoJS.pad.Pkcs7
        }
    );

    document.getElementById("result").innerText =
        "Decrypted (Plain Text):\n" +
        decrypted.toString(CryptoJS.enc.Utf8);
}
