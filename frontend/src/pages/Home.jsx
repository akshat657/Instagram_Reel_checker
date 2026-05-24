import { useState } from 'react';
import { Link, Activity, Microscope } from 'lucide-react';

/**
 * Home Page Component
 *
 * Landing page with URL input form and 3-step pipeline visualization
 * Based on Stitch medreel_analyzer_home design
 */
function Home({ onAnalyze, theme }) {
  const [url, setUrl] = useState('');
  const [language, setLanguage] = useState('auto');
  const [error, setError] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    setError('');

    // Validate URL
    if (!url.trim()) {
      setError('Please enter an Instagram Reel URL');
      return;
    }

    if (!url.includes('instagram.com/reel/') && !url.includes('instagram.com/p/')) {
      setError('Please enter a valid Instagram Reel or Post URL');
      return;
    }

    onAnalyze(url, language);
  };

  const isDark = theme === 'dark';

  return (
    <div className="min-h-screen pt-24 pb-16 px-6 md:px-12">
      {/* Background decorative blobs */}
      <div className="absolute -top-20 -left-20 w-64 h-64 bg-cyber-accent/10 rounded-full blur-[100px] -z-10" />
      <div className="absolute -top-40 -right-20 w-96 h-96 bg-cyber-accent-secondary/10 rounded-full blur-[120px] -z-10" />

      <div className="max-w-6xl mx-auto">
        {/* Hero Section */}
        <section className="text-center mb-24">
          {/* Badge */}
          <div className="inline-flex items-center px-4 py-2 rounded-full mb-8 glass-dark border border-outline/30">
            <Activity className={`w-4 h-4 mr-2 ${isDark ? 'text-cyber-accent' : 'text-clinical-accent'}`} />
            <span className={`text-sm font-bold uppercase tracking-wider ${isDark ? 'text-cyber-accent' : 'text-clinical-accent'}`}>
              Vibe Check Health Trends
            </span>
          </div>

          {/* Main Heading */}
          <h1 className="text-5xl md:text-7xl lg:text-8xl font-extrabold mb-6 leading-tight">
            Stop the Cap. <br />
            <span className={`${isDark ? 'text-cyber-accent' : 'text-clinical-accent'} bg-clip-text`}>
              Fact-check the Reel.
            </span>
          </h1>

          {/* Subtitle */}
          <p className="text-lg md:text-xl max-w-3xl mx-auto mb-12 opacity-80">
            Medical misinformation spreads 6x faster than truth. Our AI dissects health claims in Reels,
            providing technical receipts for clinical accuracy.
          </p>

          {/* Input Form */}
          <form onSubmit={handleSubmit} className="max-w-4xl mx-auto">
            <div className={`
              ${isDark ? 'glass-dark' : 'glass-light'}
              p-3 rounded-2xl flex flex-col md:flex-row gap-4 items-center
              shadow-lg ${isDark ? 'shadow-cyber-accent/20' : 'shadow-clinical-accent/20'}
              border ${isDark ? 'border-cyber-accent/40' : 'border-clinical-accent/40'}
            `}>
              {/* URL Input */}
              <div className="flex-1 w-full relative">
                <Link className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 opacity-50" />
                <input
                  type="text"
                  value={url}
                  onChange={(e) => setUrl(e.target.value)}
                  placeholder="Paste Instagram Reel URL here..."
                  className={`
                    w-full py-4 pl-12 pr-4 rounded-xl
                    ${isDark
                      ? 'bg-cyber-bg-secondary text-cyber-text-primary border-cyber-accent/20'
                      : 'bg-white text-clinical-text-primary border-clinical-accent/20'
                    }
                    border focus:outline-none focus:ring-2
                    ${isDark ? 'focus:ring-cyber-accent' : 'focus:ring-clinical-accent'}
                    placeholder:opacity-50
                    font-mono text-sm
                  `}
                />
              </div>

              {/* Language Selector */}
              <select
                value={language}
                onChange={(e) => setLanguage(e.target.value)}
                className={`
                  px-6 py-4 rounded-xl font-bold text-sm uppercase tracking-wider cursor-pointer
                  ${isDark
                    ? 'bg-cyber-bg-secondary text-cyber-text-primary border-cyber-accent/20'
                    : 'bg-white text-clinical-text-primary border-clinical-accent/20'
                  }
                  border focus:outline-none focus:ring-2
                  ${isDark ? 'focus:ring-cyber-accent' : 'focus:ring-clinical-accent'}
                `}
              >
                <option value="auto">AUTO</option>
                <option value="English">ENGLISH</option>
                <option value="Hindi">HINDI</option>
              </select>

              {/* Analyze Button */}
              <button
                type="submit"
                className={`
                  px-8 py-4 rounded-xl font-bold uppercase tracking-wider
                  flex items-center gap-2 transition-all active:scale-95
                  ${isDark
                    ? 'bg-gradient-to-r from-cyber-accent to-cyber-accent-secondary text-cyber-bg-primary'
                    : 'bg-gradient-to-r from-clinical-accent to-clinical-accent-secondary text-white'
                  }
                  shadow-lg hover:shadow-xl
                  ${isDark ? 'hover:shadow-cyber-accent/50' : 'hover:shadow-clinical-accent/50'}
                `}
              >
                <Microscope className="w-5 h-5" />
                ANALYZE
              </button>
            </div>

            {/* Error Message */}
            {error && (
              <div className="mt-4 p-4 rounded-lg bg-danger/20 border border-danger text-danger text-sm">
                {error}
              </div>
            )}

            {/* Status Indicators */}
            <div className="mt-6 flex justify-center gap-8 text-xs font-mono">
              <div className="flex items-center gap-2 opacity-70">
                <span className={`w-2 h-2 rounded-full ${isDark ? 'bg-cyber-accent shadow-[0_0_8px_#00d9ff]' : 'bg-clinical-accent shadow-[0_0_8px_#3b82f6]'}`} />
                SYSTEMS ONLINE
              </div>
              <div className="flex items-center gap-2 opacity-70">
                <span className="w-2 h-2 rounded-full bg-cyber-accent-secondary shadow-[0_0_8px_#7c3aed]" />
                4,291 REELS SCANNED TODAY
              </div>
            </div>
          </form>
        </section>

        {/* 3-Step Pipeline */}
        <section>
          <div className="mb-12">
            <h2 className="text-3xl font-bold mb-2">Technical Pipeline</h2>
            <p className="opacity-70">How we catch the cap in 45 seconds.</p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {/* Step 1: Download & Transcribe */}
            <div className={`
              p-8 rounded-2xl ${isDark ? 'glass-dark' : 'glass-light'}
              border ${isDark ? 'border-cyber-accent/30' : 'border-clinical-accent/30'}
              hover:scale-105 transition-transform duration-300
            `}>
              <div className={`
                w-16 h-16 rounded-xl mb-6 flex items-center justify-center
                ${isDark ? 'bg-cyber-accent/20' : 'bg-clinical-accent/20'}
              `}>
                <span className="text-3xl">🎵</span>
              </div>
              <h3 className="text-xl font-bold mb-3">Download & Transcribe</h3>
              <p className="opacity-70 text-sm">
                Extract audio from the Reel and transcribe speech using Groq Whisper with automatic language detection.
              </p>
              <div className="mt-4 text-xs font-mono opacity-50">
                Step 1 • ~5s
              </div>
            </div>

            {/* Step 2: Fetch Research */}
            <div className={`
              p-8 rounded-2xl ${isDark ? 'glass-dark' : 'glass-light'}
              border ${isDark ? 'border-cyber-accent-secondary/30' : 'border-clinical-accent-secondary/30'}
              hover:scale-105 transition-transform duration-300
            `}>
              <div className={`
                w-16 h-16 rounded-xl mb-6 flex items-center justify-center
                ${isDark ? 'bg-cyber-accent-secondary/20' : 'bg-clinical-accent-secondary/20'}
              `}>
                <span className="text-3xl">📚</span>
              </div>
              <h3 className="text-xl font-bold mb-3">Fetch Research Papers</h3>
              <p className="opacity-70 text-sm">
                Query PubMed, PMC, and Europe PMC in parallel to find peer-reviewed scientific evidence.
              </p>
              <div className="mt-4 text-xs font-mono opacity-50">
                Step 2 • ~10s
              </div>
            </div>

            {/* Step 3: AI Analysis */}
            <div className={`
              p-8 rounded-2xl ${isDark ? 'glass-dark' : 'glass-light'}
              border ${isDark ? 'border-cyber-accent/30' : 'border-clinical-accent/30'}
              hover:scale-105 transition-transform duration-300
            `}>
              <div className={`
                w-16 h-16 rounded-xl mb-6 flex items-center justify-center
                ${isDark ? 'bg-cyber-accent/20' : 'bg-clinical-accent/20'}
              `}>
                <span className="text-3xl">🔬</span>
              </div>
              <h3 className="text-xl font-bold mb-3">AI Fact-Check Analysis</h3>
              <p className="opacity-70 text-sm">
                Groq LLM analyzes claims against scientific evidence and generates report with inline citations.
              </p>
              <div className="mt-4 text-xs font-mono opacity-50">
                Step 3 • ~30s
              </div>
            </div>
          </div>
        </section>
      </div>
    </div>
  );
}

export default Home;
