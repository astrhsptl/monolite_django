axios.defaults.withCredentials = true;

async function getLikes(postID) {
    let data = await axios.post(`http://178.20.42.217/api/v1/docs/likes/counts/?post_id=${postID}`,)
    .then( result => {
            let elem = document.getElementById("likes"); 
            let totalResult = result.data.likes;
            elem.innerHTML = totalResult;
        } 
    )
};

async function addLike(postID, userID) {
    console.log(postID, userID)
    let data = await axios.post(`http://178.20.42.217/api/v1/docs/likes/add/?post_id=${postID}&user_id=${userID}`,)
    .then( r => {
            getLikes(postID)
        }
    )
};

function viewMoreComments() {
    document.getElementsByClassName("comment__hidden")["0"].style.display = 'grid';
}

async function addCopyLink (url) {
    let text = `http://178.20.42.217${url}`;
    try {
        await navigator.clipboard.writeText(text);
        alert('Content copied to clipboard');
      } catch (err) {
        alert('Failed to copy');
      }
}
