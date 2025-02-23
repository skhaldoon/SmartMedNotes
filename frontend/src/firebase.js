// src/firebase.js
import { initializeApp } from "firebase/app";
import { getAuth, GoogleAuthProvider } from "firebase/auth";

const firebaseConfig = {
    apiKey: "AIzaSyBkkxgGHFJ5wUJtzc4Tk3PC6r5_S3vGCVs",
    authDomain: "smartmednotes-d5d1b.firebaseapp.com",
    projectId: "smartmednotes-d5d1b",
    storageBucket: "smartmednotes-d5d1b.appspot.com",
    messagingSenderId: "814561248010",
    appId: "1:814561248010:web:4a182cb13c33883093f0f3",
    measurementId: "G-C3YK7Y57JL"
  };

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const googleProvider = new GoogleAuthProvider();

export { auth, googleProvider };
