<script lang="ts">
    import CameraButton from './CameraButton.svelte';
    import CameraView from './CameraView.svelte';
    import { shown } from './stores.js';
    import { AlertCircleIcon } from 'svelte-feather-icons'
    import { onMount } from 'svelte';
    import { fade, fly } from 'svelte/transition';
    import DataForm from './DataForm.svelte';
    let pageReady = false
    let modalNeeded : bool = false;

    function collectData (e){
        if (pageReady === true){
            pageReady = false;
            modalNeeded = true;
        }
        }
    
    onMount(() => pageReady = true);
</script>

<style lang="scss">
    @import '../../scss/variables';
    .camera {
        display: flex;
        flex-direction: column;

    }

    .placeholder {
        background-color: $background;
        width: 100%;
        height: 70vh;
        text-align: center;
    }

    .cameraview {
        width: 100%;
        height: 70vh;

    }

    .camerabutton {
        margin-top: 2rem;
        width: 100%;
        height: 10vh;
    }

    .hidden {
        display: none;
    }
    .about {
        @media  (min-width: $tablet) {
            margin-top: 3rem;
        }
        h1 {
            font-family: $heading-font-family;
            line-height: $heading-line-height;
            color: $heading-font-color;
            font-weight: $heading-font-weight;
        }
        p {
            font-weight: $font-weight;
            font-family: $font-family;
            font-size: $body-font-size;
            color: $font-color;
            line-height: $line-height;

        }

        code {
            color: $code-color;
            font-size: $code-size;
            font-family: $code-family;
            background-color: $code-background;
            border: $code-borders;
        }
    }
    .notice {
        margin-top: 2rem;

    }
    .disclaimer {
        display: flex;
        flex-direction: row;
        justify-content: center;
        align-items: center;
        
        span {
            color: $warning;
            animation: shake 0.82s cubic-bezier(.36, .07, .19, .97) both;
            animation-iteration-count: 10; 
            transform: translate3d(0, 0 , 0);
            backface-visibility: hidden;
            perspective: 1000px;
        }

        @keyframes shake {
            10%, 90% {
                 transform: translate3d(-1px, 0, 0);
                }
  
            20%, 80% {
                transform: translate3d(2px, 0, 0);
                }

            30%, 50%, 70% {
                transform: translate3d(-4px, 0, 0);
            }

            40%, 60% {
                transform: translate3d(4px, 0, 0);
            }
            
        }
        h2 {
            padding-left: 0.5rem;

        }
      
    }
    strong {
            font-size: 1.5rem;
        }
    .illegal {
        color: $warning;
    }

    .modal {
       width: 300px;
       height: 70%;
       margin:0 auto;
       display:table;
       position: absolute;
       left: 0;
       right:0;
       top: 50%; 
       border:1px solid;
       -webkit-transform:translateY(-50%);
       -moz-transform:translateY(-50%);
       -ms-transform:translateY(-50%);
       -o-transform:translateY(-50%);
       transform:translateY(-50%);
    }
</style>




<div class="camera">
       {#if pageReady}
       <div transition:fly="{{ x: 300, duration: 2000 }}" class="placeholder">
        <div class="about">
         <h1>Web FaceRecognition</h1>
         <h2>Hi!</h2>
         <p>This is a demo project cobbled together using <code>Python</code> and <code>Svelte</code> .</p>
        </div>

        <div class="notice">
            <div class="disclaimer">
                <span>
                 <AlertCircleIcon size='2x' />
                </span>
            
                 <h2>Disclaimer!</h2>
            </div>
            
            <p>This is only for educational purposes. I bear no responsibility on how you use the code.</p>
            <p><strong>Note</strong> <br />This Website, uses your camera to detect and attempt to recognize a human face. <br />
             This might be <span class="illegal">illegal</span> in some countries without consent.</p>
             <p>Being said, clicking the start button and allowing the camera permission is considered as you giving consent.</p>
             <p>Use the delete button to remove all face data stored for you.</p>
        </div>


    </div>
       {/if}
       <div class="cameraview hidden">
            <CameraView />
        </div>
        {#if pageReady}

        <div transition:fly="{{y: 200, duration:2000}}" class="camerabutton">
            <button on:click="{ collectData }">Give test data.</button>
        </div>

        {/if}

        {#if modalNeeded}
        <div
        transition:fade
        class="modal">
            <DataForm />
        </div>
        {/if}
        
        
</div>
