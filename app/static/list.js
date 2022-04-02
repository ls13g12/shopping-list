$(document).ready( function() {
    initialiseToggleHighlight()
})

function initialiseToggleHighlight(){
    $('.list-group-item').on('click', function(){
        $(this).toggleClass('selected-li-element')
    })
}
