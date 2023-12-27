<script>
    import { isAuthenticated } from '$lib/components/auth/store';
    let username = '';
    let password = '';
    let message = '';

    async function handleLogin() {
        try {
            const response = await fetch('http://localhost:8000/token', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: `username=${username}&password=${password}`
            });
            if (response.ok) {
                isAuthenticated.set(true); // Update auth state
            }

            const data = await response.json();
            console.log('Login successful:', data);

            // Store the token in localStorage
            localStorage.setItem('token', data.access_token);

            console.log('Token stored in localStorage:', localStorage.getItem('token'));
            // Redirect to another page or update the state
            // window.location.href = '/dashboard'; // Example redirection

        } catch (error) {
            message = error.message;
            console.error('Login failed:', error);
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
            <input type="text" id="username" bind:value={username} required>
        </div>
        <div>
            <label for="password">Password:</label>
            <input type="password" id="password" bind:value={password} required>
        </div>
        <button type="submit">Login</button>
        {#if message}
            <p>{message}</p>
        {/if}
    </form>
{/if}

