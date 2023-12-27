<script>
	import Login from '$lib/components/auth/Login.svelte';

	let isLoggedIn = false;
</script>

<svelte:head>
	<title>Home</title>
	<meta name="description" content="Svelte demo app" />
</svelte:head>

<section>
	<main>
		{#if !isLoggedIn}
			<Login />
		{:else}
			<h1>Welcome to the TerraSync!</h1>

			<!-- Placeholder for user-specific content -->
		{/if}
	</main>
</section>

<style>
	section {
		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;
		flex: 0.6;
	}

	h1 {
		width: 100%;
	}
</style>
