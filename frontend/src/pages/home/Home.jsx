import React from "react";
import { Link, useNavigate } from "react-router-dom";

const Home = () => {
  const navigate = useNavigate();

  const handleLoginClick = () => {
    navigate("/Login");
  };
  const handleSignupClick = () => {
    navigate("/Signup");
  };

  return (
    <div className="w-full">
      {/* Navbar */}
      <nav className="bg-blue-700 sticky top-0 z-50 p-4 flex flex-wrap items-center justify-between">
        <div className="text-white text-xl md:text-2xl font-bold">
          Smart MED Notes
        </div>
        {/* Navigation Links */}
        <div className="flex flex-wrap space-x-2 md:space-x-4 text-sm md:text-base">
          <Link to="/" className="text-white hover:text-teal-400">
            Home
          </Link>
          <Link to="/ChatInterface" className="text-white hover:text-teal-400">
            Assistant
          </Link>
          <Link to="/About" className="text-white hover:text-teal-400">
            About Us
          </Link>
          <Link to="/Contact" className="text-white hover:text-teal-400">
            Contact
          </Link>
        </div>
        {/* Buttons */}
        <div className="flex flex-wrap space-x-2 mt-2 md:mt-0">
          <button
            onClick={handleSignupClick}
            className="bg-green-600 text-white px-3 py-2 text-sm md:text-base rounded hover:bg-green-700"
          >
            Sign Up
          </button>
          <button
            onClick={handleLoginClick}
            className="bg-orange-600 text-white px-3 py-2 text-sm md:text-base rounded hover:bg-orange-700"
          >
            Log In
          </button>
        </div>
      </nav>

      {/* Content Sections */}
      <div className="min-h-screen bg-blue-50 flex flex-col items-center justify-center text-center px-4">
        <h1 className="text-2xl md:text-4xl font-bold mb-4">
          Welcome to Smart MED Notes
        </h1>
        <p className="text-base md:text-lg max-w-xl">
          Your ultimate healthcare solution!
        </p>
      </div>
      <div className="min-h-screen bg-blue-300 flex flex-col items-center justify-center text-center px-4">
        <h1 className="text-2xl md:text-4xl font-bold mb-4">Contact Us</h1>
        <p className="text-base md:text-lg max-w-xl">
          Reach out for support or to learn more about our services.
        </p>
      </div>
    </div>
  );
};

export default Home;
