import React, { useState } from "react";
import { FiSend, FiMic } from "react-icons/fi";

function Assistant() {
  const [query, setQuery] = useState("");

  const handleSend = () => {
    if (query.trim()) {
      console.log("Query submitted:", query);
      setQuery("");
    }
  };

  return (
    <div className="flex h-screen bg-gray-50">
      {/* Left Sidebar */}
      <div className="w-1/4 bg-gradient-to-b from-gray-500 to-gray-800 p-6 border-r text-white">
        <button className="w-full mb-6 bg-white text-gray-700 py-3 px-4 rounded-lg shadow hover:bg-gray-200 transition">
          Option 1
        </button>
        <button className="w-full bg-white text-gray-700 py-3 px-4 rounded-lg shadow hover:bg-gray-200 transition">
          Option 2
        </button>
      </div>

      {/* Main Chat Section */}
      <div className="flex-1 flex flex-col">
        {/* Chat Display Area */}
        <div className="flex-1 m-4 bg-white shadow-lg rounded-xl overflow-auto">
          <div className="p-6 text-center text-gray-500 text-lg font-medium">
            Start your conversation!
          </div>
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
          <button className="bg-gray-300 text-gray-700 p-3 rounded-full shadow-md hover:bg-gray-400 transition">
            <FiMic className="w-5 h-5" />
          </button>
        </div>
      </div>
    </div>
  );
}

export default Assistant;
