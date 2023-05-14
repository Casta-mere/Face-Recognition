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

  function connect() {
    socket = new WebSocket(ip);
    socket.onopen = function(event) {
      socket.send("hello");
      console.log('WebSocket connected');
    };
    socket.onmessage = function(event) {
      if (event.data == "123") {
        console.log("123");
        sendFrame();
    }
    };
    socket.onerror = function(event) {
      console.error('WebSocket error: ', event);
    };
    socket.onclose = function(event) {
      console.warn('WebSocket closed, reconnecting in 1000ms...');
      setTimeout(connect, 1000);
    };
  }

  connect();

  // Get the video frames to send to the server
  function sendFrame() {
    var canvas = document.createElement('canvas');
    var context = canvas.getContext('2d');
    canvas.width = videoPreview.videoWidth;
    canvas.height = videoPreview.videoHeight;
    context.drawImage(videoPreview, 0, 0, canvas.width, canvas.height);
    var dataURL = canvas.toDataURL('image/jpeg', 0.5);
    if (socket.readyState === WebSocket.OPEN) { // 只有socket状态为OPEN时才发送数据
      socket.send(dataURL);
    }
    setTimeout(sendFrame, 100);
  }

