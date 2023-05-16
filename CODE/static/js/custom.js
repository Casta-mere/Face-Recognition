//face Recog
function closeMedia() {
        var video = document.getElementById('video');
        if (!video.srcObject) return
        let stream = video.srcObject
        let tracks = stream.getTracks();
        tracks.forEach(track => {
            track.stop()
        })
}   

function getMedia() {
    let video = document.getElementById("video");
    let constraints = {
        video: {width: 400, height: 400},
        audio: false
    };
    let promise = navigator.mediaDevices.getUserMedia(constraints);
    promise.then(function (MediaStream) {
        video.srcObject = MediaStream;
        video.play();
    }).catch(function (PermissionDeniedError) {
        console.log(PermissionDeniedError);
    })
}

function takePhoto() {
    let canvas = document.getElementById("canvas");
    let ctx = canvas.getContext('2d');
    ctx.drawImage(video, 0, 0, 400, 400);
}

function uploadImage(){
    var canvas = document.getElementById('canvas');
    var context = canvas.getContext('2d');
    canvas.width = 400;
    canvas.height = 400;
    context.drawImage(video, 0, 0, 400, 400);
    var imgData = canvas.toDataURL("image/jpg");
    imgData = imgData.replace(/^data:image\/(png|jpg);base64,/,"")
    var uploadAjax = $.ajax({
        type: "post",
        url:"/receiveImage",
        data: JSON.stringify({"imgData": imgData}),
        contentType:"json/application",
        timeout:10000,
        async: true,
        complete: function (XMLHttpRequest, textStatus) {
            if(textStatus == 'timeout'){
                uploadAjax.abort(); 
                alert("请求超时，请重试")
                closeCard();
            }
        }
    });
}

function sendBack(){
    var name = document.getElementById("name").value;
    var stuid = document.getElementById("stuid").value;
    console.log(name);
    console.log(stuid);
    var uploadAjax = $.ajax({
        url:"/sendInfo",
        type: "get",
        dataType: "text",
        data: JSON.stringify({"name": name, "stuid": stuid}),
        contentType:"json/application",
        timeout:1500000,
        async: true,
        beforeSend: function () {
            $("#waitA").html("正在发送，请稍后...");
        },
        success: function (msg) {
            alert(msg)
            window.location.href = "/adminPage";
            },
        error: function(msg) {
            alert(msg)
            $("#waitA").html("");
        },
        complete: function (XMLHttpRequest, textStatus) {
            if(textStatus == 'timeout'){
                uploadAjax.abort(); 
                alert("请求超时，请重试")
                closeCard();
            }
        }
    });
}

//manageInfo
function turnToDel() {
    // 获取表格
    var table = document.getElementsByTagName('table')[0];
    console.log(table);

    // 获取所有行
    var rows = table.querySelectorAll('tr');
    let nData = [];
    
    // 遍历每一行
    for (var i = 0; i < rows.length-1; i++) {
        // 获取该行所有单元格
        console.log(rows[i+1].getAttribute('class'))
        console.log(rows[i+1])
        if (rows[i+1].getAttribute('class') != null) {
            var cells = rows[i+1].querySelectorAll('td');
            // 处理单元格的值
            var cellValueID = cells[1].textContent || cells[1].innerText;
            console.log(rows[i+1])
            nData.push(cellValueID);
        }
    }

    var uploadAjax = $.ajax({
      url:"/deleteInfo",
      type: "get",
      dataType: "text",
      data: JSON.stringify({"delInfo": nData}),
      contentType:"json/application",
      timeout:1500000,
      async: true,
      beforeSend: function () {
        $('#waitDel').html("请稍后...")
      },
      success: function (msg) {
          alert(msg);
          window.location.href = "/adminPage";
      },
      error: function(data) {
          alert(msg);
          $('#waitDel').html("")
      },
      complete: function (XMLHttpRequest, textStatus) {
          if(textStatus == 'timeout'){
              uploadAjax.abort(); 
              alert("请求超时，请重试")
          }
      }
    });
}

function startDevChoose(ele){
    const value = ele.getAttribute('value');
    console.log(value);
    var uploadAjax = $.ajax({
        url:"/startDev",
        type: "get",
        dataType: "text",
        headers: { 'from': '/chooseDev' },
        data: JSON.stringify({"chooseDev": value}),
        contentType:"json/application",
        timeout:1500000,
        async: true,
        success: function (msg) {
            alert(msg);
            window.location.href = "/Home";
        }
        ,
        error: function(msg) {
            alert(msg);
        }
        ,
        complete: function (XMLHttpRequest, textStatus) {
            if(textStatus == 'timeout'){
                uploadAjax.abort(); 
                alert("请求超时，请重试")
            }
        }
    });
}

function startDevNew(){
    var devName = document.getElementById('newDev').value;
    var devType = document.getElementById('type-select').value;
    console.log(devName);
    console.log(devType);
    var uploadAjax = $.ajax({
        url:"/startDev",
        type: "get",
        dataType: "text",
        headers: { 'from': '/newDev' },
        data: JSON.stringify({"devName":devName,"devType":devType}),
        contentType:"json/application",
        timeout:1500000,
        async: true,
        success: function (msg) {
            alert(msg);
            window.location.href = "/Home";
        }
        ,
        error: function(msg) {
            alert(msg);
        }
        ,
        complete: function (XMLHttpRequest, textStatus) {
            if(textStatus == 'timeout'){
                uploadAjax.abort(); 
                alert("请求超时，请重试")
            }
        }
    });
}

function turnBack() {
    window.location.href = "/adminPage";
}

function turnBackInit() {
    window.location.href = "/chooseDev";
}

function infoCard(){
    var detailedInfo = ["这是仅签到的详细信息","这是仅签退的详细信息","这是签到和签退的详细信息"];
    var typeSelect = document.getElementById("type-select");
    var detailedInfoElement = document.getElementById("detailed-info");

    typeSelect.addEventListener("change", function() {
        var selectedValue = typeSelect.options[typeSelect.selectedIndex].value;
        detailedInfoElement.innerHTML = detailedInfo[parseInt(selectedValue)-1];
    });
}

function searchUsers(){
    $(document).ready(function(){
        // 点击按钮时触发搜索功能
        $('#searchBtn').click(function(){
            var searchText = $('#searchInput').val().toLowerCase();
            $('#info tr').filter(function(){
                $(this).toggle($(this).text().toLowerCase().indexOf(searchText) > -1);
            });
        });
        
        // 在输入框中按下回车键时触发搜索功能
        $('#searchInput').keypress(function(e){
            if(e.which == 13){ // 回车键的键值为13
                $('#searchBtn').click(); // 触发搜索按钮的单击事件
            }
        });
    });
}

function select2del(){
    $(function(){  
        $("#info label").click(function() {
            if($(this).closest('tr').hasClass('selected')){
            $(this).closest('tr').removeClass('selected'); 
            }else{
            $(this).closest('tr').addClass('selected'); 
            }
        });
    }); 
}