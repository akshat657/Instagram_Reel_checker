import { useState } from 'react';
import { Send } from 'lucide-react';
import { chat as chatAPI } from '../api/client';

/**
 * Chat Interface Component
 *
 * Allows users to ask follow-up questions about the analyzed reel
 */
function ChatInterface({ context, citations, theme }) {
  const [message, setMessage] = useState('');
  const [chatHistory, setChatHistory] = useState([]);
  const [loading, setLoading] = useState(false);

  const isDark = theme === 'dark';

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!message.trim() || loading) return;

    const userMessage = message.trim();
    setMessage('');
    setLoading(true);

    // Add user message to history
    const newHistory = [...chatHistory, { role: 'user', content: userMessage }];
    setChatHistory(newHistory);

    try {
      // Call chat API
      const response = await chatAPI(userMessage, context, citations, newHistory);

      // Add assistant response to history
      setChatHistory([...newHistory, { role: 'assistant', content: response.response }]);
    } catch (error) {
      // Add error message
      setChatHistory([
        ...newHistory,
        { role: 'assistant', content: `Error: ${error.message}` }
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={`
      p-6 rounded-2xl
      ${isDark ? 'glass-dark border-cyber-accent/20' : 'glass-light border-clinical-accent/20'}
      border
    `}>
      <h3 className="text-xl font-bold mb-4 flex items-center gap-2">
        <span>💬</span>
        Ask Follow-up Questions
      </h3>

      {/* Chat History */}
      {chatHistory.length > 0 && (
        <div className="space-y-3 max-h-96 overflow-y-auto mb-4 pr-2">
          {chatHistory.map((msg, i) => (
            <div
              key={i}
              className={`
                p-4 rounded-xl
                ${msg.role === 'user'
                  ? `ml-8 ${isDark ? 'bg-cyber-accent/20' : 'bg-clinical-accent/20'}`
                  : `mr-8 ${isDark ? 'bg-cyber-bg-secondary/50' : 'bg-white/50'}`
                }
              `}
            >
              <div className="text-xs opacity-60 mb-1 font-mono">
                {msg.role === 'user' ? 'You' : 'MedReel AI'}
              </div>
              <div className="text-sm leading-relaxed whitespace-pre-wrap">
                {msg.content}
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Input Form */}
      <form onSubmit={handleSubmit} className="flex gap-2">
        <input
          type="text"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          placeholder="Ask about side effects, dosage, contraindications..."
          disabled={loading}
          className={`
            flex-1 p-3 rounded-xl
            ${isDark
              ? 'bg-cyber-bg-secondary text-cyber-text-primary border-cyber-accent/20'
              : 'bg-white text-clinical-text-primary border-clinical-accent/20'
            }
            border focus:outline-none focus:ring-2
            ${isDark ? 'focus:ring-cyber-accent' : 'focus:ring-clinical-accent'}
            disabled:opacity-50 disabled:cursor-not-allowed
            placeholder:opacity-50
          `}
        />
        <button
          type="submit"
          disabled={loading || !message.trim()}
          className={`
            px-6 py-3 rounded-xl font-medium flex items-center gap-2
            transition-all disabled:opacity-50 disabled:cursor-not-allowed
            ${isDark
              ? 'bg-gradient-to-r from-cyber-accent to-cyber-accent-secondary text-cyber-bg-primary'
              : 'bg-gradient-to-r from-clinical-accent to-clinical-accent-secondary text-white'
            }
            hover:shadow-lg active:scale-95
          `}
        >
          {loading ? (
            <>
              <div className="w-4 h-4 border-2 border-current border-t-transparent rounded-full animate-spin" />
              Thinking...
            </>
          ) : (
            <>
              <Send className="w-4 h-4" />
              Send
            </>
          )}
        </button>
      </form>

      {/* Example Questions */}
      {chatHistory.length === 0 && (
        <div className="mt-4 text-xs opacity-50">
          <p className="mb-2 font-mono">Example questions:</p>
          <ul className="space-y-1">
            <li>• What are the potential side effects?</li>
            <li>• Is this safe during pregnancy?</li>
            <li>• What's the recommended dosage?</li>
            <li>• Are there any drug interactions?</li>
          </ul>
        </div>
      )}
    </div>
  );
}

export default ChatInterface;
