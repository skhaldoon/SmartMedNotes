import "./index.css";
import { React, useState } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import reactLogo from "./assets/react.svg";
import viteLogo from "/vite.svg";
import "./App.css";
import Home from "./pages/home/Home";
import Login from "./pages/login/Login";

import Signup from "./pages/signup/Signup";
import ChatInterface from "./pages/chatInterface/chatInterface";

function App() {
  return (
    <>
      <Router>
        <Routes>
          <Route path="/" element={<ChatInterface />} />
          <Route path="/login" element={<Login />} />
          <Route path="/signup" element={<Signup />} />
        </Routes>
      </Router>
    </>
  );
}

export default App;
