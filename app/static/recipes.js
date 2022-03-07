$(document).ready(function(){
    initialise_toggle_items()
})

function initialise_toggle_items(){
    var recipe_list_elements = document.getElementsByClassName('list-group-item-action')
    for(let i=0; i <recipe_list_elements.length; i++){
        let recipe_items_div_id = recipe_list_elements[i].id + "-items"
        let recipe_items_div = document.getElementById(recipe_items_div_id)
        recipe_list_elements[i].addEventListener('click', function(event) {
            event.preventDefault();
            if(recipe_items_div.style.display == 'none'){
                recipe_items_div.style.display = 'block'
                update_recipe_items(this.id)
            }
            else{
                recipe_items_div.style.display = 'none'
            }
        });
    }
}

async function update_recipe_items(recipe_element_id){
    const items = await get_items(recipe_element_id)
    let recipe_items_div_id = recipe_element_id + "-items"
    let recipe_items_div = document.getElementById(recipe_items_div_id)
    recipe_items_div.innerHTML = ""
    
    //create and append list element for each item in recipe
    for(let i=0; i < items.length; i++){
        let li = document.createElement('li')
        li.classList.add('list-group-item')
        li.classList.add('list-group-item-light')
        li.setAttribute('id', items[i])
        li.appendChild(document.createTextNode(items[i]))
        recipe_items_div.appendChild(li)
    }

}
//fetch items from database
//if not recipe given, all items in database are returned
async function get_items(recipe_element_id=null){
    if (recipe_element_id != null){
        let arr = recipe_element_id.split("-")
        var recipe_id = arr.pop()
    }
    else{
        var recipe_id = null
    }
    var data = {id: recipe_id}
    const res = await fetch('/get_items', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
        })
        .then(res => res.json())
        .then(data => {
            return data.data
        })
        .catch((error) => {
            console.error('Error:', error);
        })
    return res
}