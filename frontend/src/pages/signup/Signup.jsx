import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./Signup.css";

const Signup = () => {
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);

  const handleSignup = () => {
    // Add your signup logic here
  };

  const handleTogglePassword = () => {
    setShowPassword(!showPassword);
  };

  const handleLogin = () => {
    navigate("/login");
  };

  return (
    <>
      <div className="home show">
        <div className="form_container active">
          <form action="#">
            <h2>Signup</h2>

            <div className="input_box">
              <input
                type="email"
                placeholder="Enter your email"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />
              <i className="uil uil-envelope-alt email"></i>
            </div>
            <div className="input_box">
              <input
                type={showPassword ? "text" : "password"}
                placeholder="Create password"
                required
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
              <i className="uil uil-lock password"></i>
              <i
                className="uil uil-eye-slash pw_hide"
                onClick={handleTogglePassword}
              ></i>
            </div>
            <div className="input_box">
              <input
                type={showPassword ? "text" : "password"}
                placeholder="Confirm password"
                required
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
              />
              <i className="uil uil-lock password"></i>
              <i
                className="uil uil-eye-slash pw_hide"
                onClick={handleTogglePassword}
              ></i>
            </div>

            <button className="button" onClick={handleSignup}>
              Signup Now
            </button>

            <div className="login_signup">
              Already have an account?{" "}
              <a href="#" id="login" onClick={handleLogin}>
                Login
              </a>
            </div>
          </form>
        </div>
      </div>
    </>
  );
};

export default Signup;
