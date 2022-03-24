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
    console.log(date.toLocaleDateString())

    let th = document.createElement('th')
    th.setAttribute('scope', 'row')
    th.classList.add('w-25', 'text-center')
    th.appendChild(document.createTextNode(date.toLocaleDateString('en-uk', { weekday:"long"})))
    th.appendChild(document.createElement('br'))
    th.appendChild(document.createTextNode(date.toLocaleDateString('en-uk', { day:"numeric", month:"numeric"})))
    
    let td = document.createElement('td')
    
    let select = document.createElement('select')
    select.classList.add("custom-select")
    let option = document.createElement('option')
    option.value = 'recipe-1'
    option.appendChild(document.createTextNode('recipe_name'))
    select.appendChild(option)


    td.appendChild(select)

    tr.appendChild(th)
    tr.appendChild(td)
    tableBody.appendChild(tr)
}
