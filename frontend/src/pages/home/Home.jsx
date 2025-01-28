import React from "react";
import { Link } from "react-router-dom";
import home1 from "../../assets/home1.jpg";
import bg from "../../assets/bg.jpg";
import chart from "../../assets/chart.svg";
import paperplane from "../../assets/paperplane.svg";
import lock from "../../assets/lock.svg";
import listcheck from "../../assets/listcheck.svg";

const Home = () => {
  return (
    <>
      {/* trying new thign */}
      <div className="relative bg-gradient-to-b from-gray-400 via-gray-400 to-gray-600 text-gray-400">
        <div className="container mx-auto px-6 py-16 text-center lg:text-left">
          <div className="flex flex-col lg:flex-row items-center">
            <div className="w-full ml-4 lg:w-1/2">
              <h1 className="text-4xl font-extrabold sm:text-5xl lg:text-6xl from-gray-400 to-gray-500 leading-tight">
                Simplifying Orthopedic <br />
                <span className="text-transparent bg-clip-text bg-gradient-to-r from-gray-500 to-gray-600">
                  Care with SmartMedNotes
                </span>
              </h1>
              <p className="mt-4 text-lg sm:text-xl text-gray-300">
                Intelligent assistant, designed to optimize workflows, save
                time, and enhance patient care
              </p>
              <div className="mt-6">
                {/* 
              <button className="py-4 px-6 font-medium text-[18px] text-white bg-gray-400 hover:bg-gray-500 rounded-[10px]">
                Get In Touch
              </button>
             */}
                <Link to="/Assistant">
                  <button className="bg-gray-500 hover:bg-gray-700 text-white px-6 py-3 rounded-lg font-medium text-lg shadow-lg">
                    Get Started
                  </button>
                </Link>
              </div>
            </div>
            <div className="w-full lg:w-1/2 mt-10 mb-12 lg:mt-0 flex justify-center">
              <div className="relative">
                <div className="absolute inset-0 bg-gradient-to-r from-gray-500 via-gray-600 to-gray-800 blur-lg rounded-full h-96 w-96"></div>
              </div>
            </div>
          </div>
        </div>
        <div className="absolute inset-0 pointer-events-none">
          <div className="absolute top-20 left-10 w-10 h-10 bg-gray-600 rounded-full opacity-50 animate-pulse"></div>
          <div className="absolute bottom-10 right-20 w-16 h-16 bg-gray-400 rounded-full opacity-50 animate-pulse"></div>
        </div>
      </div>
      {/* Features Section - Left and Right Layout */}
      <div className="bg-white mt-10 sm:px-16 px-6 py-12">
        <div className="flex justify-between items-center w-full max-w-[1200px] mx-auto">
          {/* Left Side (Text Section) */}
          <div className="w-1/2 pr-8">
            <h2 className="text-3xl font-bold text-gray-800 mb-4">
              Tailored specifically for <br className="sm:block hidden" />{" "}
              Orthopedic Practices
            </h2>
            <p className="text-gray-600 max-w-[470px] mb-6">
              "Unlike generic tools, SmartMedNotes is designed specifically for
              the complexities of orthopedic care."
            </p>
            <Link to="/Contact">
              <button className="py-4 px-6 font-medium text-[18px] text-white bg-gray-400 hover:bg-gray-500 rounded-[10px]">
                Get In Touch
              </button>
            </Link>
          </div>

          {/* Right Side (Feature Cards) */}
          <div className="w-1/2 flex flex-col space-y-6">
            <FeatureCard
              icon={chart}
              title="Effortless Documentation"
              content="Automatically generate precise, structured notes tailored to orthopedic needs"
            />
            <FeatureCard
              icon={paperplane}
              title="Continuous Improvement"
              content="Rest easy knowing your patient data is encrypted and stored in compliance with the latest healthcare regulations"
            />
            <FeatureCard
              icon={lock}
              title="Secure Data Management"
              content="Ensuring your medical notes meet all necessary regulations and standards."
            />
            <FeatureCard
              icon={listcheck}
              title="AI-Powered Insights"
              content="Leverage artificial intelligence to identify trends, streamline diagnoses, and improve treatment outcomes"
            />
          </div>
        </div>
      </div>
      {/* trying about on top */}
      <div className="w-full  min-h-screen bg-gradient-to-r from-gray-400 via-gray-400 to-gray-600 flex items-center justify-center px-6 md:px-12 lg:px-24">
        {/* Container */}
        <div className="flex flex-col lg:flex-row items-center lg:items-start lg:space-x-12 space-y-6 lg:space-y-0 w-full">
          {/* Left Section */}
          <div className="flex-1 text-left space-y-6">
            <h1 className="text-4xl md:text-5xl font-bold text-gray-700">
              Empowering Orthopedic Professionals
            </h1>
            <p className="text-lg md:text-xl text-gray-700 leading-relaxed">
              Your ultimate AI-driven healthcare solution! Organize medical
              notes, diagnose conditions, and receive expert assistance with
              ease. Experience the future of healthcare today.
            </p>
            <Link to="/Assistant">
              <button className="bg-gray-600 text-white px-6 py-3 rounded-lg shadow-lg hover:bg-gray-500 transition-all duration-300">
                Get Started
              </button>
            </Link>
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
      {/* //new */}

      {/* Hero Section with Background Image */}
      <div
        className="relative h-screen flex items-center justify-start bg-cover bg-right"
        style={{ backgroundImage: `url(${bg})` }}
      >
        {/* Overlay to dampen image */}
        <div className="absolute inset-0 bg-black bg-opacity-50"></div>

        {/* Text Section */}
        <div className="relative z-10 text-white px-10 max-w-lg">
          <h1 className="text-4xl font-bold mb-4">
            Welcome to Smart Med Notes
          </h1>
          <p className="text-lg">
            Revolutionizing healthcare through AI-driven solutions.
          </p>
        </div>
      </div>

     
    </>
  );
};

const FeatureCard = ({ icon, title, content }) => (
  <div className="flex flex-row p-6 rounded-[20px] bg-gray-100 hover:bg-gray-200">
    <div className="w-[64px] h-[64px] rounded-full flex justify-center items-center bg-gray-300">
      <img src={icon} alt={title} className="w-[50%] h-[50%] object-contain" />
    </div>
    <div className="flex-1 flex flex-col ml-3">
      <h4 className="font-semibold text-black text-[18px] leading-[23.4px] mb-1">
        {title}
      </h4>
      <p className="font-normal text-black text-[16px] leading-[24px]">
        {content}
      </p>
    </div>
  </div>
);

export default Home;
