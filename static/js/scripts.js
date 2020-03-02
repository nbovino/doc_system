function getUrlParam(parameter, defaultvalue){
    var urlparameter = defaultvalue;
    if(window.location.href.indexOf(parameter) > -1){
        urlparameter = getUrlVars()[parameter];
        }
    return urlparameter;
}

function escapeRegExp(string) {
  return string.replace(/[.*+\-?^${}()|[\]\\]/g, '\\$&'); // $& means the whole matched string
}

function openAssetTypeForm() {
    document.getElementById("new-asset-type-form").style.display = "block";
}

function closeAssetTypeForm() {
    document.getElementById("new-asset-type-form").style.display = "none";
}

function openDepartmentForm() {
    document.getElementById("new-department").style.display = "block";
}

function closeDepartmentForm() {
    document.getElementById("new-department").style.display = "none";
}

function openManufacturerForm() {
    document.getElementById("new-manufacturer").style.display = "block";
}

function closeManufacturerForm() {
    document.getElementById("new-manufacturer").style.display = "none";
}


function openAddAssocTypeForm() {
    document.getElementById("add-assoc-type-form").style.display = "block";
    document.getElementById("solution-type-button").style.display = "none";
}

function closeAddAssocTypeForm() {
    document.getElementById("add-assoc-type-form").style.display = "none";
    document.getElementById("solution-type-button").style.display = "block";
}

function backToSolution(sid) {
    window.location.href = '/view_one_solution?solution_id=' + sid;
}

function updateSolution(sid){
    console.log("updating");
    $.ajax({
        url: '/edit_solution_post',
        type: 'POST',
        data: {solution: $('#edit-solution-form').serialize(), solution_id: sid},
        success: function(response) {
            console.log("Success in the ajax request");
            location.reload(true);
        },
        error: function(error) {
            console.log(error);
        }
    });
//    window.location.href = '/view_one_solution?solution_id=' + params.get('solution_id');
};

// This is almost exactly copied code



