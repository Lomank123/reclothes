const userProfileBlock = $('#user-profile-block');
const userId = userProfileBlock.data('user-id');


function setUserInfo(user) {
    const infoBlock = $(`
        <div class="flex-block">
            <span><b>User ${user.id}</b></span>
            <span><b>Name:</b> ${user.first_name} ${user.last_name}</span>
            <span><b>Email:</b> ${user.email}</span>
            <span><b>Date joined:</b> ${user.date_joined}</span>
            <span><b>Last login</b> ${user.last_login}</span>
        </div>
    `);

    // Company info
    if (user.company !== null) {
        const companyBlock = $(`
            <div class="flex-block">
                <span>Company ${user.company}</span>
            </div>
        `)
        infoBlock.append(companyBlock);
    }

    userProfileBlock.append(infoBlock);
}


$(window).on('load', async () => {
    const url = `${defaultUserUrl}/${userId}/`;
    const userData = await ajaxCall(url);

    if ('detail' in userData) {
        console.log('Error occured!');
        return;
    }

    setUserInfo(userData);
});
