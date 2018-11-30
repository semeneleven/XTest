function changeval() {
    var checkboxes = document.getElementsByName('answer')
    for(var checkbox of checkboxes){
        if(checkbox.checked) {
            checkbox.value = 'true'
        } else {
            checkbox.value = 'false'
        }
    }
}
