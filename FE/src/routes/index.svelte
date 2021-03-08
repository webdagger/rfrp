<script lang="ts">
	import Camera from '../components/camera/Camera.svelte'
</script>
<svelte:head>
	<title>Face Recogition</title>
</svelte:head>

<style lang="scss">
	 @import '../scss/variables';
div {
	background-color: $background;
	width: 100vw;
	height: 100vh;

}
</style>

<div>
	<Camera />
	
</div>
