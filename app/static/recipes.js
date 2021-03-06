$(document).ready(function(){
		update_recipe_list()
})

function initialise_toggle_items(){
		var recipe_list_elements = document.getElementsByClassName('list-group-item-action')
		for(let i=0; i <recipe_list_elements.length; i++){
				let recipe_items_div_id = recipe_list_elements[i].id + "-items"
				let recipe_items_div = document.getElementById(recipe_items_div_id)

				recipe_list_elements[i].addEventListener('click', function(event) {
						event.preventDefault();
						if(recipe_items_div.style.display == 'none'){
								//close all other item lists
								let all_divs = document.getElementsByClassName('list-group')
								//skip main list, start for index 1
								for(let j=1; j < all_divs.length; j++){
										all_divs[j].style.display = 'none'
								}
								//set clicked div to display
								update_recipe_items(this.id)
								recipe_items_div.style.display = 'block'
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
					if(new_item) add_item_to_recipe(new_item, recipe_element_id)
				}
		});
}

function initialise_add_item_button(recipe_element_id, add_item_to_recipe_input_id, img){
		var input_element = document.getElementById(add_item_to_recipe_input_id)
		img.addEventListener('click', function (e) {
				let new_item = input_element.value
				if(new_item) add_item_to_recipe(new_item, recipe_element_id)
		});
}

function initialise_enter_keydown_recipe(){
		var input_element = document.getElementById('add-recipe-input')
		input_element.addEventListener('keypress', function (e) {
				if (e.key === 'Enter') {
					let new_recipe = input_element.value
					if(new_recipe) add_recipe(new_recipe)
				}
		});
}

function initialise_remove_recipe_button(remove_recipe_button_id, recipe_id){
		let remove_recipe_button = document.getElementById(remove_recipe_button_id)
		remove_recipe_button.addEventListener('click', function(){
				if (confirm("Are you sure?")) remove_recipe(recipe_id)
		})
}

function initialise_remove_item_button(img, recipe_id, item_id, recipe_element_id){
		img.addEventListener('click', function(){
				if (confirm("Are you sure?")) remove_item_from_recipe(recipe_id, item_id, recipe_element_id)
		})
}

async function update_recipe_list(){
		const recipes = await get_recipes()

		//empty the recipe list
		let recipe_list_div = document.getElementById("recipe-list")
		recipe_list_div.innerHTML = ""
		
		//create and append list element for each item in recipe
		if (recipes){
				for(let i=0; i < recipes.length; i++){
						let a = document.createElement('a')
						a.classList.add('list-group-item')
						a.classList.add('list-group-item-action')
						let recipe_id = 'recipe-' + recipes[i]['id']
						a.setAttribute('id', recipe_id)
						a.appendChild(document.createTextNode(recipes[i]['name']))
						recipe_list_div.appendChild(a)

						//delete button on right of list element
						let remove_div = document.createElement('div')
						remove_div.style.cssFloat = 'right'
						a.appendChild(remove_div)
						let img = document.createElement('img')
						img.setAttribute("src", "../static/images/trashcan_icon.png")
						img.setAttribute("alt", "remove")
						img.setAttribute("width", "24px")
						img.setAttribute("height", "24px")
						let remove_recipe_button_id = 'remove-recipe-' + recipe_id
						img.setAttribute('id', remove_recipe_button_id)
						remove_div.appendChild(img)

						initialise_remove_recipe_button(remove_recipe_button_id, recipe_id)
						
						let div = document.createElement('div')
						recipe_list_div.appendChild(div)
						div.classList.add('list-group', 'recipe-item-list-div')
						let div_id = 'recipe-' + recipes[i]['id'] + '-items'
						div.setAttribute('id', div_id)
						div.setAttribute('style', 'display:none')
				}
		}
		//add input box for new items under item list
		let li = document.createElement('li')
		li.classList.add('list-group-item')
		
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

//returns an array of dicts with keys of recipe id and recipe name
async function get_recipes(){

		const res = await fetch('/api/recipes', {
				method: 'GET',
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

//add recipes to database and calls the update recipe lists function
//returns an error if recipe already exists in db
async function add_recipe(new_recipe){
		var data = {recipe: new_recipe}
		const res = await fetch('/api/recipes', {
				method: 'POST',
				headers: {
						'Content-Type': 'application/json',
				},
				body: JSON.stringify(data),
				})
				.then(async res => {
						if (!res.ok){
								const data = await res.json()
								console.log(data.error)
						}
						else update_recipe_list()
				})
				.catch((error) => {
						console.error('Error:', error);
		})
}

async function remove_recipe(recipe_id){
		let arr = recipe_id.split("-")
		var recipe_id = arr.pop()
		const res = await fetch(`/api/recipes/${recipe_id}`, {
				method: 'DELETE'
		})
		.then(() => {
			update_recipe_list()
		})
		.catch((error) => {
				console.error('Error:', error);
		})
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
				li.appendChild(document.createTextNode(items[i]['name']))
				recipe_items_div.appendChild(li)
				
				//delete button on right of list element
				let remove_div = document.createElement('div')
				remove_div.style.cssFloat = 'right'
				li.appendChild(remove_div)

				let img = document.createElement('img')
				img.setAttribute("src", "../static/images/trashcan_icon.png")
				img.setAttribute("alt", "remove")
				img.setAttribute("width", "22px")
				img.setAttribute("height", "22px")
				img.classList.add("remove-icon-items")
				remove_div.appendChild(img)

				let item_id = items[i]['item_id']
				let recipe_id = items[i]['recipe_id']
				initialise_remove_item_button(img, recipe_id, item_id, recipe_element_id)
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

		//add button next to input element
		let add_button_div = document.createElement('div')
		add_button_div.style.cssFloat = 'right'
		li.appendChild(add_button_div)

		let img = document.createElement('img')
		img.setAttribute("src", "../static/images/add_icon.png")
		img.setAttribute("alt", "add")
		img.setAttribute("width", "22px")
		img.setAttribute("height", "22px")
		img.classList.add("remove-icon-items")
		add_button_div.appendChild(img)

		initialise_add_item_button(recipe_element_id, add_item_to_recipe_input_id, img)
		initialise_enter_keydown_items(recipe_element_id, add_item_to_recipe_input_id)

		input.focus()
}

//fetch items from database
//if not recipe given, all items in database are returned
async function get_items(recipe_element_id){
		let arr = recipe_element_id.split("-")
		var recipe_id = arr.pop()

		const res = await fetch(`/api/recipes/${recipe_id}/items`, {
				method: 'GET'
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

//add item to recipe
//calls update items to recipe function on success 2xx 
async function add_item_to_recipe(new_item, recipe_element_id){
		let arr = recipe_element_id.split("-")
		var recipe_id = arr.pop()

		var data = {item: new_item}
		fetch(`/api/recipes/${recipe_id}/items`, {
				method: 'POST',
				headers: {
						'Content-Type': 'application/json',
				},
				body: JSON.stringify(data),
				})
				.then(async res => {
						if(!res.ok){
								const data = await res.json()
								console.log(data.error)
						}
						if(res.ok) update_recipe_items(recipe_element_id)
				})
				.catch((error) => {
						console.error('Error:', error);
				})
}

async function remove_item_from_recipe(recipe_id, item_id, recipe_element_id){

		const res = await fetch(`api/recipes/${recipe_id}/items/${item_id}`, {
				method: 'DELETE'
				})
				.then(res => res.json())
				.then(() => {
						update_recipe_items(recipe_element_id)
				})
				.catch((error) => {
						console.error('error:', error);
				})
}