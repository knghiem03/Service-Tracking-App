'use strict';

function showSearchResult(res) {
    // Check length of res and proceed accordingly. Use jQuery to add search result to a <div> 
    if (res.length === 0)  {
        $('#sch-result').append("<br><h3>This person is not in the database.</h>");
        $('#sch-result').append('<a href="/client_page">Create a record for this new client</a>');
    }
    else {
        // console.log("Use jquery to partially update the page")
        $('#sch-result').empty();
        $('#sch-result').append("<br><h3>This person is in the database.</h>");
        for (const r of res ) {
            let id    = r.client_id;
            let first = r.fname;
            let last  = r.lname;
            $('#sch-result').append(`${first}, ${last} <a href ="/loadClient/${id}">Load a record from this person</a>`);
            $('#sch-result').append("<br/>");
            // add more ajax call here ???
        }
    }
}
function searchClient(evt) {
    evt.preventDefault();
    const formData = { fname : $('#floatingFname').val(),
                       lname : $('#floatingLname').val()  }
    console.log(formData["fname"])
    console.log(formData["lname"])
    $.get('/searchDb', formData, showSearchResult)
}
$('#searchClient-form').on('submit',searchClient);
// =========================================================================================
function addClient(evt) {
    evt.preventDefault();
    const formData = $('#addClient-form').serialize();
    $.get('/addClientToDb', formData, (response) => {
                    
                    $('#record').removeClass("disabled")
                    $('#record').addClass("active")
                   
                    // console.log("Hello I am in showAddClient function")
                    $('#showClient-form').empty();
                    const fname = response.fname;
                    const lname = response.lname;
                    $('#showClient-form').append(`<h3>Client ${fname} ${lname} has been added to the database.</h3>`);
                    
                    // console.log(response)
    })
}
$('#addClient-form').on('submit', addClient);

// =========================================================================================
function recordService(evt){
    evt.preventDefault();
    const formData = $('#recordService-form').serialize();
    $.get('/recordService', formData, (response) => {
            console.log("Hello I am here on line 50");
            $('#showService-form').empty();
            $('#showService-form').append("<h3>Service notes were recorded</h3>")
    })
}
$('#recordService-form').on('submit',recordService);

// =========================================================================================
function runQuery(evt){
    evt.preventDefault();
    const formData = $('#sms_query_form').serialize();
    $.get('/run_sms_query', formData, (response) => {
        $('#result_form').empty();
        $('#result_form').append(`<h2>Query Result</h2>`);
        console.log("Hello I am here on line 64");
        $('#result_form').append(`<div>`);
        $('#result_form').append(`<table">`);
        $('#result_form').append(`<thead>`)
        $('#result_form').append(`<th scope="col">Num</th>`)
        $('#result_form').append(`<th scope="col">First</th>`)
        $('#result_form').append(`<th scope="col">Last</th>`)
        $('#result_form').append(`<th scope="col">Phone</th>`)
        $('#result_form').append(`<th scope="col">DOB</th></tr></thead>`)
        $('#result_form').append(`</thead>`)
        $('#result_form').append(`<tbody>`)

        if ( response.length > 1 ) {
            let count = 0;
            for (const r of response ) {
                let first      = r.fname;
                let last       = r.lname;
                let phone      = r.phone;
                let dob        = r.dob;
                let program_id = r.program_id;
                count += 1;
                $('#result_form').append(`<tr>`);
                $('#result_form').append(`<th scope="row">${count}</th>`);
                $('#result_form').append(`<td>${first}</td>`);
                $('#result_form').append(`<td>${last} </td>`);
                $('#result_form').append(`<td>${phone}</td>`);
                $('#result_form').append(`<td>${dob}</td>`);
                $('#result_form').append(`</tr>`);
            }
        }
        else {
            console.log(response[0].total);
            $('#result_form').append(`Total service minutes provided: ${response[0].total}`);
        }
        $('#result_form').append(`</tbody>`);
        $('#result_form').append(`</table>`);
        $('#result_form').append(`</div>`);
        console.log("Hello I am here on line 105");
    })
}
$('#sms_query_form').on('submit', runQuery);

// =====================================================================================
function sendSMS(evt) {
    evt.preventDefault();
    const formData = $('#sms_form_1').serialize();
    $.get('/one_sms', formData, (response) => {
        $('#sms_form_1').append(`<p>SMS mesg sent to ${formData["phone"]}</p>`)
        console.log("line 85")
        console.log(typeof(formData))
        // why formData at this point is a string, may need to make a dictionary on server
        // and pass it over here ???>
    })
}
$('#sms_form_1').on('submit', sendSMS);

// =====================================================================================
function sendListSMS(evt) {
    evt.preventDefault();
    const formData = $('#sms_form_2').serialize();
    console.log("Hello line 95 tracking.js")
    $.get('/send_query_sms', formData, (response) => {
        $('#result_form').empty();
        $('#result_form').append(`<h2>Phone list to send text message</h2>`)
        console.log("Hello I am here sendListSMS tracking.js");
        for (const r of response ) {
            let first      = r.fname;
            let last       = r.lname;
            let phone      = r.phone;
            let dob        = r.dob;
            let program_id = r.program_id;
            $('#result_form').append(`text to ${first}, ${last} - ${phone} -- ${dob} --- ${program_id}`);
            $('#result_form').append("<br/>");
        }
        $('#sms_form').append("<p>SMS mesg sent</p>")
        console.log("line 110 tracking.js")
    })
}
$('#sms_form_2').on('submit',sendListSMS);