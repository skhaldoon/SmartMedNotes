import React, { useState } from "react";
import { FiSend, FiMic } from "react-icons/fi";
import axios from "axios";

function Assistant() {
  const [query, setQuery] = useState("");
  const [conversation, setConversation] = useState([]); // Stores the conversation history
  const [isListening, setIsListening] = useState(false);
  const [chatStarted, setChatStarted] = useState(false); // Controls visibility of title
  const [loading, setLoading] = useState(false); // Controls loading state

  const baseURL = "https://smartmednotes.onrender.com";

  const handleSend = async () => {
    if (!query.trim() || loading) return; // Prevent sending empty query or multiple requests

    setChatStarted(true); // Hide title once chat starts
    setLoading(true); // Show loading indicator

    try {
      // Add the user's query to the conversation
      setConversation((prev) => [...prev, { type: "user", text: query }]);

      // Send the query to the backend
      const res = await axios.post(`${baseURL}/rag`, { query }, {
        headers: { "Content-Type": "application/json" },
      });

      // Add the bot's response to the conversation
      setConversation((prev) => [
        ...prev,
        {
          type: "assistant",
          text: res.data.response,
          evaluation: res.data.evaluation, // Include evaluation scores
        },
      ]);
    } catch (error) {
      console.error("Error fetching response:", error);
      // Add an error message to the conversation
      setConversation((prev) => [
        ...prev,
        { type: "assistant", text: "An error occurred while fetching the response." },
      ]);
    }
    setLoading(false); // Hide loading indicator
    setQuery(""); // Clear the input field
  };

  const startListening = () => {
    const recognition = new window.webkitSpeechRecognition();
    recognition.lang = "en-US";
    recognition.start();
    setIsListening(true);

    recognition.onresult = (event) => {
      setQuery(event.results[0][0].transcript);
      setIsListening(false);
    };

    recognition.onerror = () => setIsListening(false);
    recognition.onend = () => setIsListening(false);
  };

  return (
    <div className="flex flex-col h-screen bg-gray-100 p-4">
      {/* Centered Title (Only visible before chat starts) */}
      {!chatStarted && (
        <div className="flex justify-center items-center h-2/3">
          <h1 className="text-5xl font-bold text-black">Your Personal Assistant</h1>
        </div>
      )}

      {/* Conversation History */}
      <div className="flex-1 overflow-auto p-4 space-y-4">
        {conversation.map((msg, index) => (
          <div
            key={index}
            className={`flex ${
              msg.type === "user" ? "justify-end" : "justify-start"
            }`}
          >
            <div
              className={`p-3 rounded-lg max-w-xs ${
                msg.type === "user"
                  ? "bg-blue-500 text-white self-end" // User message (right-aligned)
                  : "bg-gray-200 text-black self-start" // Assistant message (left-aligned)
              }`}
            >
              {msg.text}
              {/* Display evaluation scores for bot responses */}
              {msg.type === "assistant" && msg.evaluation && (
                <div className="mt-2 text-sm text-gray-700">
                  <p>
                    <strong>Perplexity:</strong>{" "}
                    {msg.evaluation.perplexity !== undefined
                      ? msg.evaluation.perplexity.toFixed(2)
                      : "N/A"}
                  </p>
                  <p>
                    <strong>Semantic Similarity:</strong>{" "}
                    {msg.evaluation.semantic_similarity !== undefined
                      ? msg.evaluation.semantic_similarity.toFixed(2)
                      : "N/A"}
                  </p>
                </div>
              )}
            </div>
          </div>
        ))}
        {/* Loading Indicator */}
        {loading && (
          <div className="flex justify-start">
            <div className="p-3 bg-gray-300 text-black rounded-lg max-w-xs animate-pulse">
              Generating response...
            </div>
          </div>
        )}
      </div>

      {/* Input Area (Moved slightly higher) */}
      <div className="flex items-center p-4 bg-white shadow-lg rounded-lg mb-4">
        <button
          className="mr-2 p-3 bg-gray-300 rounded-full"
          onClick={startListening}
          disabled={loading} // Disable while loading
        >
          <FiMic className="w-5 h-5" />
        </button>
        <input
          type="text"
          className="flex-1 p-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-gray-500"
          placeholder="e.g. How to cure a fracture?"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleSend()}
          disabled={loading} // Disable while loading
        />
        <button
          className="ml-3 bg-blue-500 text-white p-3 rounded-full"
          onClick={handleSend}
          disabled={loading} // Disable while loading
        >
          <FiSend className="w-5 h-5" />
        </button>
      </div>
    </div>
  );
}

export default Assistant;
