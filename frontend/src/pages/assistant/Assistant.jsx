import React, { useState, useEffect } from "react";
import { FiSend } from "react-icons/fi";

function Assistant() {
  const [messages, setMessages] = useState([
    { id: 1, text: "Hello! How can I assist you today?", sender: "bot" },
  ]);
  const [input, setInput] = useState("");
  const [isTyping, setIsTyping] = useState(false);
  const [placeholderText, setPlaceholderText] = useState("");
  const [currentCharIndex, setCurrentCharIndex] = useState(0);
  const [lineIndex, setLineIndex] = useState(0);

  const placeholderLines = [
    "Ask me anything!",
    "Need help with your health?",
    "What can I do for you today?",
    "Type your query here...",
  ];

  useEffect(() => {
    // Dynamic letter-by-letter typing for the placeholder
    if (lineIndex < placeholderLines.length) {
      let charIndex = 0;
      const typeInterval = setInterval(() => {
        setPlaceholderText(
          (prevText) => prevText + placeholderLines[lineIndex][charIndex]
        );
        charIndex++;

        if (charIndex === placeholderLines[lineIndex].length) {
          clearInterval(typeInterval);
          setTimeout(() => {
            setLineIndex((prevIndex) =>
              prevIndex + 1 < placeholderLines.length ? prevIndex + 1 : 0
            );
            setPlaceholderText("");
          }, 1500); // Pause before switching to the next line
        }
      }, 100); // Typing speed

      return () => clearInterval(typeInterval);
    }
  }, [lineIndex]);

  const handleSend = () => {
    if (input.trim()) {
      setMessages([
        ...messages,
        { id: Date.now(), text: input, sender: "user" },
      ]);
      setInput("");

      // Simulate bot typing and responding
      setIsTyping(true);
      setTimeout(() => {
        setMessages((prevMessages) => [
          ...prevMessages,
          {
            id: Date.now(),
            text: "I understand your request. Let me process that!",
            sender: "bot",
          },
        ]);
        setIsTyping(false);
      }, 1000);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter") {
      handleSend();
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-blue-100 flex flex-col items-center py-8 px-4">
      {/* Header */}
      <header className="w-full max-w-3xl bg-white shadow-lg py-4 px-6 flex items-center justify-between rounded-lg">
        <h1 className="text-2xl font-bold text-gray-800">Doctor's Assistant</h1>
        <button
          onClick={() => alert("Logout initiated")}
          className="bg-red-500 text-white px-4 py-2 rounded-lg hover:bg-red-600 transition-all"
        >
          Logout
        </button>
      </header>

      {/* Chat Area */}
      <main className="w-full max-w-3xl flex-grow bg-white p-6 rounded-lg shadow-lg mt-6 overflow-y-auto space-y-4">
        {messages.map((msg) => (
          <div
            key={msg.id}
            className={`flex items-start space-x-4 ${
              msg.sender === "user" ? "justify-end" : ""
            }`}
          >
            {msg.sender === "bot" && (
              <img
                src="https://via.placeholder.com/40"
                alt="Bot Avatar"
                className="w-10 h-10 rounded-full"
              />
            )}
            <div
              className={`p-3 rounded-lg max-w-xs text-sm shadow ${
                msg.sender === "user"
                  ? "bg-blue-600 text-white"
                  : "bg-gray-200 text-gray-800"
              }`}
            >
              {msg.text}
            </div>
            {msg.sender === "user" && (
              <img
                src="https://via.placeholder.com/40"
                alt="User Avatar"
                className="w-10 h-10 rounded-full"
              />
            )}
          </div>
        ))}
        {isTyping && (
          <div className="flex items-center space-x-2">
            <img
              src="https://via.placeholder.com/40"
              alt="Bot Avatar"
              className="w-10 h-10 rounded-full"
            />
            <div className="p-3 rounded-lg bg-gray-200 text-gray-800 text-sm shadow">
              Bot is typing...
            </div>
          </div>
        )}
      </main>

      {/* Input Area */}
      <footer className="w-full max-w-3xl flex items-center justify-between mt-6 bg-white rounded-lg shadow-lg">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder={placeholderText}
          className="flex-1 bg-gray-100 text-gray-800 p-4 rounded-l-lg focus:outline-none focus:ring-2 focus:ring-blue-300"
        />
        <button
          onClick={handleSend}
          className="bg-blue-600 text-white p-4 rounded-r-lg hover:bg-blue-700 transition-all"
        >
          <FiSend className="w-5 h-5" />
        </button>
      </footer>
    </div>
  );
}

export default Assistant;
