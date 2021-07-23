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


function likePost(postID){
	return fetch('/post/' + postID + '/like', {


		method: 'POST',
		headers: {
			"X-CSRFToken": getCookie('csrftoken')
		}
	}).then(() => {
		window.location.reload()
	})
}

function commentPost(postID, comment){
	const formData = new FormData()
	formData.append('content', comment)
	return fetch('/post/' + postID + '/comment', {

		
		method: 'POST',
		headers: {
			"X-CSRFToken": getCookie('csrftoken')
		},
		body: formData
	}).then(() => {
		window.location.reload()
	})
}
