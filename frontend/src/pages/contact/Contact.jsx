import React, { useRef, useState } from "react";
// import ReCAPTCHA from "react-google-recaptcha";
// import { validateEmail } from "email-validator";
import "./contact.css";
import "@fortawesome/fontawesome-free/css/all.min.css";

// import { background1, manworking4, contact1, contact2 } from "../assets";
// import emailjs from "@emailjs/browser";
import styles from "./styles.js";

const Contact = () => {
//   const [recaptchaError, setRecaptchaError] = useState("");
  // recaptcha
//   const recaptchaRef = useRef(null);

  // email connection
  const form = useRef();
  const [emailError, setEmailError] = useState("");
  const [sendingError, setSendingError] = useState("");

  const handleSubmit = async (event) => {
    event.preventDefault();

    // // ReCAPTCHA validation
    // const recaptchaValue = recaptchaRef.current.getValue();
    // if (!recaptchaValue) {
    //   // The reCAPTCHA checkbox was not checked
    //   setRecaptchaError("Please check the reCAPTCHA checkbox.");
    //   return;
    // } else {
    //   setRecaptchaError(""); // Reset the error message if reCAPTCHA is checked
    // }

    // Email connection

//     const isValidEmail = validateEmail(form.current.user_email.value);
//     const emailValue = form.current.user_email.value.trim();
//     if (!emailValue) {
//       console.log("Please enter your email.");
//       setEmailError("Please enter your email.");
//       return;
//     }
//     if (!isValidEmail) {
//       console.log("Please enter a valid email address.");
//       setEmailError("Please enter a valid email address.");
//       return;
//     }

//     emailjs
//       .sendForm(
//         "service_q4azeth",
//         "template_s9khpoj",
//         form.current,
//         "HRkSMgOE78kfT4JcR"
//       )
//       .then(
//         (result) => {
//           console.log(result.text);
//           console.log("message sent");
//           form.current.reset();
//           setEmailError("");
//           setSendingError("");
//         },
//         (error) => {
//           console.log(error.text);
//           setSendingError("Failed to send email. Please try again later.");
//         }
//       );
//   };

//   const validateEmail = (email) => {
//     const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
//     return emailRegex.test(email);
  };

  return (
    <>
      {" "}
      <div
        className={`${styles.flexCenter} relative mt-5 pt-10  sm:py-13 py-4  `}
      >
        {/* <img
        //   src={background1}
          alt="Image"
          className={`w-auto h-auto object-cover sm:py-9 py-2 `}
        /> */}
        <div className="absolute inset-0 flex flex-col  justify-center  text-white">
          <h2
            className={`text-[40px] pl-10 font-poppins leading-[24px] pt-30 mt-20   font-bold mb-4 ml-6 text-gray-600`}
          >
            Contact Us
          </h2>
          {/* <p className="text-[18px] pl-10  ml-6 sm:block hidden">
            A leading provider of quality and regulatory affairs services
          </p> */}
        </div>
      </div>
      {/* line added */}
      <div className="mt-6 text-center pb-9">
        <h2 className="text-2xl font-poopins sm:text-4xl font-bold text-gray-600">
          Get In Touch
        </h2>
        <p className="text-base font-poopins pl-7 pr-7 ml-5 mr-5 text-[18px] sm:text-[28px]  leading-[20px] sm:leading-[40px] mt-2">
          Don’t hesitate to contact us. Please use the form below or email at{" "}
          <span className="text-gray-400">info(at)smartmednotes.com</span>
          <br /> We are looking forward for your message.
        </p>
      </div>
      {/* new contact form  */}
      <div className="container ">
        <div className="content">
          <div className="left-side">
            <div className="email details">
              <i className="fas fa-envelope"></i>
              <div className="topic">Email</div>
              <div className="text-one">info@smartmednotes.com</div>
              {/* <div className="text-two">ij</div> */}
            </div>
          </div>
          <div className="right-side ">
            <div className="topic-text">Send us a message</div>
            {/* <p>
              you can send me message from here. It's my pleasure to help you.
            </p> */}
            <form action="#">
              <div className="input-box">
                <input type="text" placeholder="Enter your name" />
              </div>
              <div className="input-box required">
                <input type="text" placeholder="Enter your email" />
              </div>
              <div className="input-box message-box">
                <textarea placeholder="Enter your message"></textarea>
              </div>
              {/* <ReCAPTCHA
                ref={recaptchaRef}
                sitekey="6LcM2fMmAAAAACNfJ4AjU6wrIOg_M4Da3-YnlB1M"
              />
              {recaptchaError && (
                <p className="text-red-600">{recaptchaError}</p>
              )} */}
              <div className="button ">
                <input type="button" value="Send Now" />
              </div>
            </form>
          </div>
        </div>
      </div>
      <div className="mt-6"></div>
    </>
  );
};

export default Contact;

const formStyles = {
  display: "flex",
  flexDirection: "column",
  maxWidth: "500px",
  margin: "0 auto",
  padding: "22px",
};

const labelStyles = {
  fontWeight: "bold",
  marginBottom: "10px",
};

const inputStyles = {
  padding: "10px",
  marginBottom: "20px",
  border: "1px solid #ccc",
  borderRadius: "4px",
};

const submitButtonStyles = {
  backgroundColor: "teal",
  color: "white",
  cursor: "pointer",
  marginTop: "8px",
};

const mediaQueryStyles = {
  "@media (max-width: 768px)": {
    maxWidth: "100%",
  },
};
