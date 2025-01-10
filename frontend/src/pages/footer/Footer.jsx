import React from "react";
import { Link } from "react-router-dom";
import logo from "../../assets/lock.svg"; // Replace with your logo

const Footer = () => {
  return (
    <footer className="bg-gray-800 text-white py-12">
      <div className="max-w-7xl mx-auto px-6 sm:px-16 flex flex-col md:flex-row justify-between items-center">
        {/* Logo and Company Info */}
        <div className="flex flex-col items-center md:items-start mb-6 md:mb-0">
          <img src={logo} alt="Smart Med Notes Logo" className="w-32 mb-4" />
          <p className="text-sm text-gray-400 text-center md:text-left">
            Smart Med Notes - Revolutionizing healthcare through AI-driven
            solutions. Bringing efficiency to medical management.
          </p>
        </div>

        {/* Links Section */}
        <div className="flex flex-col md:flex-row md:space-x-12 mb-6 md:mb-0">
          <div className="flex flex-col mb-4 md:mb-0">
            <h3 className="text-lg font-semibold text-teal-400 mb-2">
              Quick Links
            </h3>
            <ul className="text-sm">
              <li>
                <Link to="/home" className="hover:text-teal-500">
                  Home
                </Link>
              </li>
              <li>
                <Link to="/about" className="hover:text-teal-500">
                  About
                </Link>
              </li>
              <li>
                <Link to="/services" className="hover:text-teal-500">
                  Services
                </Link>
              </li>
              <li>
                <Link to="/contact" className="hover:text-teal-500">
                  Contact
                </Link>
              </li>
            </ul>
          </div>

          <div className="flex flex-col mb-4 md:mb-0">
            <h3 className="text-lg font-semibold text-teal-400 mb-2">
              Contact
            </h3>
            <ul className="text-sm">
              <li>1234 Medical St., Health City</li>
              <li>Email: info@smartmednotes.com</li>
              <li>Phone: (123) 456-7890</li>
            </ul>
          </div>
        </div>

        {/* Social Links */}
        <div className="flex space-x-6 mt-6 md:mt-0">
          <a
            href="https://facebook.com"
            className="text-white hover:text-teal-500"
          >
            <i className="fab fa-facebook-f"></i>
          </a>
          <a
            href="https://twitter.com"
            className="text-white hover:text-teal-500"
          >
            <i className="fab fa-twitter"></i>
          </a>
          <a
            href="https://linkedin.com"
            className="text-white hover:text-teal-500"
          >
            <i className="fab fa-linkedin-in"></i>
          </a>
          <a
            href="https://instagram.com"
            className="text-white hover:text-teal-500"
          >
            <i className="fab fa-instagram"></i>
          </a>
        </div>
      </div>

      {/* Bottom Copyright */}
      <div className="text-center text-sm text-gray-400 mt-8">
        <p>
          &copy; {new Date().getFullYear()} Smart Med Notes. All rights
          reserved.
        </p>
      </div>
    </footer>
  );
};

export default Footer;
