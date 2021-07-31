const date = new Date();
document.querySelector('.year').innerHTML = date.getFullYear();

//Automatically fade out messages
setTimeout(function() {
    $('#message').fadeOut('slow')
}, 3000);