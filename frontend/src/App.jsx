import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { getInitialTheme, applyTheme } from './styles/themes';
import Home from './pages/Home';
import Analyzing from './pages/Analyzing';
import Results from './pages/Results';
import ThemeToggle from './components/ThemeToggle';

/**
 * Main App Component
 *
 * Manages:
 * - Theme state (dark/light)
 * - Screen state (home/analyzing/results)
 * - Analysis data flow
 */
function App() {
  // Theme management
  const [theme, setTheme] = useState(getInitialTheme);

  // Screen state: 'home', 'analyzing', 'results'
  const [screen, setScreen] = useState('home');

  // Analysis data
  const [analysisData, setAnalysisData] = useState(null);

  // Request data from Home screen
  const [requestData, setRequestData] = useState(null);

  // Apply theme on mount and changes
  useEffect(() => {
    applyTheme(theme);
  }, [theme]);

  // Handle theme toggle
  const toggleTheme = () => {
    setTheme(theme === 'dark' ? 'light' : 'dark');
  };

  // Handle analysis request from Home page
  const handleAnalyze = (url, language) => {
    setRequestData({ url, language });
    setScreen('analyzing');
  };

  // Handle analysis complete from Analyzing page
  const handleAnalysisComplete = (data) => {
    setAnalysisData(data);
    setScreen('results');
  };

  // Handle reset/new analysis
  const handleReset = () => {
    setScreen('home');
    setAnalysisData(null);
    setRequestData(null);
  };

  // Page transition variants for smooth animations
  const pageVariants = {
    initial: { opacity: 0, y: 20 },
    animate: { opacity: 1, y: 0 },
    exit: { opacity: 0, y: -20 }
  };

  return (
    <div className={`
      min-h-screen transition-theme
      ${theme === 'dark'
        ? 'bg-gradient-to-br from-cyber-bg-primary to-cyber-bg-secondary text-cyber-text-primary'
        : 'bg-gradient-to-br from-clinical-bg-primary to-clinical-bg-secondary text-clinical-text-primary'
      }
    `}>
      {/* Header: Theme Toggle + Developer Credit */}
      <div className="fixed top-6 right-6 z-50 flex items-center gap-3">
        {/* Developer Credit */}
        <a
          href="https://github.com/akshat657"
          target="_blank"
          rel="noopener noreferrer"
          className={`
            flex items-center gap-4 px-6 py-4 rounded-2xl
            ${theme === 'dark' ? 'glass-dark border-cyber-accent/30' : 'glass-light border-clinical-accent/30'}
            border transition-all hover:scale-105
            ${theme === 'dark' ? 'hover:border-cyber-accent hover:shadow-lg hover:shadow-cyber-accent/20' : 'hover:border-clinical-accent hover:shadow-lg hover:shadow-clinical-accent/20'}
          `}
          title="GitHub - Akshat Khandelwal"
        >
          <img
            src="https://github.com/akshat657.png"
            alt="Akshat Khandelwal"
            className={`w-16 h-16 rounded-full border-3 ${theme === 'dark' ? 'border-cyber-accent/50' : 'border-clinical-accent/50'} shadow-lg`}
          />
          <div className="flex flex-col">
            <span className="text-sm opacity-60 font-medium">Developed by</span>
            <span className={`font-bold text-lg ${theme === 'dark' ? 'text-cyber-accent' : 'text-clinical-accent'}`}>
              Akshat
            </span>
          </div>
        </a>

        {/* Theme Toggle */}
        <ThemeToggle theme={theme} onToggle={toggleTheme} />
      </div>

      {/* Page Content with AnimatePresence for smooth transitions */}
      <AnimatePresence mode="wait">
        {screen === 'home' && (
          <motion.div
            key="home"
            variants={pageVariants}
            initial="initial"
            animate="animate"
            exit="exit"
            transition={{ duration: 0.3 }}
          >
            <Home onAnalyze={handleAnalyze} theme={theme} />
          </motion.div>
        )}

        {screen === 'analyzing' && (
          <motion.div
            key="analyzing"
            variants={pageVariants}
            initial="initial"
            animate="animate"
            exit="exit"
            transition={{ duration: 0.3 }}
          >
            <Analyzing
              url={requestData?.url}
              language={requestData?.language}
              onComplete={handleAnalysisComplete}
              onError={handleReset}
              theme={theme}
            />
          </motion.div>
        )}

        {screen === 'results' && (
          <motion.div
            key="results"
            variants={pageVariants}
            initial="initial"
            animate="animate"
            exit="exit"
            transition={{ duration: 0.3 }}
          >
            <Results
              data={analysisData}
              onReset={handleReset}
              theme={theme}
            />
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}

export default App;
