Date.prototype.toDateInputValue = (function() {
    var local = new Date(this);
    local.setMinutes(this.getMinutes() - this.getTimezoneOffset())
    return local.toJSON().slice(0,10);
});

$(document).ready( function() {
    getSelectedDates()
    initialiseSubmitButton()
})

function initialiseSubmitButton(){
    let button = document.getElementById('submit-dates-button')
    button.addEventListener('click', function(event){
        if (validateDates()) submitDates()
    })
}

async function getSelectedDates(){
    const res = await fetch('/api/selecteddates', {
        method: 'GET'
    })
    .then(res => res.json())
    .then(data => {
        startDate = new Date(data.dates.start_date)
        endDate = new Date(data.dates.end_date)
        $('#start-date').val(startDate.toDateInputValue())
        $('#end-date').val(endDate.toDateInputValue())
        loadCalendarView(startDate, endDate)
    })
    .catch((error) => {
        console.error('Error:', error)
    })
}

function validateDates(){
    let startDate = document.getElementById('start-date').value
    let endDate = document.getElementById('end-date').value

    if(!startDate) return false
    if(!endDate) return false
    if(endDate < startDate) return false

    return true

}

async function submitDates(){
    let startDate = new Date(document.getElementById('start-date').value)
    let endDate = new Date(document.getElementById('end-date').value)
    await selectNewDates(startDate, endDate)
}

async function selectNewDates(startDate, endDate){
    var data = {
        start_date: startDate.toLocaleDateString(),
        end_date: endDate.toLocaleDateString() 
    }
    await fetch('/api/selecteddates', {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
        })
        .then(function(){          
            loadCalendarView(startDate, endDate)
        })
        .catch((error) => {
            console.error('Error:', error);
    })
}

function loadCalendarView(startDate, endDate){
    let date = startDate
    clearDateTable()
    while(date <= endDate){
        addDateRow(date)
        date.setDate(date.getDate() + 1)
    }
}

function clearDateTable(){
    let daysContainer = document.getElementById('days-container')
    daysContainer.innerHTML = ""
}

function addDateRow(date){
    let date_string = date.toLocaleDateString()   //dd/mm/yyyy format
    let daysContainer = document.getElementById('days-container')
    let dayDiv = document.createElement('div')
    dayDiv.classList.add('day-div')
    daysContainer.appendChild(dayDiv)


    let dayTitleDiv = document.createElement('div')
    dayTitleDiv.classList.add("day-title-div")
    dayDiv.append(dayTitleDiv)
    let weekDaySpan = document.createElement('span')
    weekDaySpan.setAttribute("style", "font-weight: bold")
    dayTitleDiv.appendChild(weekDaySpan)
    weekDaySpan.appendChild(document.createTextNode(date.toLocaleDateString('en-uk', { weekday:"long"}))) //full weekday word
    dayTitleDiv.appendChild(document.createTextNode(" | " + date.toLocaleDateString('en-uk', { day:"numeric", month:"long"})))  // dd/mm format
    
    let dayRecipesDiv = document.createElement('div')
    dayRecipesDiv.classList.add("day-recipes-div")
    dayDiv.appendChild(dayRecipesDiv)
    let ul = document.createElement('ul')
    ul.id  = "recipe-list-" + date_string
    dayRecipesDiv.appendChild(ul)
    loadRecipesFromDatabase(date_string)
  
    addRecipeDropdownBox(dayTitleDiv, date_string)
}

async function loadRecipesFromDatabase(date_string){

    var data = {
        date_string: date_string
    }
    const res = await fetch('/get_recipes_for_date', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
        })
        .then(async res => {
            if(res.status == 200) return res.json()
        })
        .then(data => {
            if (data){
                let recipes = data.data
                if (recipes){
                    updateRecipeList(date_string, recipes)
                    }
                }
            else emptyRecipeList(date_string)
            })
        .catch((error) => {
            console.error('Error:', error);
    })
}

