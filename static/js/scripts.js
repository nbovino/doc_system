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


//function readTextFile(file, callback) {
//    var rawFile = new XMLHttpRequest();
//    rawFile.overrideMimeType("application/json");
//    rawFile.open("GET", file, true);
//    rawFile.onreadystatechange = function() {
//        if (rawFile.readyState == 4 && rawFile.status == "200") {
//            callback(rawFile.responseText);
//        }
//    }
//    rawFile.send(null);
//}


var assetData;
function callback(response) {
//TODO: I can put the form stuff in here to create the data and make the ajax call inside the function that is called when
//TODO: the new asset type button is clicked. It should get both asset lists and compare them though to only put
//TODO: the asset types that are not in the related field already to show in the form to be selected. Then when clicking "Add"
//TODO: it will make an ajax call to update the column with updated associated asset types.
    assetData = response;
    console.log(assetData);
    for(var key in assetData) {
        console.log(key, assetData[key]);
    }
}

$.ajax({
    'type': 'GET',
    'global': false,
    'url': '/static/data/all_assoc_types.json',
    'success': function(data){
        callback(data);
    }
});

//TODO: This below function works best so far, assetData is a json object!
//var assetData = function() {
//    var tmp = null;
//    $.ajax({
//        async: false,
//        dataType: "json",
//        url: '/static/data/all_assoc_types.json',
//        success: function (data) {
//            tmp = data;
//            console.log(data);
//        }
//    });
//    console.log(tmp);
//    return tmp;
//}();
//
//console.log(assetData);

//TODO: This below function works. I just need to assign the ajax response to a variable
//function getData() {
//    $.ajax({
//
//        dataType: "json",
//        url: '/static/data/all_assoc_types.json',
    //    data: '/static/data/all_assoc_types.json',
//        success: function(data) {
//            console.log(data);
//        }
//    });
//}
//console.log(getData());
//
//console.log(getData().responseText);

$(document).ready(function() {
//    var asset_data;
//    var asset_data = jQuery.get('static/data/all_assoc_types.json', function(data, textStatus) {
//        console.log(data);
//        for (var key in data) {
//            console.log(key, data[key]);
//        }
//        console.log(data[2]);
//    });
//    console.log(asset_data);
//    console.log(asset_data.responseText);
//    for (var key in asset_data) {
//        console.log(key);
//    }
//    var assets = JSON.parse(all_assoc_types);
//    console.log(assets);
//    readTextFile("/static/data/all_assoc_types.json", function(text) {
//        var asset_data = JSON.parse(text);
//        console.log(asset_data);
//    });
//    for (var key in asset_types) {
//        if (asset_types.hasOwnProperty(key)) {
//            console.log(key, asset_types[key]);
//            console.log(key);
//        }
//    }
//    console.log(asset_data[2]);
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
        let params = new URLSearchParams(location.search);
        var asset_type = params.get('asset_type');

        $.ajax({
            url: '/add_solution_post',
            data: {solution: $('#add-solution-form').serialize(), asset_type: asset_type},
            type: 'POST',
            success: function(response) {
                console.log(response);
//                alert('form was submitted!');
            },
            error: function(error) {
                console.log(error);
            }
        });
//        var xhr = new XMLHttpRequest();
//        xhr.onreadystatechange = function() {
//            console.log(this.responseText);
//            wait();
//            if (this.readyState == 4 && this.status == 200) {
//                var myObj = JSON.parse(this.responseText);
//                document.getElementById("added-steps").innerHTML = myObj;
//            }
//        }
//        wait();
        window.location.href = '/view_solutions?asset_type=' + params.get('asset_type');
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

function showAddAssocType() {
    var newdiv = document.createElement('div');
    newdiv.setAttribute("id", "inner-add-assoc-type-button")
    // This should really add in a drop down of a multi select box to pic new types you want to add to this solution.
    newdiv.innerHTML = "<form><input type='text' name='new-assoc-type' id='add-assoc-type' role='form'></form><p><button id='add-assoc' onClick='addAssocType()'>Add</button>  <button id='cancel-asset' onClick='hideAssocType()'>Cancel</button></p>";
    document.getElementById("add-assoc-type-button").appendChild(newdiv);
    document.getElementById("new-assoc-type").style.display = "none";
};

function hideAssocType() {
    var hideForm = document.getElementById("inner-add-assoc-type-button")
    hideForm.remove();
    document.getElementById("new-assoc-type").style.display = "block";
};

function addAssocType() {
    $.ajax({
        url: '/add_assoc_type',
        data: $('$add-assoc-type').serialize(),
        type: 'POST',
        success: function(response) {
            console.log(response);
        },
        error: function(error) {
            console.log(error);
        }
    });
    location.reload(true);
}

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
