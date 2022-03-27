Date.prototype.toDateInputValue = (function() {
    var local = new Date(this);
    local.setMinutes(this.getMinutes() - this.getTimezoneOffset())
    return local.toJSON().slice(0,10);
});

$(document).ready( function() {
    let startDate = new Date()
    $('#start-date').val(startDate.toDateInputValue())
    let endDate = new Date()
    endDate.setDate(endDate.getDate() + 7)
    $('#end-date').val(endDate.toDateInputValue())

    loadCalendarView(startDate, endDate)
    initialiseSubmitButton()
})

function initialiseSubmitButton(){
    let button = document.getElementById('submit-dates-button')
    button.addEventListener('click', function(event){
        if (validateDates()) submitDates()
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

function submitDates(){
    let startDate = new Date(document.getElementById('start-date').value)
    let endDate = new Date(document.getElementById('end-date').value)

    loadCalendarView(startDate, endDate)
}

function loadCalendarView(startDate, endDate){
    let date = startDate
    clearDateTable()
    //createDateTable();
    while(date <= endDate){
        addDateRow(date)
        date.setDate(date.getDate() + 1)
    }
}

function clearDateTable(){
    let tableBody = document.getElementById('calendar-table-body')
    tableBody.innerHTML = ""
}

function addDateRow(date){
    let tableBody = document.getElementById('calendar-table-body')

    let tr = document.createElement('tr')
    let date_string = date.toLocaleDateString()
    tr.setAttribute('id', date_string)

    let th = document.createElement('th')
    th.setAttribute('scope', 'row')
    th.classList.add('w-20', 'text-center')
    th.setAttribute('scope', 'row')
    th.appendChild(document.createTextNode(date.toLocaleDateString('en-uk', { weekday:"long"})))
    th.appendChild(document.createElement('br'))
    th.appendChild(document.createTextNode(date.toLocaleDateString('en-uk', { day:"numeric", month:"numeric"})))
    
    let td = document.createElement('td')
    td.classList.add('w-40')
    tr.appendChild(th)
    tr.appendChild(td)
    tableBody.appendChild(tr)
  
    addRecipeDropdownBox(td, date_string)
}

//create recipe dropbox box for user to select all recipes
async function addRecipeDropdownBox(td, date_string){
    let div = document.createElement('div')
    div.classList.add('input-group')
    let select = document.createElement('select')
    select.classList.add("custom-select")
    select.setAttribute('style', 'width:60%')
    select.id = "select-recipe-" + date_string
    div.appendChild(select)

    let button_div = document.createElement('div')
    button_div.classList.add('input-group-append')
    let button = document.createElement('button')
    button.classList.add('btn', 'btn-outline-secondary')
    button.type = "button"
    button.innerHTML = "Add"

    initialiseAddRecipeButton(button, select, date_string)
    
    button_div.appendChild(button)
    div.appendChild(button_div)


    const res = await fetch('/get_recipes', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        }
        })
        .then(res => res.json())
        .then(data => {
            let recipes = data.data
            for(let i=0; i < recipes.length; i++){
                let option = createRecipeOption(recipes[i])
                select.appendChild(option)
            }
            td.appendChild(div)
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

function initialiseAddRecipeButton(button, select, date_string){
    button.addEventListener('click', function(event){
        event.stopPropagation()
        event.preventDefault()

        recipe_id = select.value
        
        updateRecipe(recipe_id, date_string)
    })
}

async function updateRecipe(recipe_id, date_string){
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
            if(res.ok) console.log('success')
        })
        .catch((error) => {
            console.error('Error:', error);
    })
}
