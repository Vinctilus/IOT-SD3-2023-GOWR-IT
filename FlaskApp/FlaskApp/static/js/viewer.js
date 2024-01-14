forms = document.querySelectorAll('form.viewer');
forms.forEach(element => {
    element.addEventListener("click", function () {
        window.location.href = element.action + "/" + element.name.substring(1)
    })

})