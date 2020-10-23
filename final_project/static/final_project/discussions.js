// This JS file is used for the 'discussions.html' file, to allow for dynamic deletion of posts, and upvoting/downvoting posts

document.addEventListener('DOMContentLoaded', function() {
    temp1 = document.querySelectorAll(".upvote");
    temp2 = document.querySelectorAll(".downvote");
    temp3 = document.querySelectorAll(".delete_btn");

    // Run the like_func function for each temp1 variable
    temp1.forEach(upvote => {
        upvote_func(upvote);
    });

    temp2.forEach(downvote => {
        downvote_func(downvote);
    });

    temp3.forEach(temp => {
        delete_func(temp);
    });

    nav_disable = document.querySelector('#nav-disabled')
    nav_disable.addEventListener('click', () => {
        console.log('lol')
        document.querySelector('#alert').style.display = 'block';

        setTimeout(function() {
            $('#alert').fadeOut('slow');
        }, 1500);
    })

});



// Liking post function
function upvote_func(like){
    like.addEventListener('click', () => {
        console.log('upvote')
        //Get the post ID from the 'data-' attribute and query for elements using that ID
        post_id = like.getAttribute('data-id');

        upvote = document.querySelector(`#upvote-${post_id}`);
        upvoted = upvote.getAttribute('data-upvoted');
        downvoted = upvote.getAttribute('data-downvoted');
        vote_count = document.querySelector(`#vote_count-${post_id}`);

        //Fetch /like with PUT request to use this data in the views.py
        fetch('/upvote/', {
            method: 'PUT',
            body: JSON.stringify({
                id: post_id,
                upvoted: upvoted,
                downvoted: downvoted
            })
        })
        .then(response => response.json())
        .then(result => {
            if(result.upvoted == true && result.downvoted == false){
                upvote.classList.add('fas')
                upvote.classList.remove('far')

                downvote = document.querySelector(`#downvote-${post_id}`);
                downvote.classList.add('far')
                downvote.classList.remove('fas')

                upvote.setAttribute('data-upvoted', 'true')
                upvote.setAttribute('data-downvoted', 'false')

                downvote.setAttribute('data-upvoted', 'true')
                downvote.setAttribute('data-downvoted', 'false')

            } else if(result.upvoted == false && result.downvoted == false){
                upvote.classList.add('far')
                upvote.classList.remove('fas')

                downvote = document.querySelector(`#downvote-${post_id}`);
                
                upvote.setAttribute('data-upvoted', 'false')
                upvote.setAttribute('data-downvoted', 'false')

                downvote.setAttribute('data-upvoted', 'false')
                downvote.setAttribute('data-downvoted', 'false')
            }

            vote_count.innerHTML = `Total Votes: <span style="font-size: 10px;">${result.vote_count}</span>`
        });
    })
}



// Liking post function
function downvote_func(like){
    like.addEventListener('click', () => {
        console.log('downvote')
        //Get the post ID from the 'data-' attribute and query for elements using that ID
        post_id = like.getAttribute('data-id');

        downvote = document.querySelector(`#downvote-${post_id}`);
        upvoted = downvote.getAttribute('data-upvoted');
        downvoted = downvote.getAttribute('data-downvoted');
        vote_count = document.querySelector(`#vote_count-${post_id}`);

        //Fetch /like with PUT request to use this data in the views.py
        fetch('/downvote/', {
            method: 'PUT',
            body: JSON.stringify({
                id: post_id,
                upvoted: upvoted,
                downvoted: downvoted
            })
        })
        .then(response => response.json())
        .then(result => {
            if(result.downvoted == true && result.upvoted == false){
                downvote.classList.add('fas')
                downvote.classList.remove('far')

                upvote = document.querySelector(`#upvote-${post_id}`);
                upvote.classList.add('far')
                upvote.classList.remove('fas')

                downvote.setAttribute('data-downvoted', 'true')
                downvote.setAttribute('data-upvoted', 'false')

                upvote.setAttribute('data-downvoted', 'true')
                upvote.setAttribute('data-upvoted', 'false')


            } else if(result.downvoted == false && result.upvoted == false){
                downvote.classList.add('far')
                downvote.classList.remove('fas')

                upvote = document.querySelector(`#upvote-${post_id}`);
                
                downvote.setAttribute('data-downvoted', 'false')
                downvote.setAttribute('data-upvoted', 'false')

                upvote.setAttribute('data-downvoted', 'false')
                upvote.setAttribute('data-upvoted', 'false')
            }

            vote_count.innerHTML = `Total Votes: ${result.vote_count}`
        });
    })
}




function delete_func(del){
    del.addEventListener('click', () => {
        //Get the post ID from the 'data-' attribute and query for elements using that ID
        post_id = del.getAttribute('data-id');
        delete_button = document.querySelector(`#delete-${post_id}`);
        delete_post = document.querySelector(`#post-card-${post_id}`);

        if(confirm("Are you sure you'd like to delete this post?")) {
            check = true;
        } else {
            check = false;
        }

        if(check == true){
            fetch('/delete/', {
                method: 'PUT',
                body: JSON.stringify({
                    id: post_id,
                })
            })
            .then(response => response.json())
            .then(result => {
                delete_post.style.display = 'none'
            });
        }
    });
}