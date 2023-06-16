new Vue({
  el: '#app',
  data: {
    numAcne: null,
    acneLevel: null,
    previewImage: '',
    showCamera: false
  },
  methods: {
    handleFileUpload(event) {
      const file = event.target.files[0];
      this.previewImage = URL.createObjectURL(file);
    },
    upload() {
      if (this.previewImage) {
        const formData = new FormData();
        const blob = this.dataURLtoBlob(this.previewImage);
        if (blob) {
          formData.append('image', blob);

          axios.post('/detect', formData, {
            headers: {
              'Content-Type': 'multipart/form-data'
            }
          }).then(response => {
            this.numAcne = response.data.num_acne;
            this.acneLevel = response.data.acne_level;
          }).catch(error => {
            console.error(error);
          });
        }
      }
    },
    capture() {
      const video = document.getElementById('video-player');
      const canvas = document.createElement('canvas');
      canvas.width = 300;
      canvas.height = 300;
      const context = canvas.getContext('2d');
      context.drawImage(video, 0, 0, canvas.width, canvas.height);
      this.previewImage = canvas.toDataURL('image/jpeg');
    },
    toggleCamera() {
      const video = document.getElementById('video-player');
      if (this.showCamera) {
        // Matikan kamera
        const stream = video.srcObject;
        const tracks = stream.getTracks();
        tracks.forEach(track => track.stop());
        video.srcObject = null;
      } else {
        // Nyalakan kamera
        navigator.mediaDevices.getUserMedia({ video: true })
          .then(stream => {
            video.srcObject = stream;
          })
          .catch(error => {
            console.error('Error accessing webcam: ', error);
          });
      }
      this.showCamera = !this.showCamera;
    },
    dataURLtoBlob(dataURL) {
      try {
        const byteString = atob(dataURL.split(',')[1]);
        const mimeString = dataURL.split(',')[0].split(':')[1].split(';')[0];
        const ab = new ArrayBuffer(byteString.length);
        const ia = new Uint8Array(ab);
        for (let i = 0; i < byteString.length; i++) {
          ia[i] = byteString.charCodeAt(i);
        }
        return new Blob([ab], { type: mimeString });
      } catch (error) {
        console.error('Error converting data URL to blob: ', error);
        return null;
      }
    }
  }
});
