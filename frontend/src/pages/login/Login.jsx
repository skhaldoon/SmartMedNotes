import React, { useState } from "react";
import "./Login.css";
import { useNavigate } from "react-router-dom";

import "@fortawesome/fontawesome-free/css/all.min.css";

const Login = () => {
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);

  const handleLogin = (e) => {
    e.preventDefault();
    // Add your login logic here
    console.log("Logging in with:", email, password);
  };

  const handleTogglePassword = () => {
    setShowPassword(!showPassword);
  };

  const handleForgotPassword = (e) => {
    e.preventDefault();
    // Add your forgot password logic here
    console.log("Forgot password clicked");
  };

  const handleSignup = (e) => {
    e.preventDefault();
    navigate("/signup");
  };

  return (
    <div className="home show">
      <div className="form_container active">
        <form onSubmit={handleLogin}>
          <h2>Login</h2>

          <div className="input_box">
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="Enter your email"
              required
            />
            <i className="uil uil-envelope-alt email"></i>
          </div>

          <div className="input_box">
            <input
              type={showPassword ? "text" : "password"}
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Enter your password"
              required
            />
            <i className="uil uil-lock password"></i>
            <i
              className={`uil ${
                showPassword ? "uil-eye" : "uil-eye-slash"
              } pw_hide`}
              onClick={handleTogglePassword}
            ></i>
          </div>

          <div className="option_field">
            <span className="checkbox">
              <input type="checkbox" id="check" />
              <label htmlFor="check">Remember me</label>
            </span>
            <a href="#" className="forgot_pw" onClick={handleForgotPassword}>
              Forgot password?
            </a>
          </div>

          <button type="submit" className="button">
            Login Now
          </button>

          <div className="login_signup">
            Don't have an account?{" "}
            <a href="#" id="signup" onClick={handleSignup}>
              Signup
            </a>
          </div>
        </form>
      </div>
    </div>
  );
};

export default Login;
