document.addEventListener('DOMContentLoaded', function() {
    const rewardList = document.getElementById('reward-list');
    
    // Example Rewards (This can be dynamic and AI-based)
    const rewards = [
        { name: "Free Gym Membership", pointsRequired: 1000 },
        { name: "Premium Insurance Perks", pointsRequired: 5000 },
        { name: "Fitness Gear Voucher", pointsRequired: 2000 }
    ];

    // Render rewards list
    rewards.forEach(reward => {
        const listItem = document.createElement('li');
        listItem.textContent = `${reward.name} - ${reward.pointsRequired} points`;
        rewardList.appendChild(listItem);
    });
});
