// --- DOM ELEMENTS ---
const analyzeBtn = document.getElementById("analyzeBtn");
const taskInput = document.getElementById("taskInput");
const strategySelect = document.getElementById("strategySelect");
const resultsDiv = document.getElementById("results");

// --- EVENT LISTENER ---
analyzeBtn.addEventListener("click", async () => {
    let tasks;
    try {
        tasks = JSON.parse(taskInput.value);
        if (!Array.isArray(tasks)) throw new Error("Input must be a JSON array.");
    } catch (err) {
        alert("Invalid JSON format. Ensure it's an array of tasks.");
        return;
    }

    const strategy = strategySelect.value;

    try {
        resultsDiv.innerHTML = "<p>Analyzing tasks...</p>";

        const response = await fetch("/analyze/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ tasks, strategy })
        });

        if (!response.ok) {
            const errData = await response.json();
            throw new Error(errData.error || "Server error");
        }

        const data = await response.json();
        displayResults(data);

    } catch (err) {
        console.error("Error:", err);
        resultsDiv.innerHTML = `<p style="color:red">Error: ${err.message}</p>`;
    }
});

// --- DISPLAY RESULTS ---
function displayResults(tasks) {
    resultsDiv.innerHTML = "";

    if (tasks.length === 0) {
        resultsDiv.innerHTML = "<p>No valid tasks to display.</p>";
        return;
    }

    tasks.forEach(task => {
        const div = document.createElement("div");
        div.className = "task-card";

        // Color code by score
        let color = "#4CAF50"; // default green
        if (task.score >= 80) color = "#ff4d4d"; // high priority - red
        else if (task.score >= 50) color = "#ffa500"; // medium priority - orange
        div.style.borderLeft = `8px solid ${color}`;

        div.innerHTML = `
            <strong>${task.title}</strong><br>
            Due: ${task.due_date}<br>
            Importance: ${task.importance}<br>
            Estimated Hours: ${task.estimated_hours}<br>
            Score: <strong>${task.score}</strong><br>
            Reason: ${task.reason}
        `;
        resultsDiv.appendChild(div);
    });
}
