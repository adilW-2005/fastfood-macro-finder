import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';

const Register = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const register = async (e) => {
    e.preventDefault();
    console.log("Attempting to register with:", { username, password });

    const response = await fetch("http://127.0.0.1:5000/auth/signup", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password }),
      credentials: "include",
    });

    const data = await response.json();
    console.log("Response JSON:", data);

    if (response.ok) {
      localStorage.setItem("user", JSON.stringify(data));
      console.log(`Registration successful. Logged in as ${username}`);
      navigate("/");
    } else {
      setError(data.error || "Registration failed. Please try again.");
      console.error("Registration error:", data.error);
    }
  };

  return (
    <div className="auth-container">
      <h2>Register</h2>
      {error && <p className="error">{error}</p>}
      <form onSubmit={register}>
        <input 
          type="text" 
          placeholder="Username" 
          value={username} 
          onChange={(e) => setUsername(e.target.value)} 
          required 
        />
        <input 
          type="password" 
          placeholder="Password" 
          value={password} 
          onChange={(e) => setPassword(e.target.value)} 
          required 
        />
        <button type="submit">Register</button>
      </form>
      <div className="auth-buttons">
        <Link to="/">
          <button className="secondary-btn">Go Back</button>
        </Link>
      </div>
    </div>
  );
};

export default Register;
