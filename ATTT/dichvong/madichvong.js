function xuLyCaesar(text, shift) {
    let result = "";
    shift = shift % 26;

    for (let c of text) {
        if (c >= 'a' && c <= 'z') {
            result += String.fromCharCode(
                (c.charCodeAt(0) - 97 + shift + 26) % 26 + 97
            );
        }
        else if (c >= 'A' && c <= 'Z') {
            result += String.fromCharCode(
                (c.charCodeAt(0) - 65 + shift + 26) % 26 + 65
            );
        }
        else {
            result += c;
        }
    }
    return result;
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

function maHoa() {
    let text = document.getElementById("inputText").value;
    let shift = parseInt(document.getElementById("shift").value);
    document.getElementById("outputText").value = xuLyCaesar(text, shift);
}

function giaiMa() {
    let text = document.getElementById("inputText").value;
    let shift = parseInt(document.getElementById("shift").value);
    document.getElementById("outputText").value = xuLyCaesar(text, -shift);
}
function taiFile() {
    let blob = new Blob([outputText.value], { type: "text/plain" });
    let a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = "ketqua.txt";
    a.click();
}
