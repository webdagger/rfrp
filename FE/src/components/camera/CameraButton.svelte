<script lang="ts">
    import { CameraIcon } from 'svelte-feather-icons';
    import { shown } from './stores.js';
</script>

<style lang="scss">
    @import '../../scss/variables';

    .cameraButton {
        width: 100%;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        box-sizing: content-box;
        text-align: center;
    }

    
</style>


<div class="cameraButton">
       <span>
           <CameraIcon size="4x" />
       </span>

       <p>Start Camera</p>
   
</div>