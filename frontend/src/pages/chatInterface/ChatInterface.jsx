import React, { useState } from "react";
import { FiSend } from "react-icons/fi";

function ChatInterface() {
  const [messages, setMessages] = useState([
    { id: 1, text: "Hello! How can I help you today?", sender: "bot" },
    { id: 2, text: "I need help with my account.", sender: "user" },
  ]);
  const [input, setInput] = useState("");

  const handleSend = () => {
    if (input.trim()) {
      setMessages([
        ...messages,
        { id: Date.now(), text: input, sender: "user" },
      ]);
      setInput("");

      // Simulate bot response
      setTimeout(() => {
        setMessages((prevMessages) => [
          ...prevMessages,
          {
            id: Date.now(),
            text: "Sure, I'd be happy to help!",
            sender: "bot",
          },
        ]);
      }, 1000);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col items-center py-8 px-4">
      <header className="w-full max-w-3xl bg-white shadow-md py-4 px-6 flex items-center justify-between">
        <h1 className="text-2xl font-bold text-gray-800">Doctor's Assistant</h1>
        <button className="bg-gray-300 text-gray-600 px-4 py-2 rounded hover:bg-gray-400">
          Logout
        </button>
      </header>

      <main className="w-full max-w-3xl flex-grow bg-gray-50 p-6 rounded-lg shadow-md mt-6 overflow-y-auto">
        <div className="space-y-4">
          {messages.map((msg) => (
            <div
              key={msg.id}
              className={`flex items-start space-x-4 ${
                msg.sender === "user" ? "justify-end" : ""
              }`}
            >
              <div
                className={`p-2 rounded-lg max-w-xs text-sm ${
                  msg.sender === "user" ? "bg-gray-200" : "bg-blue-100"
                }`}
              >
                <p>{msg.text}</p>
              </div>
            </div>
          ))}
        </div>
      </main>

      <footer className="w-full max-w-3xl flex items-center justify-between mt-6">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type your message..."
          className="flex-1 bg-gray-200 text-gray-800 p-3 rounded-l-lg focus:outline-none focus:ring-2 focus:ring-blue-300"
        />
        <button
          onClick={handleSend}
          className="bg-blue-600 text-white p-3 rounded-r-lg hover:bg-blue-700"
        >
          <FiSend className="w-5 h-5" />
        </button>
      </footer>
    </div>
  );
}

export default ChatInterface;
