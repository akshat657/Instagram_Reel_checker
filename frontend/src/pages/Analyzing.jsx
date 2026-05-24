import { useState, useEffect } from 'react';
import { analyzeReel } from '../api/client';
import ProgressTracker from '../components/ProgressTracker';

/**
 * Analyzing Page Component
 *
 * Shows 7-step progress tracker while analysis is in progress
 * Based on Stitch analyzing_reel design
 */
function Analyzing({ url, language, onComplete, onError, theme }) {
  const [currentStep, setCurrentStep] = useState(1);
  const [status, setStatus] = useState('Starting analysis...');
  const [error, setError] = useState(null);

  // 7-step pipeline
  const steps = [
    { id: 1, icon: '📥', title: 'Downloading audio', message: 'Extracting audio from Instagram Reel...' },
    { id: 2, icon: '🎤', title: 'Transcribing audio', message: 'Converting speech to text with Groq Whisper...' },
    { id: 3, icon: '✍️', title: 'Correcting grammar', message: 'Cleaning up transcript with AI...' },
    { id: 4, icon: '🔍', title: 'Extracting keywords', message: 'Identifying medical terms and claims...' },
    { id: 5, icon: '📚', title: 'Searching research papers', message: 'Querying PubMed, PMC, and Europe PMC...' },
    { id: 6, icon: '🤖', title: 'Analyzing with AI', message: 'Fact-checking claims against scientific evidence...' },
    { id: 7, icon: '✅', title: 'Complete', message: 'Analysis ready!' }
  ];

  useEffect(() => {
    let mounted = true;

    const performAnalysis = async () => {
      try {
        // Simulate progress through steps
        const stepInterval = setInterval(() => {
          if (mounted) {
            setCurrentStep(prev => {
              const next = Math.min(prev + 1, 6);
              if (next < 7) {
                setStatus(steps[next - 1].message);
              }
              return next;
            });
          }
        }, 3000); // Update every 3 seconds

        // Actual API call
        const result = await analyzeReel(url, language);

        if (mounted) {
          clearInterval(stepInterval);
          setCurrentStep(7);
          setStatus('Analysis complete!');

          // Wait a moment before transitioning
          setTimeout(() => {
            if (mounted) {
              onComplete(result);
            }
          }, 1500);
        }
      } catch (err) {
        if (mounted) {
          setError(err.message);
          setTimeout(() => {
            if (mounted) {
              onError();
            }
          }, 3000);
        }
      }
    };

    performAnalysis();

    return () => {
      mounted = false;
    };
  }, [url, language]);

  const isDark = theme === 'dark';

  if (error) {
    return (
      <div className="min-h-screen flex items-center justify-center px-6">
        <div className="max-w-md w-full p-8 rounded-2xl glass-dark border border-danger text-center">
          <span className="text-6xl mb-4 block">⚠️</span>
          <h2 className="text-2xl font-bold mb-4 text-danger">Analysis Failed</h2>
          <p className="opacity-70 mb-6">{error}</p>
          <div className="text-sm opacity-50">Redirecting to home...</div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen flex items-center justify-center px-6">
      <div className="max-w-2xl w-full">
        {/* Main content card */}
        <div className={`
          ${isDark ? 'glass-dark' : 'glass-light'}
          p-12 rounded-3xl
          border ${isDark ? 'border-cyber-accent/30' : 'border-clinical-accent/30'}
          text-center
        `}>
          {/* Circular Progress */}
          <div className="mb-8 relative inline-block">
            <svg className="w-32 h-32 transform -rotate-90">
              <circle
                cx="64"
                cy="64"
                r="56"
                stroke={isDark ? 'rgba(0, 217, 255, 0.2)' : 'rgba(59, 130, 246, 0.2)'}
                strokeWidth="8"
                fill="none"
              />
              <circle
                cx="64"
                cy="64"
                r="56"
                stroke={isDark ? '#00d9ff' : '#3b82f6'}
                strokeWidth="8"
                fill="none"
                strokeDasharray={`${(currentStep / 7) * 352} 352`}
                className="transition-all duration-500"
                strokeLinecap="round"
              />
            </svg>
            <div className="absolute inset-0 flex items-center justify-center">
              <span className="text-4xl">{steps[currentStep - 1].icon}</span>
            </div>
          </div>

          {/* Status Text */}
          <h2 className="text-2xl font-bold mb-2">
            {steps[currentStep - 1].title}
          </h2>
          <p className="opacity-70 mb-8">
            {status}
          </p>

          {/* Progress Tracker */}
          <ProgressTracker currentStep={currentStep} steps={steps} theme={theme} />

          {/* Progress Bar */}
          <div className="mt-8">
            <div className={`w-full h-2 rounded-full ${isDark ? 'bg-cyber-bg-secondary' : 'bg-clinical-bg-secondary'}`}>
              <div
                className={`h-full rounded-full transition-all duration-500 ${
                  isDark
                    ? 'bg-gradient-to-r from-cyber-accent to-cyber-accent-secondary'
                    : 'bg-gradient-to-r from-clinical-accent to-clinical-accent-secondary'
                }`}
                style={{ width: `${(currentStep / 7) * 100}%` }}
              />
            </div>
            <div className="mt-2 text-sm font-mono opacity-50">
              Step {currentStep} of 7 • {Math.round((currentStep / 7) * 100)}%
            </div>
          </div>
        </div>

        {/* Fun fact while waiting */}
        <div className="mt-6 text-center text-sm opacity-50 font-mono">
          💡 Tip: Medical misinformation spreads 6x faster than verified facts
        </div>
      </div>
    </div>
  );
}

export default Analyzing;
