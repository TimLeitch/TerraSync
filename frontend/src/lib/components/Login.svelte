<script>
let username = '';
let password = '';

const handleLogin = () => {
    //TODO: Add login logic
}

const handleRegister = () => {
    //TODO: Add register logic
}

const handleMouseOver = () => {
    
}
</script>

<div class="login-container" on:mouseover={handleMouseOver}>
    <h2>Login</h2>
    <form on:submit|preventDefault={handleLogin}>
        <div class="input-container">
            <label for="username">Username</label>
            <input type="text" id="username" bind:value={username} />
        </div>
        <div class="input-container">
            <label for="password">Password</label>
            <input type="password" id="password" bind:value={password} />
        </div>
        <div class="button-container">
            <button type="submit">Login</button>
        </div>
    </form>
</div>

<style>
.login-container {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    flex: 0.6;
    border: 1px solid rgba(0, 0, 0, 0.2);
    border-radius: 8px;
    padding: 1rem;
    box-shadow: 0 30px 50px rgba(0, 0, 0, 0.1);
}
    


.input-container {
    display: flex;
    flex-direction: column;
    margin: 0.5rem;
}

input, button {
    margin: 0.5rem;
}    
.button-container {
    display: flex;
    justify-content: center;
    align-items: center;
}
</style>
