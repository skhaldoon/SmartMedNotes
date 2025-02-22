import React, { useState } from "react";
import { FiSend, FiMic } from "react-icons/fi";
import axios from "axios";

function Assistant() {
  const [query, setQuery] = useState("");
  const [conversation, setConversation] = useState([]); // Stores the conversation history
  const [isListening, setIsListening] = useState(false);

  const baseURL = "https://54bb-35-199-155-245.ngrok-free.app";

  const handleSend = async () => {
    if (!query.trim()) return; // Don't send empty queries
    try {
      // Add the user's query to the conversation
      setConversation((prev) => [...prev, { type: "user", text: query }]);

      // Send the query to the backend
      const res = await axios.post(`${baseURL}/rag`, { query }, {
        headers: { "Content-Type": "application/json" },
      });

      // Add the bot's response and evaluation scores to the conversation
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
      {/* Conversation History */}
      <div className="flex-1 overflow-auto p-4 space-y-4">
        {conversation.map((msg, index) => (
          <div
            key={index}
            className={`flex ${msg.type === "user" ? "justify-end" : "justify-start"}`}
          >
            <div
              className={`p-3 rounded-lg max-w-xs ${
                msg.type === "user"
                  ? "bg-blue-200 self-end" // User message style
                  : "bg-green-200 self-start" // Bot message style
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
      </div>

      {/* Input Area */}
      <div className="flex items-center p-4 bg-white shadow-lg rounded-lg">
        <button
          className="mr-2 p-3 bg-gray-300 rounded-full"
          onClick={startListening}
        >
          <FiMic className="w-5 h-5" />
        </button>
        <input
          type="text"
          className="flex-1 p-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-gray-500"
          placeholder="Ask a question..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleSend()}
        />
        <button className="ml-3 bg-blue-500 text-white p-3 rounded-full" onClick={handleSend}>
          <FiSend className="w-5 h-5" />
        </button>
      </div>
    </div>
  );
}

export default Assistant;