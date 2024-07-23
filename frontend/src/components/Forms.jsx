import React, { useState } from 'react';
import { register, login } from '../services/userService';
import { useNavigate } from 'react-router-dom';
import '../styles/Form.css';

const LoginForm = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState({});
  const navigate = useNavigate();

    const validateForm = () => {
        let errors = {};
        let isValid = true;

        if (!username) {
            errors.username = 'Username is required';
            isValid = false;
        }

        if (!password) {
            errors.password = 'Password is required';
            isValid = false;
        }

        setError(errors);
        return isValid;
    };

  const handleSubmit = async (event) => {
      event.preventDefault();

      if (!validateForm()) {
          return;
      }

      const user = { username, password};
      const response = await login(user);

      if (response !== undefined) {
          localStorage.setItem('profile', response.profile);
          // navigate('/'); // TODO: uncomment this line after creating the Home Page
      } else {
          alert('Invalid username or password')
      }
  };

  return (
      <form onSubmit={handleSubmit} className="form-container">
          <h1>Login</h1>
          <h2>Welcome back</h2>

          {error.username && <p className="form-error">{error.username}</p>}
            <input
                className="form-input"
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                placeholder="Username"
            />
            {error.password && <p className="form-error">{error.password}</p>}
            <input
                className="form-input "
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Password"
            />

          <button className="form-button" type="submit">
              Login
          </button>
          <p>Don't have an account? <a className="form-link" href="/register">Sign Up</a></p>
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
    const [error, setError] = useState({});
    const navigate = useNavigate();

    const validateForm = () => {
        let errors = {};
        let isValid = true;

        if (!username) {
            errors.username = 'Username is required';
            isValid = false;
        }

        if (!password) {
            errors.password = 'Password is required';
            isValid = false;
        }

        if (!email.includes('@') && email) {
            errors.email = 'Invalid email';
            isValid = false;
        }

        setError(errors);
        return isValid;
    }

    const handlePasswordChange = (e) => {
        setPassword(e.target.value);
        if (e.target.value !== confirmPassword) {
            setError(prevErrors => ({ ...prevErrors, confirmPassword: 'Passwords do not match' }));
        } else {
            setError(prevErrors => {
                const { confirmPassword, ...rest } = prevErrors;
                return rest;
            });
        }
    };

    const handleConfirmPasswordChange = (e) => {
        setConfirmPassword(e.target.value);
        if (password !== e.target.value) {
            setError(prevErrors => ({ ...prevErrors, confirmPassword: 'Passwords do not match' }));
        } else {
            setError(prevErrors => {
                const { confirmPassword, ...rest } = prevErrors;
                return rest;
            });
        }
    };

    const handleSubmit = async (event) => {
        event.preventDefault();

        if (!validateForm()) {
            return;
        }

        const newUser = { username, password, first_name: firstName, last_name: lastName, email};
        const response = await register(newUser);
        if (response !== undefined) {
            alert('Registration successful');
            navigate('/login');
        } else {
            alert('Username already exists. Please try again.');
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
            {error.username && <p className="form-error">{error.username}</p>}
            <input
                className="form-input"
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                placeholder="Username"
            />
            {error.password && <p className="form-error">{error.password}</p>}
            <input
                className="form-input"
                type="password"
                value={password}
                onChange={handlePasswordChange}
                placeholder="Password"
            />
            {error.confirmPassword && <p className="form-error">{error.confirmPassword}</p>}
            <input
                className="form-input"
                type="password"
                value={confirmPassword}
                onChange={handleConfirmPasswordChange}
                placeholder="Confirm Password"
            />
            {error.email && <p className="form-error">{error.email}</p>}
            <input
                className="form-input"
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="Email"
            />

            <button className="form-button" type="submit">
                Sign Up
            </button>
            <p>Already have an account? <a className="form-link" href="/login">Login</a></p>
        </form>
    );
};

export {RegisterForm, LoginForm};