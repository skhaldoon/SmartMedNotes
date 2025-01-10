import React from "react";
import home1 from "../../assets/home1.jpg";
const About = () => {
  return (
    <div className="w-full min-h-screen bg-gradient-to-r from-blue-50 via-teal-50 to-blue-100 flex items-center justify-center px-6 md:px-12 lg:px-24">
      {/* Container */}
      <div className="flex flex-col lg:flex-row items-center lg:items-start lg:space-x-12 space-y-6 lg:space-y-0 w-full">
        {/* Left Section */}
        <div className="flex-1 text-left space-y-6">
          <h1 className="text-4xl md:text-5xl font-bold text-blue-800">
            Empowering Orthopedic Professionals
          </h1>
          <p className="text-lg md:text-xl text-gray-700 leading-relaxed">
            Your ultimate AI-driven healthcare solution! Organize medical notes,
            diagnose conditions, and receive expert assistance with ease.
            Experience the future of healthcare today.
          </p>
          <button className="bg-green-600 text-white px-6 py-3 rounded-lg shadow-lg hover:bg-green-700 transition-all duration-300">
            Get Started
          </button>
        </div>

        {/* Right Section */}
        <div className="flex-1 flex justify-center">
          <div className="relative w-full max-w-lg">
            {/* Decorative Background for the Image */}
            <div className="absolute inset-0 bg-gradient-to-br from-blue-300 via-blue-200 to-blue-100 rounded-full blur-2xl opacity-10 -z-10"></div>
            <img
              src={home1}
              alt="Medical Illustration"
              className="w-full rounded-lg shadow-2xl"
            />
          </div>
        </div>
      </div>
    </div>
  );
};
export default About;
