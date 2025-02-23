import "./index.css";
import { React, useState, useEffect } from "react";
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import { auth } from "./firebase";  // Import Firebase auth
import Home from "./pages/home/Home";
import Login from "./pages/login/Login";
import Contact from "./pages/contact/Contact";
import Signup from "./pages/signup/Signup";
import Navbar from "./pages/navbar/Navbar";
import Assistant from "./pages/assistant/Assistant";
import About from "./pages/about/About";
import Footer from "./pages/footer/Footer";

function App() {
  const [user, setUser] = useState(null);

  useEffect(() => {
    const unsubscribe = auth.onAuthStateChanged((user) => {
      setUser(user);
    });
    return () => unsubscribe();
  }, []);

  return (
    <Router>
      <Navbar />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/login" element={user ? <Navigate to="/" /> : <Login />} />
        <Route path="/signup" element={user ? <Navigate to="/" /> : <Signup />} />
        <Route path="/contact" element={<Contact />} />
        <Route path="/assistant" element={user ? <Assistant /> : <Navigate to="/login" />} />
        <Route path="/about" element={<About />} />
        <Route path="/footer" element={<Footer />} />
      </Routes>
      <Footer />
    </Router>
  );
}

export default App;