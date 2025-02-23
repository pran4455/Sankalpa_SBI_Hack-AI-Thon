function generateRoadmap() {
    let userInput = document.getElementById("userInput").value;

    fetch('/generate', {
            method: 'POST',
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ input: userInput })
        })
        .then(response => response.json())
        .then(data => {
            document.getElementById("output").innerText = data.roadmap || "Error generating roadmap";
        })
        .catch(error => console.error("Error:", error));
}