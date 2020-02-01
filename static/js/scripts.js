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

$(document).ready(function() {
    var max_fields = 10;
    var wrapper = $("#dynamic-input-steps");
    var add_button = $(".add-step-field");
    var submit_button = $("#add-solution-button")
    var add_form = $("#add-solution-form")
    var x = 1;

    $(add_button).click(function(e) {
        e.preventDefault();
        var newdiv = document.createElement('div');
        newdiv.innerHTML = "Step: " + x + " <br><input type='text' name='step" + x + "' ><a href='#' class='delete'>Delete</a>";
        document.getElementById("dynamic-input-steps").appendChild(newdiv);
        x++;

    });

    $(wrapper).on("click", ".delete", function(e) {
        e.preventDefault();
        $(this).parent('div').remove();
        x--;
    })

    $(submit_button).click(function() {

//        console.log($('#add-solution-form').serialize());
        $.ajax({
            url: '/add_solution_post',
            data: $('form').serialize(),
            type: 'POST',
            success: function(response) {
                console.log(response);
            },
            error: function(error) {
                console.log(error);
            }
        });
        var xhr = new XMLHttpRequest();
        xhr.onreadystatechange = function() {
            console.log(this.responseText);
            wait();
            if (this.readyState == 4 && this.status == 200) {
                var myObj = JSON.parse(this.responseText);
                document.getElementById("added-steps").innerHTML = myObj;
            }
        }

        window.location.href = '/add_solution?message=Solution Added';
//        location.reload(true)
    });

});

function showAddAssetType() {
//    var x = document.getElementById("asset-type-buttons")
    document.getElementById("asset-type-buttons").style.display = "block";
    document.getElementById("new-asset-type").style.display = "none";
};

function hideAddAssetType() {
    document.getElementById("asset-type-buttons").style.display = "none";
    document.getElementById("new-asset-type").style.display = "block";
};

function addAssetType() {
    console.log("Add asset type function in python to add this to database, then reload the page from JS")
    $.ajax({
        url: '/add_asset_type',
        data: $('form').serialize(),
        type: 'POST',
        success: function(response) {
            console.log(response);
        },
        error: function(error) {
            console.log(error);
        }
    });
    location.reload(true);
};

//$(document.getElementById("new-asset-type")).click(function() {

//    var assetButtons = document.getElementById("asset-type-buttons")
//    var newHTML = "<p><button id='add-asset'>Add</button>  <button id='cancel-asset'>Cancel</button></p>";
//    assetButtons.innerHTML = newHTML;
//        console.log($('#add-solution-form').serialize());
//    $.ajax({
//        url: '/add_solution_post',
//        data: $('form').serialize(),
//        type: 'POST',
//        success: function(response) {
//            console.log(response);
//        },
//        error: function(error) {
//            console.log(error);
//        }
//    });
//    var xhr = new XMLHttpRequest();
//    xhr.onreadystatechange = function() {
//        console.log(this.responseText);
//        wait();
//        if (this.readyState == 4 && this.status == 200) {
//            var myObj = JSON.parse(this.responseText);
//            document.getElementById("added-steps").innerHTML = myObj;
//        }
//    }
//});

//fetch('/add_solution')
//    .then(function (response) {
//        document.getElementById("added-steps").innerHTML = response.text();
//    }).then(function (text) {
//        console.log('GET response text:');
//        console.log(text);
//    })

//fetch('/add_solution')
//    .then(function (response) {
//        return response.json();
//    })
//    .then(function (json) {
//        console.log('GET response as JSON:');
//        console.log(json)
//    })
