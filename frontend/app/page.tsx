"use client";
import axios from "axios";
import { useState } from "react";
import ReactMarkdown from "react-markdown"

export default function Home() {
  const [message, setMessage] = useState("");
  const [prompt, setPrompt] = useState("");
  async function sendMessage(){
    const message = await axios.post(`${process.env.NEXT_PUBLIC_BACKEND_URL}/chat`, {
      prompt: prompt
    })
    setMessage(message.data.response);
  }

  return (
  <div className="h-screen flex flex-col items-center justify-center w-full  p-12">
  <div className="w-full max-w-md">
    <div className="bg-white shadow-md rounded-lg p-6">
      <h2 className="text-2xl font-bold mb-4">Chatbox</h2>
      <div className="h-64 overflow-y-auto mb-4">
        <div className="mb-2">
          <p className="text-sm text-gray-600">{prompt}</p>
          <ReactMarkdown>{message}</ReactMarkdown>
        </div>
      </div>
      <input
      onKeyDown={(e) => {
        if (e.key === "Enter") {
          sendMessage();
        }
      }}
      value={prompt}
      onChange={(e: React.ChangeEvent<HTMLInputElement>) => setPrompt(e.target.value)}
        type="text"
        placeholder="Type your message..."
        className="w-full border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
      />
    </div>
  </div>
  </div>
  );
}