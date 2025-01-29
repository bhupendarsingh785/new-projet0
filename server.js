// backend/server.js
require('dotenv').config(); // Environment variables ke liye
const express = require('express'); // Express framework
const axios = require('axios'); // API calls ke liye
const cors = require('cors'); // Frontend-Backend communication ke liye

const app = express(); // Express app banayein
const PORT = 5000; // Server ka port

// Middleware
app.use(cors()); // Allow frontend requests
app.use(express.json()); // JSON data handle karein

// Environment Variables 
const OPENAI_API_KEY = process.env.OPENAI_API_KEY; // OpenAI API key
const DEEPSEEK_API_KEY = process.env.DEEPSEEK_API_KEY; // DeepSeek API key

// ChatGPT API Call
app.post('/generate-code', async (req, res) => {
    const { userInput } = req.body; // Frontend se user input lein

    try {
        // Call ChatGPT API
        const chatGPTResponse = await axios.post(
            'https://api.openai.com/v1/completions', // OpenAI API endpoint
            {
                model: "text-davinci-003", // Model name
                prompt: Generate code for: ${userInput}, // User input
                max_tokens: 1000, // Maximum tokens
            },
            {
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': Bearer ${OPENAI_API_KEY}, // API key
                },
            }
        );

        const chatGPTCode = chatGPTResponse.data.choices[0].text; // Generated code

        // Call DeepSeek API (replace with correct endpoint)
        const deepseekResponse = await axios.post(
            'https://api.deepseek.com/v3/generate', // DeepSeek API endpoint
            {
                input: userInput, // User input
                model: "deepseek-v3", // Model name
                max_tokens: 1000, // Maximum tokens
            },
            {
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': Bearer ${DEEPSEEK_API_KEY}, // API key
                },
            }
        );

        const deepseekCode = deepseekResponse.data.output; // Generated code

        // Combine codes
        const generatedCode = ${chatGPTCode}\n\n${deepseekCode};

        // Send response to frontend
        res.json({ code: generatedCode });
    } catch (error) {
        console.error("Error generating code:", error);
        res.status(500).json({ error: "An error occurred while generating code." });
    }
});

// Start server
app.listen(PORT, () => {
    console.log(Server running on http://localhost:${PORT});
});