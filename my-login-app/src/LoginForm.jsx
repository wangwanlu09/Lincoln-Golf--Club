import React, { useState } from 'react';
import axios from 'axios';

const LoginForm = () => {
  const [email, setEmail] = useState('');
  const [membernum, setMembernum] = useState('');
  const [password, setPassword] = useState('');
  const [msg, setMsg] = useState('');

  const handleSubmit = async (event) => {
    event.preventDefault();

    try {
      const response = await axios.post('http://localhost:5000/login/', {
        email,
        membernum,
        password,
      });

      if (response.data.success) {
        window.location.href = response.data.redirect_url;
      } else {
        setMsg(response.data.message);
      }
    } catch (error) {
      console.error('There was an error logging in!', error);
      setMsg('An error occurred. Please try again.');
    }
  };

  return (
    <div className="container d-flex justify-content-center align-items-center vh-100">
      <div className="col-md-4">
        <h3 className="container d-flex justify-content-center fw-bold mb-3 text-secondary">Log In</h3>
        <form onSubmit={handleSubmit}>
          <div className="form-outline mb-4">
            <input
              type="email"
              name="email"
              id="emailLoginForm"
              className="form-control"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
            <label className="form-label" htmlFor="email">Email address</label>
          </div>
          <div className="form-outline mb-4">
            <input
              type="password"
              name="password"
              id="password"
              className="form-control"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
            <label className="form-label" htmlFor="password">Password</label>
          </div>
          <div className="row mb-4">
            <div className="col d-flex justify-content-center">
              <div className="form-check">
                <input
                  className="form-check-input"
                  type="checkbox"
                  value=""
                  id="rememberme"
                  name="rememberme"
                  defaultChecked
                />
                <label className="form-check-label" htmlFor="rememberme">
                  Remember me
                </label>
              </div>
            </div>
            <div className="col">
              <a href="/forgotpassword">Forgot password?</a>
            </div>
          </div>
          <button type="submit" className="btn custom-btn btn-block mb-4 container d-flex justify-content-center">
            Log in
          </button>
          {msg && <div className="alert alert-danger">{msg}</div>}
          <div className="text-center">
            <p>Not a member? <a href="/register">Register</a></p>
          </div>
        </form>
      </div>
    </div>
  );
};

export default LoginForm;


