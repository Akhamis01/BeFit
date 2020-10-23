// This file is used in the 'register.html' file, to allow dynamic validation checking, and to add PayPal functionality

paid = false;

$("#username-check").click(function() {
    $(this).focus();
    console.log('click inside username')
});

$("#username-check").blur(function(){
    temp_user = document.querySelector('#username-check').value;

    fetch(`/user_exist`, {
        method: 'PUT',
        body: JSON.stringify({
            username: temp_user
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log('fetch call')
        if(data.user_exists == true || temp_user == ''){
            $("#register").fadeOut(800);
            document.querySelector('#username-check').classList.add('is-invalid');
            document.querySelector('#username-check').classList.remove('is-valid');

            document.querySelector('#valid-feedback').style.display = 'none';
            document.querySelector('#invalid-feedback').style.display = 'block';

        } else{
            document.querySelector('#username-check').classList.remove('is-invalid');
            document.querySelector('#username-check').classList.add('is-valid');

            document.querySelector('#valid-feedback').style.display = 'block';
            document.querySelector('#invalid-feedback').style.display = 'none';

            if($('#pick-user').val()!="Paid" || paid == true){
                $("#register").fadeIn(800);
            }
        }
    })
});


$("#pass").click(function() {
    $(this).focus();
    console.log('click inside pass')
});

$("#pass-confirm").click(function() {
    $(this).focus();
    console.log('click inside pass-confirm')
});

$("#pass").blur(function(){
    pass_check()
});

$("#pass-confirm").blur(function(){
    pass_check()
});

function pass_check(){
    pass = document.querySelector('#pass').value
    pass_confirm = document.querySelector('#pass-confirm').value

    if(pass == pass_confirm && pass != ''){
        if($('#pick-user').val()!="Paid" || paid == true){
            $("#register").fadeIn(800);
        }

        document.querySelector('#pass').classList.remove('is-invalid');
        document.querySelector('#pass-confirm').classList.remove('is-invalid');
        document.querySelector('#pass').classList.add('is-valid');
        document.querySelector('#pass-confirm').classList.add('is-valid');
    } else{
        $("#register").fadeOut(800);
        document.querySelector('#pass').classList.add('is-invalid');
        document.querySelector('#pass-confirm').classList.add('is-invalid');
        document.querySelector('#pass').classList.remove('is-valid');
        document.querySelector('#pass-confirm').classList.remove('is-valid');
    }
}



function selection(){
    if($('#pick-user').val()=="Paid"){
        $("#paypal-button-container").fadeIn(1500);
        $("#cv-upload").fadeOut(500);
        $("#register").fadeOut(800);
    }
    else if($('#pick-user').val()=="Free"){
        $("#paypal-button-container").fadeOut(1000);
        $("#cv-upload").fadeOut(800);
        $("#register").fadeIn(800);
    }
    else if($('#pick-user').val()=="Professional"){
        $("#paypal-button-container").fadeOut(1000);
        $("#cv-upload").fadeIn(800);
        $("#register").fadeIn(800);
    }

}

// Render the PayPal button into #paypal-button-container
paypal.Buttons({
    style: {
        shape: 'pill',
        label: 'pay',
        height: 40,
    },

    // Set up the transaction
    createOrder: function(data, actions) {
        return actions.order.create({
            purchase_units: [{
                amount: {
                    value: '2.99'
                }
            }]
        });
    },

    // Finalize the transaction
    onApprove: function(data, actions) {
        return actions.order.capture().then(function(details) {
            $("#paypal-button-container").fadeOut(1000);
            $("#selection-user").fadeOut(1000);
            $("#register").fadeIn(1000);
            paid = true;

            // Show a success message to the buyer
            alert('Transaction completed!, thank you for your purchase!');
        });
    }

}).render('#paypal-button-container');