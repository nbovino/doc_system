function getUrlParam(parameter, defaultvalue){
    var urlparameter = defaultvalue;
    if(window.location.href.indexOf(parameter) > -1){
        urlparameter = getUrlVars()[parameter];
        }
    return urlparameter;
}

function wait() {
    return confirm("small pause");
}


//function addInput() {
//    var newdiv = document.createElement('div');
//    newdiv.innerHTML = "Step: # <br><input type='text'>";
//    document.getElementById("dynamic-input-steps").appendChild(newdiv)
//};


//$('#add-solution-form').submit(function(e){
//    e.preventDefault();
//    $.ajax({
//        type: "POST",
//        url: "add_solution.html",
//        data: {data: $('form').serialize()},
//        success: function(response){
//            console.log("success!");
//        }
//});


$(document).ready(function() {
    var max_fields = 10;
    var wrapper = $("#dynamic-input-steps");
    var add_button = $(".add-step-field");
    var submit_button = $("#add-solution-button")
    var x = 1;
    $(add_button).click(function(e) {
        e.preventDefault();
//        if (x < max_fields) {
//            $(wrapper).append('<div><input type="text" name="mytext[]"/><a href="#" class="delete">Delete</a></div>'); //add input box

            var newdiv = document.createElement('div');
            newdiv.innerHTML = "Step: " + x + " <br><input type='text' name='step" + x + "' ><a href='#' class='delete'>Delete</a>";
            document.getElementById("dynamic-input-steps").appendChild(newdiv);
            x++;

    }); //else {
//            alert('You Reached the limits')
//        }
    $(wrapper).on("click", ".delete", function(e) {
        e.preventDefault();
        $(this).parent('div').remove();
        x--;
    })
//TODO: This works
    $(submit_button).click(function() {
        formData = $('form').serialize()
        console.log('Sending data');
        console.log(formData);
        wait();

//        var object = {};
//        formData.forEach(function(value, key){
//            object[key] = value;
//        });
//        var json = JSON.stringify(object)
//        var fs = require('fs');
//        fs.writeFile("test.txt", json, function(err) {
//            if (err) {
//                console.log(err);
//            }
//        });
    });

});

//    $(wrapper).on("click", ".delete", function(e) {
//        e.preventDefault();
//        $(this).parent('div').remove();
//        x--;
//    })
//});

//    var steps = document.getElementById("dynamic-input-steps");
//    var input = document.createElement("input");
//    input.type = "text";
//    steps.appendChild(document.createElement("br"));