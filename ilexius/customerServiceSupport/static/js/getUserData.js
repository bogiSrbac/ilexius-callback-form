const getClientId = document.querySelectorAll('.list-group-item');
const idUrl = document.querySelectorAll('.id');
const loopCustomerData = document.getElementById('loopCustomerData');
const commentSubmitButton = document.getElementById('commentSubmitButton');
let messageError = document.getElementById('error-text1');
let messageSuccess = document.getElementById('success-text1');
let close3 = document.querySelector('.close3');
let close4 = document.querySelector('.close4');
let addText = document.querySelector('.add-text');


for(let i = 0; i < getClientId.length; i++){
    getClientId[i].addEventListener('click', ()=>{
    console.log('test1');
    let id = idUrl[i].innerHTML;
    let xhrUpdate = new XMLHttpRequest();
    xhrUpdate.responseType = 'json';
    xhrUpdate.enctype = 'multipart/form-data';
    let urlUpdate = `/update-comment/${id}`;
    xhrUpdate.open('GET', urlUpdate, true);
    xhrUpdate.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    console.log('test2');
    htmlCustomer = '';
    xhrUpdate.onload = function () {
        dataUpdate = xhrUpdate.response;

        //disable comment update button if date of callback is in future
        let d1 = new Date();
        let jsonDate = d1.toJSON();
        let callbackTime = Date.parse(dataUpdate.customer.date_and_time_for_callback);
        if(Date.parse(jsonDate) < callbackTime){
            commentSubmitButton.disabled = true;
            commentSubmitButton.value = 'DISABLED';
                        addText.removeAttribute('id')


        }else{
            commentSubmitButton.disabled = false;
            commentSubmitButton.value = 'SUBMIT';
            addText.setAttribute('id', 'add-text')
        }
        htmlCustomer += `<li class="list-group-item"><span class="text-primary">Customer: </span>${dataUpdate.customer.first_name} ${dataUpdate.customer.last_name}</li>`
        if(dataUpdate.customer.phone_number){
            htmlCustomer += `<li class="list-group-item"><span class="text-primary">Phone number: </span>${dataUpdate.customer.phone_number}</li>`
        }
        if(dataUpdate.customer.company){
            htmlCustomer += `<li class="list-group-item"><span class="text-primary">Company: </span>${dataUpdate.customer.company}</li>`
        }
        htmlCustomer += `<li class="list-group-item"><span class="text-primary">Email: </span>${dataUpdate.customer.email}</li>`;
        htmlCustomer += `<li class="list-group-item"><span class="text-primary">Subject: </span>${dataUpdate.customer.subject}</li>`
        htmlCustomer += `<li class="list-group-item"><span class="text-primary">Problem desctription: </span>${dataUpdate.customer.problem_description}</li>`
        let dateTime = new Date(dataUpdate.customer.date_and_time_for_callback)
        let newDate = moment(dateTime).format('DD-MM-YYYY HH:mm')
        if(dataUpdate.customer.date_and_time_for_callback){
            htmlCustomer += `<li class="list-group-item"><span class="text-primary">Date/time: </span>${newDate}</li>`
        }
        let newDate1 = moment(dataUpdate.submit).format('DD-MM-YYYY HH:mm')
        htmlCustomer += `<li class="list-group-item"><span class="text-primary">Submit date: </span>${newDate1}</li>`

        let newDate2 = moment(dataUpdate.update).format('DD-MM-YYYY HH:mm')
        htmlCustomer += `<li class="list-group-item"><span class="text-primary">Update date: </span>${newDate2}</li>`
        if(dataUpdate.customer.comment){
            htmlCustomer += `<li class="list-group-item"><span class="text-primary">Comment: </span>${dataUpdate.customer.comment}</li>`
        }
        if(dataUpdate.customer.realized === false){
            htmlCustomer += `<li class="list-group-item"><span class="text-primary">Realized: </span>${dataUpdate.customer.realized}</li>`
        }

        loopCustomerData.innerHTML = htmlCustomer;





        //inserting data to update form

        adminId.value = dataUpdate.customer.admin;

        addCommentFunction(dataUpdate.customer.id)
        // close.addEventListener('click', ()=>{
        //     messageError.innerText = '';
        //     messageSuccess.innerHTML = '';
        // });
        // close2.addEventListener('click', ()=>{
        //     messageError.innerText = '';
        //     messageSuccess.innerHTML = '';
        // })

    };
    xhrUpdate.send();
    console.log('test1');
})
}

const commentId = document.getElementById('id_comment');
const realizedId = document.getElementById('id_realized');
const adminId = document.getElementById('id_administrator');
const formComment = document.getElementById('formComment');
function addCommentFunction(id) {
        formComment.addEventListener('submit', e=>{
            e.preventDefault();
            console.log('test1');
        const commentXHR = new FormData();
        commentXHR.append('csrfmiddlewaretoken', csrftoken2);
        commentXHR.append('comment', commentId.value);
        commentXHR.append('realized', realizedId.value);
        commentXHR.append('administrator', adminId.value);

        let updateXHR = new XMLHttpRequest();
        updateXHR.responseType = 'json';
        updateXHR.enctype = 'multipart/form-data';
        updateXHR.data = commentXHR;
        let updateId = `${id}`;
        let updateURL = `/update-comment-new/${updateId}/`;
        updateXHR.open('POST', updateURL, true);
        updateXHR.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
        console.log('test2');
        updateXHR.onload = function () {
            update = updateXHR.response;
            console.log('test3');

            if(update.message){
                messageError.innerHTML = update.message;
                triggerModa2()
             }

            close3.addEventListener('click', ()=>{
                messageError.innerText = '';
                messageSuccess.innerHTML = '';
            });
            close4.addEventListener('click', ()=>{
                messageError.innerText = '';
                messageSuccess.innerHTML = '';
            })

        }
        updateXHR.send(commentXHR);

        })
}
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken2 = getCookie('csrftoken');

function triggerModa2() {
         $("#myModal2").modal('show');

}