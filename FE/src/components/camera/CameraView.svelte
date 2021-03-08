<script lang="ts">
  // https://github.com/samdutton/simpl/blob/gh-pages/imagecapture/js/main.js
    import { onMount } from 'svelte';
    import { shown } from './stores.js';

    const constraints = {
      video:{
        width: {
          min: 1280,
          ideal: 1920,
          max: 2560,
        },
        height: {
        min: 720,
          ideal: 1080,
          max: 1440
        },
        facingMode: 'user'
      }
       
      }


    onMount ( async () => {
      let canvas = document.querySelector('canvas');
      let video = document.querySelector('video');
      let image = document.querySelector('img');
      let mediaStream;

      //let isSecureOrigin = location.protocol === 'https:' || location.host === 'localhost';
      //if(!isSecureOrigin){
      //  alert('Must be run from a secure origin: HTTPS');
      //  location.protocol = 'HTTPS';
      //}

      function hasGetUserMedia() {
        return !!(navigator.mediaDevices && navigator.mediaDevices.getUserMedia);
      }
      if (hasGetUserMedia()) {
        navigator.mediaDevices.enumerateDevices()
        .then(getStream)
        .catch(error => {
          console.log(error)
        });

    } else {
    alert("mediaDevices or getUserMedia() is not supported by your browser");
    }

    function getStream () {
      navigator.mediaDevices.getUserMedia(constraints)
      .then(gotStream)
      .catch(error => {
        console.log('getUserMedia error: ', error);
      })
    }

    function gotStream(stream) {
      console.log('getUserMedia() got stream: ', stream);
      mediaStream = stream;
      video.srcObject = stream;
      video.classList.remove('hidden');
      video.onloadedmetadata = function(e) {
        video.play();
      };
      // show video
      //imageCapture = new ImageCapture(stream.getVideoTracks()[0]);

    }

  })

</script>


<style lang="scss">
  .container{
    width: 100%;
    height: 100%;
  }

  .hidden {
    display: none;
  }

  #video {
    width: 100%;
    height: 100%;
    
  }
</style>
<div class="container">
    <!-- svelte-ignore a11y-media-has-caption -->
    <video class="hidden" playsinline id="video">

    </video>
  <div class="photo">
    <!-- svelte-ignore a11y-missing-attribute -->
    <img class="hidden" id="image" /> 
    
    <canvas class="hidden" id="canvas"></canvas>
  </div>
  

</div>

