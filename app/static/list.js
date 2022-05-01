Date.prototype.toDateInputValue = (function() {
    var local = new Date(this);
    local.setMinutes(this.getMinutes() - this.getTimezoneOffset())
    return local.toJSON().slice(0,10);
});

$(document).ready( function() {
    initialiseToggleHighlight()
    getSelectedDates()
    initialiseSubmitButton()
})

function initialiseToggleHighlight(){
    $('.list-group-item').on('click', function(){
        $(this).toggleClass('selected-li-element')
    })
}

function initialiseSubmitButton(){
    let button = document.getElementById('submit-dates-button')
    button.addEventListener('click', function(event){
        if (validateDates()) submitDates()
    })
}

async function getSelectedDates(){
    const res = await fetch('/get_selected_dates', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        }
        })
        .then(async res => {
            if(res.status >= 200 && res.status < 300) return res.json()
            else{
                const data = await res.json()
                console.log(data.error)
            }
        })
        .then(data => {
          if(data.dates){
            startDate = new Date(data.dates.start_date)
            endDate = new Date(data.dates.end_date)
          }
          else{
            startDate = new Date()
            endDate = new Date()
          }
          $('#start-date').val(startDate.toDateInputValue())
          $('#end-date').val(endDate.toDateInputValue())
        })
        .catch((error) => {
            console.error('Error:', error);
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
    const res = await fetch('/select_new_dates_items', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
        })
        .then((response)=>{         
            if(response.redirected){
                window.location.href = response.url;
            }
        })
        .catch((error) => {
            console.error('Error:', error);
    })
}