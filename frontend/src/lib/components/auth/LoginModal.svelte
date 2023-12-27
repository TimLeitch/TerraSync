<script lang="ts">
    import { isAuthenticated, userGroups } from './store.js';
    import { createEventDispatcher } from 'svelte';

    const dispatch = createEventDispatcher();
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
                dispatch('close'); // Emit event to close modal
            } else {
                message = 'Invalid username or password';
            }
        } catch (error) {
            message = 'Login failed';
        }
    }
    function parseJwt(token: string) {
    try {
        const base64Url = token.split('.')[1];
        const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
        const jsonPayload = decodeURIComponent(atob(base64).split('').map(function(c) {
            return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
        }).join(''));

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

<div class="login-modal">
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
            <p class="error">{message}</p>
        {/if}
    </form>
    <button on:click={() => dispatch('close')}>Close</button>
</div>

<style>
    .login-modal {
        /* Styling for login modal */
    }
    .error {
        color: red;
    }
</style>