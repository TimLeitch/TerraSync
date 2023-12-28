<script lang="ts">
	import { isAuthenticated, userGroups } from '$lib/components/auth/store.js';

	let isLoggedIn: boolean;
	let groups;

	// Subscribe to the store values
	isAuthenticated.subscribe((value) => {
		isLoggedIn = value;
	});

	userGroups.subscribe((value) => {
		groups = value;
	});
</script>

<svelte:head>
	<title>Home</title>
	<meta name="description" content="Svelte demo app" />
</svelte:head>

<section>
	<main>
		{#if !isLoggedIn}
			<h1>Please log in</h1>
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
