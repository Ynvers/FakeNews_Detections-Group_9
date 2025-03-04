class FakeNewsDetector {
    constructor() {
        this.initializeElements();
        this.initializeEventListeners();
        this.currentInputType = 'text';
    }

    initializeElements() {
        // Input type buttons
        this.inputTypeButtons = document.querySelectorAll('.input-type-btn');
        this.inputForms = document.querySelectorAll('.input-form');

        // Input elements
        this.textArea = document.querySelector('#textInput textarea');
        this.urlInput = document.querySelector('#urlInput input');
        this.fileInput = document.querySelector('#fileInput input');
        this.dropZone = document.querySelector('.file-drop-zone');

        // Action elements
        this.analyzeBtn = document.getElementById('analyzeBtn');
        this.loadingIndicator = document.getElementById('loading');
        this.resultsSection = document.getElementById('results');
    }

    initializeEventListeners() {
        // Input type selection
        this.inputTypeButtons.forEach(button => {
            button.addEventListener('click', () => this.switchInputType(button));
        });

        // File drag and drop
        this.dropZone.addEventListener('dragover', (e) => {
            e.preventDefault();
            this.dropZone.style.borderColor = 'var(--primary-color)';
        });

        this.dropZone.addEventListener('dragleave', () => {
            this.dropZone.style.borderColor = 'var(--border-color)';
        });

        this.dropZone.addEventListener('drop', (e) => {
            e.preventDefault();
            this.dropZone.style.borderColor = 'var(--border-color)';
            const file = e.dataTransfer.files[0];
            if (file && file.type === 'application/pdf') {
                this.handleFileSelection(file);
            }
        });

        this.dropZone.addEventListener('click', () => {
            this.fileInput.click();
        });

        this.fileInput.addEventListener('change', (e) => {
            const file = e.target.files[0];
            if (file) {
                this.handleFileSelection(file);
            }
        });

        // Analyze button
        this.analyzeBtn.addEventListener('click', () => this.analyzeContent());
    }

    switchInputType(button) {
        // Update active button
        this.inputTypeButtons.forEach(btn => btn.classList.remove('active'));
        button.classList.add('active');

        // Update active form
        const inputType = button.dataset.type;
        this.currentInputType = inputType;
        this.inputForms.forEach(form => {
            form.classList.remove('active');
            if (form.id === `${inputType}Input`) {
                form.classList.add('active');
            }
        });
    }

    handleFileSelection(file) {
        if (file.type === 'application/pdf') {
            const fileName = file.name;
            this.dropZone.innerHTML = `
                <i class="fas fa-file-pdf"></i>
                <p>${fileName}</p>
                <small>Click or drag another file to replace</small>
            `;
        }
    }

    async analyzeContent() {
        let content;

        // Get content based on input type
        switch (this.currentInputType) {
            case 'text':
                content = this.textArea.value.trim();
                if (!content) {
                    this.showError('Please enter some text to analyze');
                    return;
                }
                break;

            case 'url':
                content = this.urlInput.value.trim();
                if (!this.isValidUrl(content)) {
                    this.showError('Please enter a valid URL');
                    return;
                }
                break;

            case 'file':
                const file = this.fileInput.files[0];
                if (!file) {
                    this.showError('Please select a PDF file');
                    return;
                }
                content = file;
                break;
        }

        // Show loading state
        this.loadingIndicator.style.display = 'block';
        this.resultsSection.style.display = 'none';

        try {
            // Simulate API call (replace with actual API endpoint)
            const result = await this.sendToAPI(content);
            this.displayResults(result);
        } catch (error) {
            this.showError('An error occurred during analysis');
            console.error(error);
        } finally {
            this.loadingIndicator.style.display = 'none';
        }
    }

    async sendToAPI(content) {
        // Replace with actual API endpoint
        const API_ENDPOINT = 'http://127.0.0.1:8000/analyze';

        const formData = new FormData();

        if (this.currentInputType === 'file') {
            formData.append('file', content);
        } else {
            formData.append('content', content);
            formData.append('type', this.currentInputType);
        }

        const response = await fetch(API_ENDPOINT, {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error('API request failed');
        }

        return await response.json();
    }

    // async sendToAPI(content) {
    //     console.log("📡 Simulation de l'envoi de contenu à l'API...");
    
    //     // Simuler un délai (comme une vraie requête API)
    //     await new Promise(resolve => setTimeout(resolve, 1500));
    
    //     // Générer un score aléatoire (0 à 100)
    //     const credibilityScore = Math.floor(Math.random() * 100);
    
    //     // Définir un verdict basé sur le score
    //     let verdict;
    //     if (credibilityScore >= 70) {
    //         verdict = "✅ Ce contenu est fiable.";
    //     } else if (credibilityScore >= 40) {
    //         verdict = "⚠️ Ce contenu contient des informations douteuses.";
    //     } else {
    //         verdict = "❌ Ce contenu semble être une fake news.";
    //     }
    
    //     // Simuler une réponse JSON de l'API
    //     const fakeResponse = {
    //         credibilityScore,
    //         verdict,
    //     };
    
    //     console.log("✅ Réponse simulée :", fakeResponse);
    
    //     return fakeResponse;
    // }
    

    displayResults(result) {
        // Update timestamp
        const timestamp = document.querySelector('.timestamp');
        timestamp.textContent = new Date().toLocaleString();

        // Update score
        const scoreValue = document.querySelector('.score-value');
        const scoreCircle = document.querySelector('.score-circle');
        const credibilityScore = result.credibilityScore;

        scoreValue.textContent = `${credibilityScore}%`;

        // Update score circle color based on score
        if (credibilityScore >= 70) {
            scoreCircle.style.borderColor = 'var(--success-color)';
        } else if (credibilityScore >= 40) {
            scoreCircle.style.borderColor = 'var(--warning-color)';
        } else {
            scoreCircle.style.borderColor = 'var(--danger-color)';
        }

        // Update verdict
        const verdictText = document.querySelector('.verdict-text');
        verdictText.textContent = result.verdict;

        // Show results
        this.resultsSection.style.display = 'block';

        // Save to history
        this.saveToHistory(result);
    }

    saveToHistory(result) {
        const history = JSON.parse(localStorage.getItem('analysisHistory') || '[]');
        history.unshift({
            timestamp: new Date().toISOString(),
            type: this.currentInputType,
            content: this.getContentPreview(),
            result: result
        });
        localStorage.setItem('analysisHistory', JSON.stringify(history.slice(0, 10)));
    }

    getContentPreview() {
        switch (this.currentInputType) {
            case 'text':
                return this.textArea.value.slice(0, 100) + '...';
            case 'url':
                return this.urlInput.value;
            case 'file':
                return this.fileInput.files[0]?.name || 'Unknown file';
        }
    }

    isValidUrl(string) {
        try {
            new URL(string);
            return true;
        } catch (_) {
            return false;
        }
    }

    showError(message) {
        alert(message);
    }
}

// Initialize the detector
const detector = new FakeNewsDetector();