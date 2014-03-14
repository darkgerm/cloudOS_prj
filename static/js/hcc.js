//var username = "";
var hosts = 1;

function addOption(act, opt, i, fn) {
    var s1 = document.getElementById(act);
    var s2 = document.getElementById(opt);
    var s3 = document.getElementById("OK" + i);
    s2.innerHTML = " ";
    //b = $('<button>').html('OK')
    //b.attr('id', 'OK' + i); 
    //b.attr({onclick : "doOK(" + i + ",\'" + fn + "\')"});
    //s3.innerHTML=b[0].outerHTML;
    if(s1.value == "delete") s2.innerHTML = " ";
    else if(s1.value == "download") {
       s2.innerHTML = " ";
       s2 = document.getElementById('OK' + i);
       s2.innerHTML="<div><a href=\'un/" + username + "/fn/" + fn + "\'>Download</a></div>"; 
    }
    else if(s1.value == "compile") {
        var tmp = "<input type = \"radio\" id=\"mpi" + i + "-1\" name=\"mpi" +
                 "\" value=\"c\" checked=\"checked\">mpicc</input>";
        var tp2 = "<input type = \"radio\" id=\"mpi" + i + "-2\" name=\"mpi" + 
                 "\" value=\"cpp\">mpic++</input>";
        tp2 = tmp + tp2 + "   exeName:<input type=\"text\" id=\"exe"
                           + i + "\" value=\"a.out\" />";
        s2.innerHTML = tp2;
    }
    else if(s1.value == "run") {
        var tmp = "Hosts:<select id=\"host" + i + "\" name=\"host" + i + "\">";
        if(username.length > 5) hosts = 7;
        for(var j = 1; j <= hosts; ++j) {
            tmp += "<option value=" + j + ">" + j + "</option>";
        }
        tmp += "</select> np:<input type=\"number\" id=\"np" + i + "\"/>";
        tmp += " args:<input type=\"text\" id=\"args" + i + "\" value=\" \"/>";
        s2.innerHTML = tmp;
    }
    else s2.innerHTML = " ";
}

function doOK(i, fn) {
    var s1 = document.getElementById('action' + i);
    if(s1.value == "delete") {
        $.ajax({
            type: "DELETE",
            url: "http://xxx.xxx.xxx.xxx:5566/un/" + username + "/fn/" + fn,
            dataType: "json",
            success: function(json) {
                console.log(json);
                updateContent(json);
            },
            error: function() {
                console.log("JSON Failed");
            }
        });
    }
    else if(s1.value == "download") {
       s1 = document.getElementById('OK' + i);
       s1.innerHTML="<div><a href=\'un/" + username + "/fn/" + fn + "\'>Download</a></div>"; 
    }
    else if(s1.value == "compile") {
        var s2 = document.getElementById('mpi' + i + "-1");
        var tmp = "c";
        //if(s2.mpi[0].checked) tmp = "c";
        //else tmp = "cpp";
        var send = {
            "filetype": tmp,
            "exename": (document.getElementById('exe' + i)).value 
        }
        $.ajax({
            type: "POST",
            url: "http://xxx.xxx.xxx.xxx:5566/c/un/" + username + "/fn/" + fn,
            data: JSON.stringify(send),
            dataType: "json",
            contentType: "application/json",
            success: function(json) {
                console.log(json);
                updateContent(json);
                var sc2 = document.getElementById('std2');
                var sc3 = document.getElementById('std3');
                sc2.value = json.data['stdout']
                sc3.value = json.data['stderr']
            },
            error: function() {
                console.log("JSON Failed");
            }
        });
    }
    else if(s1.value == "run"){
        var s2 = document.getElementById('host' + i);
        var s3 = document.getElementById('np' + i);
        var s4 = document.getElementById('args' + i);
        var send = {
            "hosts": s2.value,
            "np": s3.value,
            "args": s4.vaule
        }
        $.ajax({
            type: "POST",
            url: "http://xxx.xxx.xxx.xxx:5566/r/un/" + username + "/fn/" + fn,
            dataType: "json",
            data: JSON.stringify(send),
            contentType: "application/json",
            success: function(json) {
                console.log(json);
                updateContent(json);
                var sc2 = document.getElementById('std2');
                var sc3 = document.getElementById('std3');
                sc2.value = json.data['stdout']
                sc3.value = json.data['stderr']
            },
            error: function() {
                console.log("JSON Failed");
            }
        });
    }
    else return;
}

function updateContent(json) {
   // username = $('#sendForm').find('input')[0].value;
    hosts = 5;
    var cnt = "<tr>" + "<td>FileName</td>" + "<td>Size</td>" + "<td>Action</td>"
            + "<td>Option</td>" + "<td>Check</td>" + "</tr>";
    var myOpt = "";
    for(var i = 0; i < json.data.length; ++i) {
        var fn = json.data[i]['name'];
        cnt += "<tr>";
        cnt += "<td>" + fn + "</td>";
        cnt += "<td>" + json.data[i]['size'] + "</td>";
        var myAct = "<select id=\"action" + i + "\" name = \"action" + i
                  + "\" onchange=\"addOption(this.id,\'myOpt" + i + "\'," + i + ",\'" + fn + "\')\">"
                  + "<option value=\"\"></option>"
                  + "<option value=\"delete\">delete</option>"
                  + "<option value=\"download\">download</option>"
                  + "<option value=\"compile\">compile</option>"
                  + "<option value=\"run\">run</option>"
                  + "</select>";
        cnt += "<td>" + myAct + "</td>";
        cnt += "<td>" + "<div id=\"myOpt" + i + "\"></div>" + "</td>";
        b = $('<button>').html('OK')
        b.attr('id', 'OK' + i); 
        b.attr({onclick : "doOK(" + i + ",\'" + fn + "\')"});
        cnt += "<td>" + b[0].outerHTML + "</td>";
        cnt += "</tr>";
    }
    $('#content').empty();
    $('#content').append(cnt);
}

function loadJSON() {
    //var username = $('#sendForm').find('input')[0].value;
    $.ajax({
        type: "GET",
        url: "http://xxx.xxx.xxx.xxx:5566/un/" + username,
        dataType: "json",
        success: function(json) {
            console.log(json);
            updateContent(json);
        },
        error: function() {
            console.log("JSON Failed");
        }
    });
}

function sendForm() {
    $('#sendForm').submit(function(e) {
        var formData = new FormData(this);
        $.ajax({
            url: "http://xxx.xxx.xxx.xxx:5566/fsupload",
            type: "POST",
            data: formData,
            mimeType: "multipart/form-data",
            contentType: false,
            cache: false,
            processData: false,
            success: function(data, textStatus, jqXHR) {
                console.log(data)
                console.log(textStatus)
                console.log(jqXHR)
            },
            error: function(jqXHR, textStatus, errorThrown) {
            }
        });
        e.preventDefault();
    });
    $('#sendForm').submit();
    $('#sendForm').find('input').each(function() {
        if(this.name != "username") {
            this.value = "";
        }
    });
}

//function sendData() {
//    var data = {};
//    $('#sendForm').find('input').each(function() {
//        data[this.name] = this.value;
//    });
//    sendJSON(data);
//}

//function sendJSON(data) {
//    $.ajax({
//        type: "POST",
//        contentType: "application/json",
//        url: "http://xxx.xxx.xxx.xxx:5566/fsupload",
//        data: JSON.stringify(data),
//        dataType: "json",
//        success: function(resp) {
//            console.log(resp);
//        },
//        error: function() {
//            console.log("Send JSON Failed");
//        }
//    });
//}
