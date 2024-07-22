import { useState } from "react";
import {useNavigate} from "react-router-dom";
import axios from "axios";

function LoginForm({ route }) {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const navigate = useNavigate();

    const handleSubmit = async (event) => {
        event.preventDefault()

        try {
            const response = await axios.post(`https://localhost:8080/${route}/`, {username: username, password: password})
            console.log(response.data)
            navigate(response.data.redirect_url)
        } catch (error) {
            console.log(error)
        }
    }

    return(
        <form onSubmit={handleSubmit} className="form-container">
            <h1>Login</h1>
            <input
                className="form-input"
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                placeholder="Username"
            />
            <input
                className="form-input"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Password"
            />
            <button onSubmit={handleSubmit} className="form-button" type="submit">
                Login
            </button>
        </form>
    )
}

export default LoginForm;