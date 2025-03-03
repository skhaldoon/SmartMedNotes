import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { signInWithEmailAndPassword, signInWithPopup, sendPasswordResetEmail } from "firebase/auth";
import { auth, googleProvider } from "../../firebase";  // Import Firebase auth
import "./Login.css";
import Home from "../../pages/home/Home";

const Login = () => {
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [rememberMe, setRememberMe] = useState(false);
  const [error, setError] = useState("");
  const [resetMessage, setResetMessage] = useState(""); // Added state for reset message

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      await signInWithEmailAndPassword(auth, email, password);
      if (rememberMe) {
        localStorage.setItem("userEmail", email);
      } else {
        localStorage.removeItem("userEmail");
      }
      navigate(Home);  // Redirect to Home after login
    } catch (err) {
      setError("Invalid email or password.");
    }
  };

  const handleGoogleLogin = async () => {
    try {
      await signInWithPopup(auth, googleProvider);
      navigate(Home);
    } catch (err) {
      setError("Google sign-in failed.");
    }
  };

  const handleForgotPassword = async () => {
    if (!email) {
      setError("Enter your email to reset password.");
      return;
    }
    try {
      await sendPasswordResetEmail(auth, email);
      setResetMessage("Password reset link sent to your email.");
      setError(""); // Clear error if successful
    } catch (err) {
      setError("Failed to send reset email.");
    }
  };

  return (
    <div className="home show">
      <div className="form_container active">
        <form onSubmit={handleLogin}>
          <h2>Login</h2>

          {error && <p className="error">{error}</p>}
          {resetMessage && <p className="success">{resetMessage}</p>} {/* Display success message */}

          <div className="input_box">
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="Enter your email"
              required
            />
          </div>

          <div className="input_box">
            <input
              type={showPassword ? "text" : "password"}
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Enter your password"
              required
            />
            <span className="toggle_password" onClick={() => setShowPassword(!showPassword)}>
              {showPassword ? "👁️" : "🙈"}
            </span>
          </div>

          <div className="option_field">
            <div className="checkbox">
              <input
                type="checkbox"
                id="remember"
                checked={rememberMe}
                onChange={() => setRememberMe(!rememberMe)}
              />
              <label htmlFor="remember">Remember me</label>
            </div>
            <button type="button" onClick={handleForgotPassword} className="forgot_password" style={{ color: "red" }}>
              Forgot Password?
            </button>
          </div>

          <button type="submit" className="button">Login</button>
          <button type="button" className="button google" onClick={handleGoogleLogin}>
            Login with Google
          </button>
        </form>
      </div>
    </div>
  );
};

export default Login;