(async function() {
    // Fetch and parse ans.txt
    const ansUrl = 'https://raw.githubusercontent.com/vizn3r/picovina/refs/heads/main/pdf/ans.txt';
    const response = await fetch(ansUrl);
    const textData = await response.text();
    
    // Parse into question-answer map
    const qaMap = new Map();
    let currentQuestion = null;
    
    textData.split('\n').forEach(line => {
        const trimmed = line.trim();
        if (trimmed.startsWith('•')) {
            const answer = trimmed.substring(1).trim();
            if (currentQuestion) qaMap.get(currentQuestion).push(answer);
        } else if (trimmed) {
            currentQuestion = trimmed;
            qaMap.set(currentQuestion, []);
        }
    });

    // Process questions on page
    document.querySelectorAll('table.elis_test_question').forEach(table => {
        const questionElem = table.querySelector('td.odsazena:not(.t-select-answer)');
        if (!questionElem) return;
        
        const questionText = questionElem.textContent.trim();
        const answers = qaMap.get(questionText) || [];
        
        table.querySelectorAll('td.odsazena.t-select-answer').forEach(answerElem => {
            const answerText = answerElem.textContent.trim();
            if (answers.includes(answerText)) {
                const checkbox = answerElem.closest('tr').querySelector('input[type="checkbox"]');
                if (checkbox) checkbox.checked = true;
            }
        });
    });
})();
