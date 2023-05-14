const videoPreview = document.getElementById('video-preview');
while (true) {
  try {
    navigator.mediaDevices.getUserMedia({ video: true })
      .then(stream => {
        videoPreview.srcObject = stream;
        videoPreview.play();
        console.log("played");
      })
    break
  } catch(error) {
    console.error(error);
  }
}

let ip=Server.ip

// 定义函数用于连接 socket
function connect() {
  let socket = new WebSocket(ip);
  // 监听连接成功事件
  socket.onopen = function() {
    console.log('Socket已连接');
  };
  // 监听连接失败事件
  socket.onerror = function() {
    console.log('连接失败，3秒后重试');
    setTimeout(function() {
      connect(); // 延迟3秒后再次尝试连接
    }, 3000);
  };
}

// 调用连接函数
connect();

//shake hands with server :send hello
socket.onopen = function (event) {
    socket.send("hello");
    //receive message from server,if message is "123",start sending video frames
    socket.onmessage = function (event) {
        if (event.data == "123") {
            console.log("123");
            sendFrame();
        }
    }
}
// Get the video frames to send to the server
function sendFrame() {var canvas = document.createElement('canvas');
  var context = canvas.getContext('2d');
  canvas.width = videoPreview.videoWidth;
  canvas.height = videoPreview.videoHeight;
  context.drawImage(videoPreview, 0, 0, canvas.width, canvas.height);
  var dataURL = canvas.toDataURL('image/jpeg', 0.5);
  socket.send(dataURL);
  setTimeout(sendFrame, 100);
}

