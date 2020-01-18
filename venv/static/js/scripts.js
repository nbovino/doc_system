function getUrlParam(parameter, defaultvalue){
    var urlparameter = defaultvalue;
    if(window.location.href.indexOf(parameter) > -1){
        urlparameter = getUrlVars()[parameter];
        }
    return urlparameter;
}


function addInput() {
    var newdiv = document.createElement('div');
    newdiv.innerHTML = "Step: # <br><input type='text'>";
    document.getElementById("dynamic-input-steps").appendChild(newdiv)
};


//    var steps = document.getElementById("dynamic-input-steps");
//    var input = document.createElement("input");
//    input.type = "text";
//    steps.appendChild(document.createElement("br"));