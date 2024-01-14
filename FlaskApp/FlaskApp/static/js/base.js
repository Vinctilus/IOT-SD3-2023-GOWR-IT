donottoggel = document.querySelectorAll('.nonetogel');
donottoggel.forEach(element => {
    element.addEventListener('click', function () {
        if (this.checked) {
            this.checked = false;

        } else {
            this.checked = true;

        }
    })
    donottoggel.checked = donottoggel.checked
})

logo = document.getElementById("logoContainer");
logo.addEventListener("click", function () {
    window.location.href ="/home";
    })