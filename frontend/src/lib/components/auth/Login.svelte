<script lang="ts">
	import { isAuthenticated, userGroups } from './store.js';
	let username = '';
	let password = '';
	let message = '';

	async function handleLogin() {
		try {
			const response = await fetch('http://localhost:8000/token', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/x-www-form-urlencoded'
				},
				body: `username=${username}&password=${password}`
			});
			if (response.ok) {
				const data = await response.json();
				const decodedToken = parseJwt(data.access_token);
				userGroups.set(decodedToken.groups || []); // Update groups store
				isAuthenticated.set(true);
				// ... other login success logic
			}

			const data = await response.json();
			console.log('Login successful:', data);

			// Store the tokens in localStorage
			localStorage.setItem('accessToken', data.access_token);
			localStorage.setItem('refreshToken', data.refresh_token);

			console.log('Token stored in localStorage:', localStorage.getItem('token'));
			// Redirect to another page or update the state
			// window.location.href = '/dashboard'; // Example redirection
		} catch (error) {
			if (error instanceof Error) {
				message = error.message;
				console.error('Login failed:', error);
			}
		}
	}
	function parseJwt(token: string) {
		try {
			const base64Url = token.split('.')[1];
			const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
			const jsonPayload = decodeURIComponent(
				atob(base64)
					.split('')
					.map(function (c) {
						return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
					})
					.join('')
			);

			return JSON.parse(jsonPayload);
		} catch (e) {
			return null;
		}
	}
	function handleLogout() {
		localStorage.removeItem('token');
		isAuthenticated.set(false);
	}
</script>

{#if $isAuthenticated}
	<button on:click={handleLogout}>Logout</button>
{:else}
	<form on:submit|preventDefault={handleLogin}>
		<div>
			<label for="username">Username:</label>
			<input type="text" id="username" bind:value={username} required />
		</div>
		<div>
			<label for="password">Password:</label>
			<input type="password" id="password" bind:value={password} required />
		</div>
		<button type="submit">Login</button>
		{#if message}
			<p>{message}</p>
		{/if}
	</form>
{/if}
