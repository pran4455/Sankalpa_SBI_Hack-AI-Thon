async function earnPoints() {
    let name = prompt("Enter your name:");
    if (name) {
        await fetch('/api/add_points', {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({"name": name, "points": 10})
        });
        alert("🏅 10 points added!");
    }
}

async function referFriend() {
    let name = prompt("Enter your name:");
    if (name) {
        await fetch('/api/referral', {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({"name": name})
        });
        alert("🔗 Referral bonus added!");
    }
}
