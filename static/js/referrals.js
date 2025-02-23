document.addEventListener('DOMContentLoaded', function() {
    const referralList = document.getElementById('referral-list');
    const referralForm = document.getElementById('referral-form');
    const referralEmailInput = document.getElementById('referral-email');

    // Simulate fetching user's referrals
    const referrals = [
        { email: "friend1@example.com", status: "Invited" },
        { email: "friend2@example.com", status: "Accepted" }
    ];

    // Render referral list
    referrals.forEach(referral => {
        const listItem = document.createElement('li');
        listItem.textContent = `${referral.email} - ${referral.status}`;
        referralList.appendChild(listItem);
    });

    // Handle referral form submission
    referralForm.addEventListener('submit', function(event) {
        event.preventDefault();
        const email = referralEmailInput.value;
        
        if (email) {
            // Simulate sending a referral invitation
            alert(`Referral sent to ${email}`);
            referralEmailInput.value = ''; // Clear input
        }
    });
});
