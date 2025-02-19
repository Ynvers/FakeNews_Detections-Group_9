// script.js
document.getElementById('analyzeButton').addEventListener('click', function () {
    const text = document.getElementById('textInput').value;
    const url = document.getElementById('urlInput').value;
    const pdfFile = document.getElementById('pdfInput').files[0];

    if (text.trim() !== "") {
        analyzeText(text);
    } else if (url.trim() !== "") {
        analyzeUrl(url);
    } else if (pdfFile) {
        analyzePdf(pdfFile);
    } else {
        alert("Veuillez entrer un texte, un lien ou téléverser un fichier PDF.");
    }
});

function analyzeText(text) {
    // Simuler une analyse de texte
    const result = simulateAnalysis(text);
    displayResult(result);
    addToHistory(`Texte: "${text.substring(0, 50)}..."`, result);
}

function analyzeUrl(url) {
    // Simuler une analyse de lien
    const result = simulateAnalysis(`Lien: ${url}`);
    displayResult(result);
    addToHistory(`Lien: ${url}`, result);
}

function analyzePdf(pdfFile) {
    // Simuler une analyse de PDF
    const reader = new FileReader();
    reader.onload = function (e) {
        const text = e.target.result.substring(0, 100); // Limite à 100 caractères pour l'exemple
        const result = simulateAnalysis(`PDF: ${text}`);
        displayResult(result);
        addToHistory(`Fichier PDF: ${pdfFile.name}`, result);
    };
    reader.readAsText(pdfFile);
}

function simulateAnalysis(input) {
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

function addToHistory(input, result) {
    const historyList = document.getElementById('history');
    const listItem = document.createElement('li');
    listItem.textContent = `${input} - ${result.label} (${result.confidence}%)`;
    historyList.appendChild(listItem);
}