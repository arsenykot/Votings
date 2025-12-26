//#region htmlutils
function spawnToast(color, icon, content, closeButton = false, container = null){
    let toastElement = document.createElement("div");
    toastElement.classList.add("toast", "align-items-center", "text-bg-"+color, "border-0", "mb-2", "mt-2", "mr-2");

    let toastInnerContainer = document.createElement("div");
    toastInnerContainer.classList.add("d-flex");

    let toastIcon = document.createElement("i");
    toastIcon.classList.add("bi", "bi-"+icon, "ms-2", "me-0", "m-auto");

    let toastBody = document.createElement("div");
    toastBody.classList.add("toast-body");
    toastBody.innerHTML = content;

    toastInnerContainer.appendChild(toastIcon);
    toastInnerContainer.appendChild(toastBody);

    if(closeButton==true){
        closeButton = document.createElement("button");
        closeButton.classList.add("btn-close", "me-2", "m-auto");
        closeButton.setAttribute("data-bs-dismiss","toast");
        toastInnerContainer.appendChild(closeButton);
    }
    toastElement.appendChild(toastInnerContainer);

    if(container == null) container = document.getElementById("toast-container");

    container.appendChild(toastElement);
    toastBootstrap = bootstrap.Toast.getOrCreateInstance(toastElement);
    toastBootstrap.show();
}
function setSpinner(element, text, size="sm", type="border"){
    let spinner = document.createElement("div");
    spinner.classList.add("spinner-"+type, "spinner-"+type+"-"+size);
    spinner.ariaHidden = true;
    element.innerHTML = "";
    element.appendChild(spinner);
    element.innerHTML += " ";
    let label = document.createElement("span");
    label.innerText = text;
    element.appendChild(label);
}
let LAST_SEEN_ERROR_TOAST = null;
function errorToast(error, text){
    if(error==LAST_SEEN_ERROR_TOAST) return;
    LAST_SEEN_ERROR_TOAST = error;
    spawnToast("danger", "exclamation-octagon-fill", text);
}
function clearError(){
    LAST_SEEN_ERROR_TOAST = null;
}
//#endregion htmlutils
//#region ajax
function ajaxQuery(endpoint, method, ready_callback, data = null, error_passthrough = false, httpheaders=[]){
    let queryXHR = new XMLHttpRequest();
    let errorCallback = function(e){
        if(error_passthrough){
            ready_callback({
                status: "failed",
                error: e
            });
        }
        else{
            console.error(e);
            spawnToast("danger", "exclamation-ocatgon-fill", "Something went wrong. Check console for more details.");
        }
    };
    queryXHR.addEventListener("readystatechange", function(e){
        if(queryXHR.readyState == queryXHR.DONE){
            ready_callback({
                status: queryXHR.status,
                content: queryXHR.response
            });
        }
    });
    queryXHR.addEventListener("error", errorCallback);
    try{
        let newdata = "";
        for(key in data){
            if(newdata.length>0) newdata += "&";
            newdata += encodeURIComponent(key)+"="+encodeURIComponent(data[key]);
        }
        let addr = "";
        if(method=="GET"){
            addr = endpoint + "?" + newdata;
        }
        else{
            addr = endpoint;
        }
        queryXHR.open(method, addr);
        httpheaders.forEach(pair => {
            queryXHR.setRequestHeader(pair[0], pair[1]);
        });
        if(method == "POST"){
            queryXHR.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
            console.log(data); console.log(newdata);
            data = newdata;
        }
        queryXHR.send(data);
    }
    catch(e){
        errorCallback(e);
    }
    
}
function ajaxGet(endpoint, ready_callback, data, error_passthrough=false, httpheaders=[]){ajaxQuery(endpoint, "GET", ready_callback, data, error_passthrough, httpheaders);}
function ajaxPost(endpoint, ready_callback, data, error_passthrough=false, httpheaders=[]){ajaxQuery(endpoint, "POST", ready_callback, data, error_passthrough, httpheaders);}
function buildAjaxFormHandler(callback){
    return function(e){
        e.preventDefault();
        let form = e.target;
        let formElements = Array.from(form.querySelectorAll("input"));
        let formButtons = Array.from(form.querySelectorAll("button"));
        let formTextAreas = Array.from(form.querySelectorAll("textarea"));
        let formSelects = Array.from(form.querySelectorAll("select"));

        formElements = formElements.concat(formButtons, formTextAreas, formSelects);
        let headers = [];
        let requestData = {};
        let spinnerElements = [];
        formElements.forEach(element => {
            if(element.name=="csrfmiddlewaretoken") headers.push(["X-CSRFToken", element.value]);

            if(element.type=="checkbox") requestData[element.name] = element.checked ? "on":"off";
            else if(element.type=="radio"){
                if(element.checked) requestData[element.name] = element.value;
            }
            else if(element.type=="submit") {}
            else requestData[element.name] = element.value;

            element.setAttribute("data-was-disabled", element.disabled);
            element.disabled = true;
        });

        formButtons.forEach(element => {
            if(element.hasAttribute("data-spinner-text")){
                element.setAttribute("data-default-text", element.innerText);
                setSpinner(element, element.getAttribute("data-spinner-text"));
                spinnerElements.push(element);
            }
        });

        let responseHandler = function(resp){
            spinnerElements.forEach(element => {
                element.innerText = element.getAttribute("data-default-text");
            });
            formElements.forEach(element => {
                element.disabled = element.getAttribute("data-was-disabled")=="true";
            });
            if(resp.status == "error"){
                console.error(resp);
                spawnToast("danger", "exclamation-octagon-fill", "Something went wrong. Check DevTools console for more information.", false);
            }
            else{
                callback(resp);
            }
        }
        ajaxPost(form.action, responseHandler, requestData, true, headers);
    }
}
//#endregion ajax
//#region formvalidation
function validateForm(form){
    let is_valid = true;
    let inputs = form.querySelectorAll("input");
    let submit_button = form.querySelector("input[type='submit']");
    if (!submit_button) submit_button = form.querySelector("button[type='submit']");
    inputs.forEach(input=>{
        if(input.hasAttribute("data-skiponfull")) return;
        if (!validateFormInput(input)){
            is_valid = false;
        }
        if (!submit_button && input.type == "submit") submit_button = input;
    });
    if(submit_button) submit_button.disabled = !is_valid;
    return is_valid;
}
function validateFormInput(input){
    let VALID = true;
    input.classList.remove("is-valid", "is-invalid");
    if (input.min && input.type=="number") VALID = VALID && input.value >= input.min;
    if (input.min && input.type!="number") VALID = VALID && input.value.length >= input.min;

    if (input.max && input.type=="number") VALID = VALID && input.value <= input.max;
    if (input.max && input.type!="number") VALID = VALID && input.value.length <= input.max;

    input.classList.add(VALID?"is-valid":"is-invalid");
    return VALID;
}
//#endregion formvalidation