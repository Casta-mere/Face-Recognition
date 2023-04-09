const videoPreview = document.getElementById('video-preview');

navigator.mediaDevices.getUserMedia({ video: true })
  .then(stream => {
    videoPreview.srcObject = stream;
    videoPreview.play();
  })
  .catch(error => {
    console.error(error);
  });