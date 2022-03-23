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
    //div for all div
    let div = document.getElementById('calendar-view-div')
    div.innerHTML = ""

    let date = startDate
    while(date <= endDate){
        addDateDiv(date)
        date.setDate(date.getDate() + 1)
    }
}

function addDateDiv(date){
    //div for all calendar entries
    let div = document.getElementById('calendar-view-div')

    let dateDiv = document.createElement('div')
    dateDiv.classList.add('date-div')
    dateDiv.appendChild(document.createTextNode(date.toDateString()))

    div.appendChild(dateDiv)
}


