// script.js
document.getElementById('analyzeButton').addEventListener('click', function() {
    const text = document.getElementById('textInput').value;
    if (text.trim() === "") {
        alert("Veuillez entrer un texte à analyser.");
        return;
    }

    // Simuler une analyse (remplacez par une vraie analyse si nécessaire)
    const result = analyzeText(text);
    displayResult(result);
    addToHistory(text, result);
});

function analyzeText(text) {
    // Simuler une analyse avec un résultat aléatoire
    const isTrue = Math.random() > 0.5;
    const confidence = (Math.random() * 100).toFixed(2);
    return {
        label: isTrue ? "Vrai" : "Fake",
        confidence: confidence
    };
}

function displayResult(result) {
    const resultDiv = document.getElementById('result');
    resultDiv.innerHTML = `Résultat : <strong>${result.label}</strong> (Confiance : ${result.confidence}%)`;
}

function addToHistory(text, result) {
    const historyList = document.getElementById('history');
    const listItem = document.createElement('li');
    listItem.textContent = `"${text.substring(0, 50)}..." - ${result.label} (${result.confidence}%)`;
    historyList.appendChild(listItem);
}