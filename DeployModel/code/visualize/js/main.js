$("#show-method").click(function(){
    $("#graph")[0].style.display = "block"
})

$("#close-method").click(function(){
    $("#graph")[0].style.display = "none"
})

$("#cal-path").click(function(){
    var setting = {
        "async": true,
        "crossDomain": true,
        "url": "http://127.0.0.1:5000/CalPath",
        "method": "POST",
        "headers": {
        "content-type": "application/json",
        "cache-control": "no-cache",
        "postman-token": "e81e0d1c-cde1-b166-2025-1d8726e91517"
        },
        "processData": false
    };
    data = {
        "iter_times": $("#iter-times")[0].value,
        "startID": $("#start-node")[0].value,
        "destID": $("#dest-node")[0].value,
        "config_loc": $("#config-loc")[0].value
    }
    setting["data"] = JSON.stringify(data)

    $.ajax(setting).done(function (response) {
        alert(response)
    })
})