$(document).ready(function() {
    $('#edit-solution-button').click(function(e) {

        var update_submit_button = $("#update-solution-button");

        function edit_callback(response) {
            console.log("I got here!")
            var newHTML = "<form method='POST' action='#' id='edit-solution-form' name='edit-solution' role='form'>";
            newHTML = newHTML + "<label for='solution_title'>Solution Title:</label>";
            //TODO: make my own function to escape a string in JS or find one...
            newHTML = newHTML + '<input type="text" name="solution_title" required type="text" value="' + escapeRegExp(response["Title"]) + '"></br>';
            newHTML = newHTML + "</br><p>Steps</p><div id='dynamic-input-steps'>";

            for (step in response['Steps']) {
                newHTML = newHTML + "<div>"
                newHTML = newHTML + "<input type='text' name='step" + step + "' value='" + escapeRegExp(response['Steps'][step]) + "'>";
                newHTML = newHTML + "<a href='#' class='delete'>Delete</a></br></br></div>";
                var totalSteps = step
            }
            newHTML = newHTML + "</div><input type='button' value='Add Step' class='add-step-field'><br><br>";
            newHTML = newHTML + "<span style='display: none'><input type='text' name='solution_id' required type='text' value='" + solution_id + "'></span>";
            newHTML = newHTML + "<button type='button' onClick='backToSolution(" + response['Solution_id'] + ")'>Cancel</button>";
            newHTML = newHTML + "<button type='button' onclick='updateSolution(" + response['Solution_id'] + ")'>Update Solution</button>";
            newHTML = newHTML + "</form>";
            document.getElementById('js-solution').innerHTML = newHTML;

            $("#dynamic-input-steps").on("click", ".delete", function(e) {
                e.preventDefault();
                $(this).parent('div').remove();
                totalSteps--;
            })

            $(".add-step-field").click(function(e) {
                e.preventDefault();
                totalSteps++;
                var newdiv = document.createElement('div');
                newdiv.innerHTML = "Step: " + totalSteps + " <br><input type='text' name='step" + totalSteps + "' ><a href='#' class='delete'>Delete</a>";
                document.getElementById("dynamic-input-steps").appendChild(newdiv);
            });
        }


        $.ajax({
        'type': 'GET',
        'global': false,
        'url': '/static/data/one_solution.json',
        'success': function(data){
            console.log("success");
            edit_callback(data);
        }
        });
    });


function showSnackbar() {
    var x = document.getElementById("snackbar");
    x.className = "show";
    setTimeout(function() { x.className = x.className.replace("show", "");
    }, 2000);
}


//this searches but returns odd results. Could really use this later if made better.
$.ajaxSetup({ cache: false });
 $('#search-solutions').keyup(function(){
  var resultsFound = 0;
  $('#result').html('');
  $('#state').val('');
  var searchField = $('#search-solutions').val();
  var expression = new RegExp(searchField, "i");
  if (searchField != '') {
      $.getJSON('static/data/all_solution_data.json', function(data) {
       $.each(data, function(key, value){
        if (value.title.search(expression) != -1)
        {
         resultsFound++;
//         console.log(resultsFound);
         $('#result').append('<li class="list-group-item link-class"> '+ value.title + '|</span><span id="sidvalue" value="' + value.id + '"></span></li>');
        }
       });
      });
      setTimeout(function() {
        if (resultsFound == 0 && $('#result').html() == '') {
            showSnackbar();
        }
      }, 2000);
  } else {
    $('#result').html('');
  }


 });
  $('#result').on('click', 'li', function() {
//  var click_text = $(this).text();
  var click_text = $('.list-group-item').text().split('|');
  var selectedId = $('#sidvalue').attr('value');
  console.log('selected ID is' + selectedId);
  $('#search-solutions').val($.trim(click_text[0]));
  $("#result").html('');
 });
})

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
        window.location.href = '/view_solutions?asset_type=' + params.get('asset_type');
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

    function callback(response) {
    //TODO: I can put the form stuff in here to create the data and make the ajax call inside the function that is called when
    //TODO: the new asset type button is clicked. It should get both asset lists and compare them though to only put
    //TODO: the asset types that are not in the related field already to show in the form to be selected. Then when clicking "Add"
    //TODO: it will make an ajax call to update the column with updated associated asset types.
        var assetData = response;
    //    console.log(assetData);
    //    for(var key in assetData) {
    //        console.log(key, assetData[key]);
    //    }
    //    for(var k in assetData['all_asset_types']) {
    //        console.log(k);
    //    }
    //    for(var k in assetData['solution_asset_types']) {
    //        console.log(k);
    //    }
        var available_types = {};
        for (k in assetData['all_asset_types']) {
            if (k in assetData['solution_asset_types']) {
            } else {
                available_types[k] = assetData['all_asset_types'][k];
            }
        }
        console.log(available_types);
        var newdiv = document.createElement('div');
        newdiv.setAttribute("id", "inner-add-assoc-type-button");
        var formHTML = "<select id='add-assoc-type' multiple>";
        for (k in available_types) {
            formHTML = formHTML + "<option value=" + k + ">" + available_types[k] + "</option>";
        }
        formHTML = formHTML + "</select><p><button id='add-assoc' onClick='addAssocType()'>Add</button>  <button id='cancel-asset' onClick='hideAssocType()'>Cancel</button></p>";
        newdiv.innerHTML = formHTML;
        document.getElementById("add-assoc-type-button").appendChild(newdiv);
        document.getElementById("new-assoc-type").style.display = "none";
    }

    $.ajax({
    'type': 'GET',
    'global': false,
    'url': '/static/data/one_solution_data.json',
    'success': function(data){
        callback(data);
    }
    });

};

function hideAssocType() {
    var hideForm = document.getElementById("inner-add-assoc-type-button")
    hideForm.remove();
    document.getElementById("new-assoc-type").style.display = "block";
};

function addAssocType() {
    let params = new URLSearchParams(location.search);
    var solution_id = params.get('solution_id');
    $.ajax({
        url: '/add_assoc_type',
        async: false,
        data: {added_types: $('#add-assoc-type option:selected').val(), solution_id: solution_id},
        type: 'POST',
        success: function(response) {
            console.log(response);
            location.reload(true);
        },
        error: function(error) {
            console.log(error);
        }
    });
//    window.location.href = '/view_one_solution?solution_id=' + params.get('solution_id');
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
