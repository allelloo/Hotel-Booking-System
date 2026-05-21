const pricePerNight=document.body.dataset.price;

const today=new Date().toISOString().split('T')[0];

document.getElementById('check_in').min=today;
document.getElementById('check_out').min=today;

function updatePrice(){

const ci=document.getElementById('check_in').value;
const co=document.getElementById('check_out').value;

if(ci && co){

const nights=(new Date(co)-new Date(ci))/86400000;

if(nights>0){

document.getElementById(
'price-preview'
).style.display='block';

document.getElementById(
'nights-label'
).textContent=nights+' night'+(nights>1?'s':'');

document.getElementById(
'total-price'
).textContent='$'+
(nights*pricePerNight).toFixed(2);

document.getElementById(
'check_out'
).min=ci;

}

}

}

document.getElementById(
'check_in'
).addEventListener('change',updatePrice);

document.getElementById(
'check_out'
).addEventListener('change',updatePrice);