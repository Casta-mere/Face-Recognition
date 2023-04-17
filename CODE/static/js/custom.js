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

function turnBack() {
    window.location.href = "/";
}

function sendBack(){
    var name = document.getElementById("name").value
    var email = document.getElementById("email").value
    console.log(name)
    console.log(email)
    var uploadAjax = $.ajax({
        url:'/sendInfo',
        type: 'get',
        dataType: "text",
        data: JSON.stringify({"name": name, "email": email}),
        contentType:'json/application',
        timeout:10000,
        async: true,
        beforeSend: function () {
            $("#waitA").html("正在发送，请稍后...");
        },
        success: function (msg) {
            alert(msg)
            window.location.href = "/";
        },
        error: function(msg) {
            alert(msg)
        },
        complete: function (XMLHttpRequest, textStatus) {
            if(textStatus == 'timeout'){
                uploadAjax.abort(); 
                alert("请求超时，请重试")
            }
        }
    });
}

//first page
function getState(){
    $.ajax({
        url: "/getState",
        type: "get",
        timeout: 10000,
        success: function(msg){
          $('#rcg').html(msg)
      },
      });
  }
  setInterval(getState, 400)

//manageInfo
function turnToDel() {
    var nData = document.getElementById('delName').value;
    console.log(nData);
    var uploadAjax = $.ajax({
      url:"/deleteInfo",
      type: "get",
      dataType: "text",
      data: JSON.stringify({"delName": nData}),
      contentType:"json/application",
      timeout:10000,
      async: true,
      beforeSend: function () {
        $('#waitDel').html("请稍后...")
      },
      success: function (msg) {
          alert(msg);
          window.location.href = "/adminPage";
      },
      error: function(msg) {
          alert(msg);
      },
      complete: function (XMLHttpRequest, textStatus) {
          if(textStatus == 'timeout'){
              uploadAjax.abort(); 
              alert("请求超时，请重试")
          }
      }
  });
  }

function turnBack() {
    window.location.href = "/";
}

