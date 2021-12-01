document.addEventListener("DOMContentLoaded", (event) => {
    document.querySelector('#info').addEventListener("submit", function(e){
        var fname = document.getElementById("fname").value;
        var email = document.getElementById("email").value;
        var comment = document.getElementById("comment").value;
        var data = {f: fname, e: email, c: comment};
        fetch(
        '/add_visitor',
        {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            body: JSON.stringify(data),
        })
        .then(response => response.json())
        e.preventDefault();
    })
});