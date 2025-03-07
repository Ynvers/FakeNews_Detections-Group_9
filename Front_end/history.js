// class HistoryManager {
//     constructor() {
//         this.historyList = document.getElementById('historyList');
//         this.loadHistory();
//     }

//     loadHistory() {
//         const history = JSON.parse(localStorage.getItem('analysisHistory') || '[]');
        
//         if (history.length === 0) {
//             this.historyList.innerHTML = `
//                 <div class="empty-history">
//                     <i class="fas fa-history"></i>
//                     <p>No analysis history yet</p>
//                 </div>
//             `;
//             return;
//         }

//         this.historyList.innerHTML = history.map(item => this.createHistoryItem(item)).join('');
//     }

//     createHistoryItem(item) {
//         const date = new Date(item.timestamp).toLocaleString();
//         const score = item.result.credibilityScore;
//         let scoreClass;
        
//         if (score >= 70) scoreClass = 'success';
//         else if (score >= 40) scoreClass = 'warning';
//         else scoreClass = 'danger';

//         return `
//             <div class="history-item">
//                 <div class="history-header">
//                     <div class="history-meta">
//                         <span class="history-date">${date}</span>
//                         <span class="history-type">
//                             <i class="fas fa-${this.getTypeIcon(item.type)}"></i>
//                             ${item.type.toUpperCase()}
//                         </span>
//                     </div>
//                     <div class="history-score ${scoreClass}">
//                         ${score}% Credible
//                     </div>
//                 </div>
                
//                 <div class="history-content">
//                     <p>${item.content}</p>
//                 </div>
                
//                 <div class="history-verdict">
//                     <strong>Verdict:</strong> ${item.result.verdict}
//                 </div>
//             </div>
//         `;
//     }

//     getTypeIcon(type) {
//         switch (type) {
//             case 'text': return 'align-left';
//             case 'url': return 'link';
//             case 'file': return 'file-pdf';
//             default: return 'question';
//         }
//     }
// }

// // Initialize the history manager
// const historyManager = new HistoryManager();

class HistoryManager {
    constructor() {
        this.historyList = document.getElementById('historyList');
        this.loadHistory();
        this.addEventListeners();
    }

    addEventListeners() {
        // Ajouter un bouton pour effacer l'historique
        const clearButton = document.createElement('button');
        clearButton.className = 'clear-history-btn';
        clearButton.innerHTML = '<i class="fas fa-trash"></i> Clear History';
        clearButton.onclick = () => this.clearHistory();
        document.querySelector('header').appendChild(clearButton);
    }

    loadHistory() {
        const history = JSON.parse(localStorage.getItem('analysisHistory') || '[]');
        
        if (history.length === 0) {
            this.showEmptyState();
            return;
        }

        this.historyList.innerHTML = `
            <div class="history-container">
                ${history.map((item, index) => this.createHistoryItem(item, index)).join('')}
            </div>
        `;
    }

    showEmptyState() {
        this.historyList.innerHTML = `
            <div class="empty-history">
                <i class="fas fa-history fa-3x"></i>
                <h3>No Analysis History</h3>
                <p>Your previous analysis results will appear here</p>
            </div>
        `;
    }

    createHistoryItem(item, index) {
        const date = new Date(item.timestamp).toLocaleString();
        const score = item.result.credibilityScore;
        const scoreClass = this.getScoreClass(score);

        return `
            <div class="history-item" data-index="${index}">
                <div class="history-item-header">
                    <div class="history-meta">
                        <span class="history-date">
                            <i class="fas fa-calendar"></i>
                            ${date}
                        </span>
                        <span class="history-type">
                            <i class="fas fa-${this.getTypeIcon(item.type)}"></i>
                            ${item.type.toUpperCase()}
                        </span>
                    </div>
                    <div class="credibility-badge ${scoreClass}">
                        <i class="fas fa-shield-alt"></i>
                        ${score}% Credible
                    </div>
                </div>

                <div class="history-content">
                    <h4>Analyzed Content:</h4>
                    <p>${this.truncateContent(item.content)}</p>
                </div>

                <div class="history-details">
                    <div class="verdict">
                        <h4>Verdict:</h4>
                        <p>${item.result.verdict}</p>
                    </div>
                    
                </div>

                <button class="delete-item-btn" onclick="historyManager.deleteItem(${index})">
                    <i class="fas fa-trash"></i>
                </button>
            </div>
        `;
    }

    getScoreClass(score) {
        if (score >= 70) return 'high-credibility';
        if (score >= 40) return 'medium-credibility';
        return 'low-credibility';
    }

    getTypeIcon(type) {
        const icons = {
            text: 'align-left',
            url: 'link',
            file: 'file-pdf',
        };
        return icons[type] || 'question';
    }

    truncateContent(content) {
        return content.length > 150 ? content.substring(0, 150) + '...' : content;
    }

    deleteItem(index) {
        if (confirm('Are you sure you want to delete this item?')) {
            const history = JSON.parse(localStorage.getItem('analysisHistory') || '[]');
            history.splice(index, 1);
            localStorage.setItem('analysisHistory', JSON.stringify(history));
            this.loadHistory();
        }
    }

    clearHistory() {
        if (confirm('Are you sure you want to clear all history?')) {
            localStorage.removeItem('analysisHistory');
            this.loadHistory();
        }
    }
}

// Initialize the history manager
const historyManager = new HistoryManager();