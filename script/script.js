(async () => {
  const rawTxtUrl = 'https://raw.githubusercontent.com/vizn3r/picovina/main/pdf/ans.txt';

  try {
    const res = await fetch(rawTxtUrl);
    const answerText = await res.text();
    const correctAnswers = answerText.trim().split('\n').map(a => a.trim());

    const answerCells = document.querySelectorAll('td.t-select-answer');

    let marked = 0;

    correctAnswers.forEach(correct => {
      answerCells.forEach(cell => {
        const cellText = cell.innerText.trim();
        if (cellText === correct) {
          const row = cell.closest('tr');
          const checkbox = row?.querySelector('input[type="checkbox"]');
          if (checkbox && !checkbox.checked) {
            checkbox.checked = true;
            cell.style.backgroundColor = 'lightgreen';
            cell.style.fontSize = '1.2em';
            cell.style.fontWeight = 'bold';
            marked++;
          }
        }
      });
    });

    alert(`✅ Marked ${marked} correct answers`);
  } catch (e) {
    console.error('❌ Failed to load answers or inject script:', e);
    alert('❌ Could not load answers or mark questions.');
  }
})();
