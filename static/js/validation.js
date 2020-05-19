function editInformation(type) {
    inputs = document.getElementsByClassName(type);

    for (var i = 0; i < inputs.length; i++) {
        inputs[i].removeAttribute('disabled')
    }

    console.log(this);
}

function validateForm() {
    return;
}