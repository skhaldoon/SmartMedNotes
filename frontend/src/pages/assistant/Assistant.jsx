import React, { useState } from "react";
import { FiSend, FiMic, FiVolume2, FiVolumeX } from "react-icons/fi";
import axios from "axios";

function Assistant() {
  const [query, setQuery] = useState("");
  const [modelUsed, setModelUsed] = useState("");
  const [response, setResponse] = useState(""); // State to store the response
  const [isSpeaking, setIsSpeaking] = useState(false);

  // Initialize speech recognition
  const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
  recognition.lang = "en-US";
  recognition.interimResults = false;

  // Handle speech recognition
  const handleMicClick = () => {
    recognition.start();
    recognition.onresult = (event) => {
      const spokenText = event.results[0][0].transcript;
      console.log("Recognized speech:", spokenText);
      setQuery(spokenText); // Update query with recognized speech
    };

    recognition.onerror = (event) => {
      console.error("Speech recognition error", event);
    };
  };

  const speakResponse = () => {
    if (isSpeaking) {
      window.speechSynthesis.cancel();
      setIsSpeaking(false);
    } else {
      let textToSpeak = "";
  
      if (typeof response === "string") {
        textToSpeak = response; // If response is already plain text
      } else if (React.isValidElement(response)) {
        // Extract text from JSX response
        const extractText = (node) => {
          if (typeof node === "string") return node;
          if (Array.isArray(node)) return node.map(extractText).join(" ");
          if (node && typeof node === "object" && node.props) 
            return extractText(node.props.children);
          return "";
        };
        textToSpeak = extractText(response);
      }
  
      if (textToSpeak.trim()) {
        const speech = new SpeechSynthesisUtterance(textToSpeak);
        speech.lang = "en-US";
        speech.rate = 1;
        window.speechSynthesis.speak(speech);
        setIsSpeaking(true);
        speech.onend = () => setIsSpeaking(false);
      }
    }
  };
  

  const handleSend = async () => {
    if (query.trim()) {
      console.log("Query submitted:", query);
      console.log("Model used:", modelUsed);

      const baseURL = "https://4f07-34-169-121-255.ngrok-free.app"; // replace with current ngrok URL
      const endpoint = modelUsed === "Gpt2" ? "/gpt2" : "/all-MiniLM-L6-v2";

      try {
        const response = await axios.post(
          baseURL + endpoint,
          { query },
          {
            headers: {
              "Content-Type": "application/json",
            },
          }
        );

        console.log("Full Response:", response.data);

        let responseText = "";
        if (response.data && typeof response.data.response === "string") {
          responseText = response.data.response;
          setResponse(
            <div className="text-gray-700">
              <p><strong>Model Used:</strong> {modelUsed}</p>
              <p><strong>Query:</strong> {query}</p>
              <p><strong>Response:</strong> {responseText}</p>
            </div>
          );
        } else if (response.data && Array.isArray(response.data.response)) {
          responseText = response.data.response.map(item => item.content).join(" ");
          setResponse(
            <div className="text-gray-700">
              <p><strong>Model Used:</strong> {modelUsed}</p>
              <p><strong>Query:</strong> {query}</p>
              <p><strong>Response:</strong></p>
              {response.data.response.map((item, index) => (
                <div key={index}>
                  <p><strong>Content:</strong> {item.content}</p>
                  <br />
                </div>
              ))}
            </div>
          );
        } else {
          responseText = "Unexpected response format.";
          setResponse(responseText);
        }
      } catch (error) {
        console.error("Error fetching response:", error);
        setResponse("An error occurred while fetching the response.");
      }

      setQuery(""); // Clear query after sending
    }
  };

  const handleModelClick = (model) => {
    setModelUsed(model);
    console.log("Model selected:", model);
  };

  return (
    <div className="flex h-screen bg-gray-50">
      {/* Left Sidebar */}
      <div className="w-1/4 bg-gradient-to-b from-gray-500 to-gray-800 p-6 border-r text-white">
        <button
          className="w-full mb-6 bg-white text-gray-700 py-3 px-4 rounded-lg shadow hover:bg-gray-200 transition"
          onClick={() => handleModelClick("all-MiniLM-L6-v2")}
        >
          all-MiniLM-L6-v2
        </button>
        <button
          className="w-full bg-white text-gray-700 py-3 px-4 rounded-lg shadow hover:bg-gray-200 transition"
          onClick={() => handleModelClick("Gpt2")}
        >
          Gpt2
        </button>
      </div>

      {/* Main Chat Section */}
      <div className="flex-1 flex flex-col">
        {/* Chat Display Area */}
        <div className="flex-1 m-4 bg-white shadow-lg rounded-xl overflow-auto p-6">
          {response ? (
            <div className="text-gray-700">{response}</div>
          ) : (
            <div className="text-center text-gray-500 text-lg font-medium">
              Start your conversation!
            </div>
          )}
        </div>

        {/* Input Area */}
        <div className="flex items-center p-4 border-t bg-white shadow-lg">
          <input
            type="text"
            className="flex-1 mr-4 p-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-gray-500 shadow-sm"
            placeholder="Type your query..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleSend()}
          />
          <button
            className="mr-3 bg-gray-500 text-white p-3 rounded-full shadow-md hover:bg-gray-600 transition"
            onClick={handleSend}
          >
            <FiSend className="w-5 h-5" />
          </button>
          <button
            className="mr-3 bg-gray-300 text-gray-700 p-3 rounded-full shadow-md hover:bg-gray-400 transition"
            onClick={handleMicClick}
          >
            <FiMic className="w-5 h-5" />
          </button>
          <button
  className="bg-gray-300 text-gray-700 p-3 rounded-full shadow-md hover:bg-gray-400 transition"
  onClick={speakResponse}
>
  {isSpeaking ? <FiVolumeX className="w-5 h-5" /> : <FiVolume2 className="w-5 h-5" />}
</button>


        </div>
      </div>
    </div>
  );
}

export default Assistant;
