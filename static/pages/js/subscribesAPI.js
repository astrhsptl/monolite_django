async function subscribe(user, author) {
    let res = await axios.get(`http://178.20.42.217/api/v1/docs/subscribers/add/?subscriber_id=${user}&author_id=${author}`); 
    await location.reload();
}
