import React from "react";
import "tailwindcss/tailwind.css";
import { useNavigate } from "react-router-dom";
// import "./Home.css";
const Home = () => {
  const navigate = useNavigate();
  const handleLoginClick = () => {
    navigate("/Login");
  };
  const handleSignupClick = () => {
    navigate("/Signup");
  };

  return (
    <div className="w-full m-0 p-0 box-border overflow-x-hidden">
      {/* Navbar */}
      <nav className="bg-blue-700 p-4 sticky top-0 z-10 flex flex-wrap justify-between items-center">
        <div className="text-white text-2xl font-bold">
          Smart MED Notes
        </div>
        <div className="flex space-x-4">
          <a href="#about" className="text-white hover:text-teal-400">
            About
          </a>
          <a href="#testimonials" className="text-white hover:text-teal-400">
            Testimonials
          </a>
          <a href="#contact" className="text-white hover:text-teal-400">
            Contact
          </a>
        </div>
        <div onClick={handleSignupClick} className="flex space-x-2">
          <button className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700">
            Sign Up
          </button>
          <button
            onClick={handleLoginClick}
            className="bg-orange-600 text-white px-4 py-2 rounded hover:bg-orange-700"
          >
            Log In
          </button>
        </div>
      </nav>

      {/* Sections */}
      <div
        id="home"
        className="w-full min-h-screen flex flex-col justify-center items-center bg-blue-50 text-center py-8"
      >
        <h1 className="text-4xl font-bold mb-4">
          Welcome to Generative AI Doctor Assistant
        </h1>
        <p className="text-lg max-w-md">Your ultimate healthcare solution!</p>
      </div>

      <div
        id="about"
        className="w-full min-h-screen flex flex-col justify-center items-center bg-blue-100 text-center py-8"
      >
        <h1 className="text-4xl font-bold mb-4">About Us</h1>
        <p className="text-lg max-w-md">
          Learn how we are revolutionizing healthcare with AI-powered solutions.
        </p>
      </div>

      <div
        id="testimonials"
        className="w-full min-h-screen flex flex-col justify-center items-center bg-blue-200 text-center py-8"
      >
        <h1 className="text-4xl font-bold mb-4">Testimonials</h1>
        <p className="text-lg max-w-md">
          Hear what our users have to say about their experience.
        </p>
      </div>

      <div
        id="contact"
        className="w-full min-h-screen flex flex-col justify-center items-center bg-blue-300 text-center py-8"
      >
        <h1 className="text-4xl font-bold mb-4">Contact Us</h1>
        <p className="text-lg max-w-md">
          Reach out for support or to learn more about our services.
        </p>
      </div>
    </div>
  );
};

export default Home;
