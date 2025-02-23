document.addEventListener('DOMContentLoaded', function() {
    // Mock data for leaderboard and challenges
    const leaderboard = [
        { name: "John Doe", points: 1000 },
        { name: "Jane Smith", points: 900 },
        { name: "Jack Daniels", points: 850 }
    ];

    const challenges = [
        { title: "30-Day Step Challenge", reward: "500 points", status: "In Progress" },
        { title: "Policy Renewal", reward: "200 points", status: "Completed" }
    ];

    // Render leaderboard
    const leaderboardList = document.getElementById('leaderboard-list');
    leaderboard.forEach(user => {
        const listItem = document.createElement('li');
        listItem.textContent = `${user.name}: ${user.points} points`;
        leaderboardList.appendChild(listItem);
    });

    // Render challenges
    const challengeList = document.getElementById('challenge-list');
    challenges.forEach(challenge => {
        const listItem = document.createElement('li');
        listItem.textContent = `${challenge.title} - ${challenge.reward} (${challenge.status})`;
        challengeList.appendChild(listItem);
    });
});
