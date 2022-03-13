$(document).ready(function(){
    initialise_toggle_items()
    initialise_enter_keydown_recipe()
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
        }) 
    }
}

function initialise_enter_keydown_items(recipe_element_id, add_item_to_recipe_input_id){
    var input_element = document.getElementById(add_item_to_recipe_input_id)
    input_element.addEventListener('keypress', function (e) {
        if (e.key === 'Enter') {
          let new_item = input_element.value
          add_item_to_recipe(new_item, recipe_element_id)
        }
    });
}

function initialise_enter_keydown_recipe(){
    var input_element = document.getElementById('add-recipe-input')
    input_element.addEventListener('keypress', function (e) {
        if (e.key === 'Enter') {
          let new_recipe = input_element.value
          add_recipe(new_recipe)
        }
    });
}

function initialise_remove_item_button(remove_item_button_id, recipe_item_id, recipe_element_id){
    let remove_item_button = document.getElementById(remove_item_button_id)
    remove_item_button.addEventListener('click', function(){
        remove_item_from_recipe(recipe_item_id, recipe_element_id)
    })
}

async function update_recipe_list(){
    const recipes = await get_recipes()
    console.log(recipes)
    //empty recipe list
    let recipe_list_div = document.getElementById("recipe-list")
    recipe_list_div.innerHTML = ""
    
    //create and append list element for each item in recipe
    for(let i=0; i < recipes.length; i++){
        let a = document.createElement('a')
        a.classList.add('list-group-item')
        a.classList.add('list-group-item-action')
        let recipe_id = 'recipe-' + recipes[i]['id']
        a.setAttribute('id', recipe_id)
        a.appendChild(document.createTextNode(recipes[i]['name']))
        recipe_list_div.appendChild(a)
        
        let div = document.createElement('div')
        div.classList.add('list-group')
        let div_id = 'recipe-' + recipes[i]['id'] + '-items'
        div.setAttribute('id', div_id)
        div.setAttribute('style', 'display:none')
        recipe_list_div.appendChild(div)
    }
    //add input box for new items under item list
    let li = document.createElement('li')
    li.classList.add('list-group-item')
    li.classList.add('list-group-item-action')

    
    let input = document.createElement('input')
    let add_recipe_input_id = "add-recipe-input"
    input.setAttribute('id', add_recipe_input_id)
    input.setAttribute('type', 'text')
    input.setAttribute('placeholder', 'new recipe')
    input.classList.add("add-item-input")
    li.appendChild(input)
    recipe_list_div.appendChild(li)
    input.focus()

    initialise_enter_keydown_recipe()
    initialise_toggle_items()
}

async function get_recipes(){

    const res = await fetch('/get_recipes', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        }
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

async function add_recipe(new_recipe){
    var data = {recipe: new_recipe}
    const res = await fetch('/add_recipe', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
        })
        .then(res => res.json())
        .then(res => {
            update_recipe_list()
        })
        .catch((error) => {
            console.error('Error:', error);
        })
    return res
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
        let recipe_item_id = 'item-' + items[i]['id']
        li.setAttribute('id', recipe_item_id)
        li.appendChild(document.createTextNode(items[i]['name']))
        recipe_items_div.appendChild(li)
        
        let button_div = document.createElement('div')
        button_div.style.cssFloat = 'right'
        li.appendChild(button_div)

        let button = document.createElement('button')
        button_div.appendChild(button)
        button.appendChild(document.createTextNode('X'))
        let remove_item_button_id = 'remove-recipe-item-' + recipe_item_id
        button.setAttribute('id', remove_item_button_id)

        initialise_remove_item_button(remove_item_button_id, recipe_item_id, recipe_element_id)
    }
    //add input box for new items under item list
    let li = document.createElement('li')
    li.classList.add('list-group-item')
    li.classList.add('list-group-item-light')
    let add_item_to_recipe_input_id = "input-add-item-to-" + recipe_element_id
    
    let input = document.createElement('input')
    input.setAttribute('id', add_item_to_recipe_input_id)
    input.setAttribute('type', 'text')
    input.setAttribute('placeholder', 'new item')
    input.classList.add("add-item-input")
    li.appendChild(input)
    recipe_items_div.appendChild(li)
    input.focus()

    initialise_enter_keydown_items(recipe_element_id, add_item_to_recipe_input_id)
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

async function add_item_to_recipe(new_item, recipe_element_id){
    let arr = recipe_element_id.split("-")
    var recipe_id = arr.pop()

    var data = {recipe_id: recipe_id, item: new_item}
    const res = await fetch('/add_item_to_recipe', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
        })
        .then(res => res.json())
        .then(res => {
            update_recipe_items(recipe_element_id)
        })
        .catch((error) => {
            console.error('Error:', error);
        })
    return res
}

async function remove_item_from_recipe(recipe_item_id, recipe_element_id){
    let arr = recipe_item_id.split("-")
    var recipe_item_id = arr.pop()

    var data = {recipe_item_id: recipe_item_id}
    const res = await fetch('/remove_item_from_recipe', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
        })
        .then(res => res.json())
        .then(res => {
            update_recipe_items(recipe_element_id)
        })
        .catch((error) => {
            console.error('Error:', error);
        })
    return res
}