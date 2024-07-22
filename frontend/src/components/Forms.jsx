import React, { useState } from 'react';
import { register, login } from '../services/userService';
import { useNavigate } from 'react-router-dom';
import '../styles/Form.css';

const LoginForm = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
    const navigate = useNavigate();

  const handleSubmit = async (event) => {
    event.preventDefault();
    const user = { username: username, password: password};
    const response = await login(user);

    if (response !== undefined) {
      localStorage.setItem('user', response.user);
      // navigate('/'); // TODO: uncomment this line after creating the Home Page
    } else {
        alert('Invalid username or password')
    }
  };

  return (
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
          <button className="form-button" type="submit">
              Login
          </button>
      </form>
  );
};

const RegisterForm = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [firstName, setFirstName] = useState('');
    const [lastName, setLastName] = useState('');
    const [email, setEmail] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');

    const handleSubmit = async (event) => {
        event.preventDefault();
        if (password !== confirmPassword) {
            // handle password mismatch here
            return;
        }
        const newUser = {username, password};
        const response = await register(newUser);
        if (response.status === 201) {
            // handle successful registration here
        } else {
            // handle registration error here
        }
    };

    return (
        <form onSubmit={handleSubmit} className="form-container">
            <h1>Sign Up</h1>
            <h2>Create your account</h2>
            <input
                className="form-input"
                type="text"
                value={firstName}
                onChange={(e) => setFirstName(e.target.value)}
                placeholder="First Name"
            />
            <input
                className="form-input"
                type="text"
                value={lastName}
                onChange={(e) => setLastName(e.target.value)}
                placeholder="Last Name"
            />
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
            <input
                className="form-input"
                type="password"
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                placeholder="Confirm Password"
            />
            <input
                className="form-input"
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="Email"
            />
            <button className="form-button" type="submit">
                Login
            </button>
            <p>Already have an account? <a href="/login">Login</a></p>
        </form>
    );
};

export {RegisterForm, LoginForm};