$(document).ready(function(){
    initialise_edit_mode();
})

function initialise_edit_mode(){
    var recipe = document.getElementById("recipe-1");
    var recipe_items_div = document.getElementById("recipe-1-items");

    recipe.addEventListener('click', function(event) {
        console.log('clicked')
        event.preventDefault();
        if(recipe_items_div.style.display == 'none'){
            recipe_items_div.style.display = 'block'
        }
        else{
            recipe_items_div.style.display = 'none'
        }
    });
}