let archiveData = document.getElementById('archive-data');

archiveData.addEventListener('click', e=>{
    e.preventDefault();
    let archiveXHR = new XMLHttpRequest();
    archiveXHR.responseType = 'json';
    archiveXHR.enctype = 'multipart/form-data';
    let archiveURL = '/archive/';
    archiveXHR.open('GET', archiveURL, true);
    archiveXHR.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    htmlTen = '';
    archiveXHR.onload = function () {
        archiveCalls = archiveXHR.response;
        location.reload();



        if(archiveCalls.message){
                messageError.innerHTML = archiveCalls.message;
                triggerModal()
             }



        close3.addEventListener('click', ()=>{
            messageError.innerText = '';
            messageSuccess.innerHTML = '';
        });
        close4.addEventListener('click', ()=>{
            messageError.innerText = '';
            messageSuccess.innerHTML = '';
        })

    };
    archiveXHR.send();
    console.log('test1');
})