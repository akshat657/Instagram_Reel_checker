/**
 * API client for communicating with FastAPI backend
 */
import axios from 'axios';

// API base URL - defaults to localhost for development
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

/**
 * Analyze Instagram Reel
 *
 * @param {string} url - Instagram Reel URL
 * @param {string} language - Language preference ('auto', 'English', 'Hindi')
 * @returns {Promise} Analysis response with caption, transcripts, analysis, citations
 */
export const analyzeReel = async (url, language = 'auto') => {
  try {
    const response = await axios.post(`${API_BASE_URL}/api/analyze`, {
      url,
      language
    }, {
      timeout: 180000, // 3 minutes timeout for long analysis
    });

    return response.data;
  } catch (error) {
    if (error.response) {
      // Server responded with error
      throw new Error(error.response.data.detail || 'Analysis failed');
    } else if (error.request) {
      // No response from server
      throw new Error('Cannot connect to server. Is the backend running?');
    } else {
      // Request setup error
      throw new Error(error.message);
    }
  }
};

/**
 * Chat with context from analyzed reel
 *
 * @param {string} message - User's question
 * @param {Object} context - Analysis context (caption, transcript, analysis)
 * @param {Array} citations - Research citations
 * @param {Array} history - Chat history
 * @returns {Promise} Chat response
 */
export const chat = async (message, context, citations = [], history = []) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/api/chat`, {
      message,
      context,
      citations,
      history
    }, {
      timeout: 30000, // 30 seconds for chat
    });

    return response.data;
  } catch (error) {
    if (error.response) {
      throw new Error(error.response.data.detail || 'Chat failed');
    } else if (error.request) {
      throw new Error('Cannot connect to server');
    } else {
      throw new Error(error.message);
    }
  }
};

/**
 * Health check - verify backend is running
 *
 * @returns {Promise} Health status
 */
export const healthCheck = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/api/health`, {
      timeout: 5000,
    });
    return response.data;
  } catch (error) {
    throw new Error('Backend is not responding');
  }
};

export default {
  analyzeReel,
  chat,
  healthCheck,
};
