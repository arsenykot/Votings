//#region htmlutils
function spawnToast(color, icon, content, closeButton = true, container = null){
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
        queryXHR.open(method, endpoint);
        httpheaders.forEach(pair => {
            queryXHR.setRequestHeader(pair[0], pair[1]);
        });
        if(method == "POST"){
            queryXHR.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
            let newdata = "";
            for(key in data){
                newdata += encodeURIComponent(key)+"="+encodeURIComponent(data[key])+"&";
            }
            data = newdata;
        }
        else{
            if(data == null){}
            else{
                queryXHR.setRequestHeader('Content-Type', 'application/json');
                data = JSON.stringify(data);
            }
        }
        
        queryXHR.send(data);
    }
    catch(e){
        errorCallback(e);
    }
    
}
function ajaxGet(endpoint, ready_callback, error_passthrough=false, httpheaders=[]){ajaxQuery(endpoint, "GET", ready_callback, error_passthrough, httpheaders);}
function ajaxPost(endpoint, ready_callback, data, error_passthrough=false, httpheaders=[]){ajaxQuery(endpoint, "POST", ready_callback, data, error_passthrough, httpheaders);}
function buildAjaxFormHandler(callback){
    return function(e){
        e.preventDefault();
        let form = e.target;
        let formElements = Array.from(form.querySelectorAll("input"));
        let formButtons = Array.from(form.querySelectorAll("button"));
        formElements = formElements.concat(formButtons);
        let headers = [];
        let requestData = {};
        let spinnerElements = [];
        formElements.forEach(element => {
            if(element.name=="csrfmiddlewaretoken") headers.push(["X-CSRFToken", element.value]);
            requestData[element.name] = element.value;
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