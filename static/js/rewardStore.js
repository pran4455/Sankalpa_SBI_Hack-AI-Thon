document.addEventListener('DOMContentLoaded', function() {
    const userPointsElement = document.getElementById('user-points');
    const userTierElement = document.getElementById('user-tier');
    const rewardList = document.getElementById('reward-list');
    
    // Fetch user data (points, tier) from the backend (via API or session data)
    fetch('/api/user_info')
        .then(response => response.json())
        .then(data => {
            userPointsElement.textContent = data.points;
            userTierElement.textContent = data.user_tier;
            loadRewards(data.points); // Load personalized rewards based on points
        });

    // Fetch rewards based on points
    function loadRewards(points) {
        fetch(`/api/rewards?points=${points}`)
            .then(response => response.json())
            .then(rewards => {
                rewardList.innerHTML = '';
                rewards.forEach(reward => {
                    const listItem = document.createElement('li');
                    listItem.textContent = `${reward.name} - ${reward.pointsRequired} points`;
                    const redeemButton = document.createElement('button');
                    redeemButton.textContent = 'Redeem';
                    redeemButton.onclick = () => redeemReward(reward.id);
                    listItem.appendChild(redeemButton);
                    rewardList.appendChild(listItem);
                });
            });
    }

    // Handle reward redemption
    function redeemReward(rewardId) {
        fetch('/api/redeem_reward', {
            method: 'POST',
            body: JSON.stringify({ reward_id: rewardId }),
            headers: { 'Content-Type': 'application/json' },
        })
        .then(response => response.json())
        .then(data => alert(data.message));
    }
});
