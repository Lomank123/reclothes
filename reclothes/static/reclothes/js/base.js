// CSRF
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');

function formatDate(date) {
    const result = new Date(date);
    return result.toLocaleDateString();
}

function ajaxGet(url, callback, data=null) {
    $.ajax({
        url: url,
        headers: {"X-CSRFToken": csrftoken},
        data: data,
        method: 'GET',
        dataType: 'json',
        success: (result) => {
            console.log(result);
            callback(result);
        },
        error: (error) => {
            console.log(error);
        }
    });
}
