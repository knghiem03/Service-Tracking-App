'use strict';

// Use this script to load client information from database back to html form.
console.log("loadClientForm.js file line 4")
$('#input-fname').val(`${fname}`)
$('#input-lname').val(`${lname}`)
$('#input-dob').val(`${dob}`)
$('#input-phone').val(`${phone}`)
$('#input-address').val(`${address}`)
$('#input-city').val(`${city}`)
$('#input-state').val(`${state}`)
$('#input-zip').val(`${zip}`)
$('#input-county').val(`${county}`)
$('#input-lang').val(`${lang}`) 
$('#addToDB').addClass("disabled")
console.log("loadClientForm.js file line 8")
