const videoPreview = document.getElementById('video-preview');
navigator.mediaDevices.getUserMedia({ video: true })
  .then(stream => {
    videoPreview.srcObject = stream;
    videoPreview.play();
    console.log("played");
  })
  .catch(error => {
    console.error(error);
  });
// let socket = new WebSocket('ws://192.168.102.148:8888');
let socket = new WebSocket('ws://192.168.121.33:8888');
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

