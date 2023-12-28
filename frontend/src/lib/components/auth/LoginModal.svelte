<script lang="ts">
    import { isAuthenticated, userGroups } from './store.js';
    import { createEventDispatcher } from 'svelte';

    const dispatch = createEventDispatcher();
    let username = '';
    let password = '';
    let message = '';
    let showOverlay = false;

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

{#if showOverlay}
    <div class="login-modal">
        <form on:submit|preventDefault={handleLogin}>
            <div>
                <input type="text" id="username" bind:value={username} required placeholder="Enter your username" />
            </div>
            <div>
                <input type="password" id="password" bind:value={password} required placeholder="Enter your password" />
            </div>
            <button type="submit">Login</button>
            {#if message}
                <p class="error">{message}</p>
            {/if}
        </form>
        <button on:click={() => { showOverlay = false; }}>Close</button>
    </div>
    <div class="overlay"></div>
{/if}

<style>
    .login-modal {
        /* Styling for login modal */
        position: fixed;  /* Make the modal fixed */
        top: 0;  /* Position it at the top of the page */
        right: 0;  /* Position it at the right of the page */
        z-index: 1000;  /* Ensure it appears on top of other elements */
        padding-top: 10px;
        padding-right: 10px;
    }
    .error {
        color: red;
    }
    .overlay {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(0, 0, 0, 0.5);
        z-index: 999;  /* Ensure the overlay appears below the modal */
    }
    #username, #password {
        margin-bottom: 10px;
        border-radius: 15px;
        text-align: center;
    }
</style>

