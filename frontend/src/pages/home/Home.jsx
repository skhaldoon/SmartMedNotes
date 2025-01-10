import React from "react";
import { Link } from "react-router-dom";
import home1 from "../../assets/bg.jpg";
import chart from "../../assets/chart.svg";
import paperplane from "../../assets/paperplane.svg";
import lock from "../../assets/lock.svg";
import listcheck from "../../assets/listcheck.svg";

const Home = () => {
  return (
    <>
      {/* Hero Section with Background Image */}
      <div
        className="relative h-screen flex items-center justify-start bg-cover bg-right"
        style={{ backgroundImage: `url(${home1})` }}
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

      {/* Features Section - Left and Right Layout */}
      <div className="bg-white sm:px-16 px-6 py-12">
        <div className="flex justify-between items-center w-full max-w-[1200px] mx-auto">
          {/* Left Side (Text Section) */}
          <div className="w-1/2 pr-8">
            <h2 className="text-3xl font-bold text-gray-800 mb-4">
              We do the paperwork, so <br className="sm:block hidden" /> you
              handle the business
            </h2>
            <p className="text-gray-600 max-w-[470px] mb-6">
              We are committed to delivering quality services to our clients and
              actively encourage feedback. Our company values professionalism
              and supports individual growth.
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
              title="Client Care"
              content="Your satisfaction is our utmost priority every step of the way."
            />
            <FeatureCard
              icon={paperplane}
              title="Continuous Improvement"
              content="Committed to ongoing enhancements and innovation to drive your success."
            />
            <FeatureCard
              icon={lock}
              title="Regulatory Compliance"
              content="Ensuring your medical devices meet all necessary regulations and standards."
            />
            <FeatureCard
              icon={listcheck}
              title="Audit Readiness Assistance"
              content="Preparing your organization for regulatory audits with meticulous attention to detail."
            />
          </div>
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
