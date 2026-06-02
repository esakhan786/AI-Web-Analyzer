document.getElementById("analyzeBtn").addEventListener("click", async () => {
  const resultDiv = document.getElementById("result");
  const question = document.getElementById("question").value;

  resultDiv.innerText = "Analyzing...";

  const [tab] = await chrome.tabs.query({
    active: true,
    currentWindow: true
  });

  const url = tab.url;

  try {
    const response = await fetch("http://localhost:8000/analyze", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        url: url,
        question: question
      })
    });

    const data = await response.json();

    resultDiv.innerText = data.answer;

  } catch (error) {
    resultDiv.innerText = "Error: Backend is not running or URL cannot be loaded.";
  }
});
