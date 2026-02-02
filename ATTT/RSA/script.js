let publicKey = {};
let privateKey = {};
let encryptedData = [];

/* ================= PRIME FUNCTIONS ================= */

// Kiểm tra số nguyên tố
function isPrime(n) {
    if (n < 2) return false;

    for (let i = 2; i * i <= n; i++) {
        if (n % i === 0) return false;
    }
    return true;
}

// Sinh số nguyên tố ngẫu nhiên
function randomPrime(min, max) {
    let num;
    do {
        num = Math.floor(Math.random() * (max - min)) + min;
    } while (!isPrime(num));

    return num;
}

/* ================= MATH FUNCTIONS ================= */

function gcd(a, b) {
    if (b === 0) return a;
    return gcd(b, a % b);
}

// Tìm nghịch đảo modular
function modInverse(e, phi) {
    for (let d = 1; d < phi; d++) {
        if ((e * d) % phi === 1) {
            return d;
        }
    }
    return -1;
}

// Lũy thừa modulo nhanh
function modPow(base, exp, mod) {
    let result = 1;
    base %= mod;

    while (exp > 0) {
        if (exp % 2 === 1)
            result = (result * base) % mod;

        exp = Math.floor(exp / 2);
        base = (base * base) % mod;
    }

    return result;
}

/* ================= RSA KEY GENERATION ================= */

function generateKeys() {

    // Sinh prime 2-3 chữ số (demo)
    let p = randomPrime(100, 300);
    let q = randomPrime(100, 300);

    let n = p * q;
    let phi = (p - 1) * (q - 1);

    let e = 17;

    while (gcd(e, phi) !== 1) {
        e++;
    }

    let d = modInverse(e, phi);

    publicKey = { n, e };
    privateKey = { n, d };

    document.getElementById("pVal").innerText = p;
    document.getElementById("qVal").innerText = q;

    document.getElementById("publicKey").innerText =
        `n = ${n}\ne = ${e}`;

    document.getElementById("privateKey").innerText =
        `n = ${n}\nd = ${d}`;

    encryptedData = [];
}

/* ================= ENCRYPT ================= */

function encrypt() {

    let text = document.getElementById("plainText").value;

    if (!publicKey.n) {
        alert("Hãy tạo khóa RSA trước!");
        return;
    }

    encryptedData = [];

    for (let i = 0; i < text.length; i++) {

        let charCode = text.charCodeAt(i);

        let cipher = modPow(charCode, publicKey.e, publicKey.n);

        encryptedData.push(cipher);
    }

    document.getElementById("cipherText").innerText =
        encryptedData.join(" ");
}

/* ================= DECRYPT ================= */

function decrypt() {

    if (!privateKey.n) {
        alert("Chưa có private key!");
        return;
    }

    let result = "";

    for (let i = 0; i < encryptedData.length; i++) {

        let charCode =
            modPow(encryptedData[i], privateKey.d, privateKey.n);

        result += String.fromCharCode(charCode);
    }

    document.getElementById("decryptedText").innerText =
        result;
}