function emptyRecipeList(date_string){
    let ul_id = `recipe-list-${date_string}`
    let ul = document.getElementById(ul_id)
    ul.innerHTML = ""
}

function updateRecipeList(date_string, recipes){
    let ul_id = `recipe-list-${date_string}`
    let ul = document.getElementById(ul_id)
    ul.innerHTML = ""
    for(let i=0; i < recipes.length; i++){
        let li = document.createElement('li')
        li.appendChild(document.createTextNode(recipes[i].name))
        li.classList.add('recipe-li')
        ul.appendChild(li)
        addRemoveRecipeButton(li, date_string, recipes[i].id)
    }
}

function addRemoveRecipeButton(li, date_string, recipe_id){
    let span = document.createElement('span')
    let img = document.createElement('img')
    img.setAttribute("src", "../static/images/trashcan_icon.png")
    img.setAttribute("alt", "remove")
    img.setAttribute("width", "24px")
    img.setAttribute("height", "24px")
    img.classList.add("remove-icon")
    img.id = "remove-recipe-" + recipe_id + "-" + date_string
    span.appendChild(img)
    li.appendChild(span)
    span.classList.add('remove-button-span')

    initialiseRemoveRecipeButton(img, date_string, recipe_id)
}

function initialiseRemoveRecipeButton(img, date_string, recipe_id){
    img.addEventListener('click', function(event){
        event.preventDefault()
        event.stopPropagation()
        removeRecipeFromDate(recipe_id, date_string)
    })
}

//create recipe dropbox box for user to select all recipes
async function addRecipeDropdownBox(dayTitleDiv, date_string){
    let span = document.createElement('span')
    span.classList.add("dropdown-span")
    let select = document.createElement('select')
    select.classList.add("select-recipes")
    select.id = "select-recipe-" + date_string
    span.appendChild(select)

    let option = document.createElement('option')
    option.value = "0"
    option.disabled = true
    option.selected = true
    option.innerHTML = "Add"
    select.appendChild(option)

    addRecipeOptions(select)
    
    dayTitleDiv.appendChild(span)

    initialiseAddRecipe(select, date_string)

}

async function addRecipeOptions(select){
    await fetch('/api/recipes', {
        method: 'GET'
        })
        .then(res => res.json())
        .then(data => {
            let recipes = data.data
            for(let i=0; i < recipes.length; i++){
                let option = createRecipeOption(recipes[i])
                select.appendChild(option)
            }    
        })
        .catch((error) => {
            console.error('Error:', error);
    })
}

function createRecipeOption(recipe){
    let option = document.createElement('option')
    option.value = recipe.id
    option.appendChild(document.createTextNode(recipe.name))
    return option
}

function initialiseAddRecipe(select, date_string){
    select.addEventListener('change', function(event){
        event.stopPropagation()
        event.preventDefault()
        recipe_id = select.value
        if (recipe_id) addRecipe(recipe_id, date_string)
        select.value = "0"
    })
}

async function addRecipe(recipe_id, date_string){
    var recipe_data = {
        recipe_id: recipe_id,
        date_string: date_string
    }
    const res = await fetch('/add_recipe_date', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(recipe_data)
        })
        .then(async res => {
            if(!res.ok){
                const data = await res.json()
                console.log(data.error)
            }
            if(res.ok) loadRecipesFromDatabase(date_string)
        })
        .catch((error) => {
            console.error('Error:', error);
    })
}

async function removeRecipeFromDate(recipe_id, date_string){
    var recipe_data = {
        recipe_id: recipe_id,
        date_string: date_string
    }
    const res = await fetch('/remove_recipe_date', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(recipe_data)
        })
        .then(async res => {
            if(!res.ok){
                const data = await res.json()
                console.log(data.error)
            }
            if(res.ok) loadRecipesFromDatabase(date_string)
        })
        .catch((error) => {
            console.error('Error:', error);
    })
}
