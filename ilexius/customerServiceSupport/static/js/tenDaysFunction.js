let addTenDays = document.getElementById('addTenDays');

document.addEventListener('DOMContentLoaded', e=>{
    e.preventDefault();
    console.log('test1');
    let xhr = new XMLHttpRequest();
    xhr.responseType = 'json';
    xhr.enctype = 'multipart/form-data';
    let fURLnew = '/free-terms-ten-days/';
    xhr.open('GET', fURLnew, true);
    xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    console.log('test2');
    htmlTen = '';
    xhr.onload = function () {
        dataTenDays = xhr.response;
        console.log(dataTenDays.dataTenDays);
        let counter = 0;
        for(let key in dataTenDays.dataTenDays){
            htmlTen += `<div class="container-fluid border border-secondary p-2 rounded mb-4">`;
            htmlTen += `<h5 class="text-secondary date-ten-full">Date ${Object.keys(dataTenDays.dataTenDays)[counter]}</h5>`;

            for(let key2 in dataTenDays.dataTenDays[key]){
                htmlTen += `<span class="badge badge-secondary ml-1 mt-1 get-date-ten"><span style="display: none">${Object.keys(dataTenDays.dataTenDays)[counter]}</span> ${dataTenDays.dataTenDays[key][key2]}</span>`

            }
            htmlTen += `</div>`;
            counter++;
        }
        addTenDays.innerHTML = htmlTen;

        const fullDate = document.querySelectorAll('.date-ten-full');
        const tenTerm = document.querySelectorAll('.get-date-ten');
        for(let c = 0; c < tenTerm.length; c++){
            tenTerm[c].addEventListener('click', ()=>{
                let text = tenTerm[c].childNodes[0].innerHTML;
                date_and_time_callback.value = `${text} ${tenTerm[c].innerText}`;
            })        }


        let close = document.querySelector('.close');
        let close2 = document.querySelector('.close2');

        close.addEventListener('click', ()=>{
            messageError.innerText = '';
            messageSuccess.innerHTML = '';
        });
        close2.addEventListener('click', ()=>{
            messageError.innerText = '';
            messageSuccess.innerHTML = '';
        })

    };
    xhr.send();
    console.log('test1');
})