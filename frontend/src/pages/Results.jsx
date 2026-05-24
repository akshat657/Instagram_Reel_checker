import { ArrowLeft, Download, FileText } from 'lucide-react';
import CitationCard from '../components/CitationCard';
import ChatInterface from '../components/ChatInterface';

/**
 * Results Page Component
 *
 * Displays analysis results in 3-column layout:
 * - Left: Video preview & metadata
 * - Center: Analysis with inline citations
 * - Right: Research citations
 * - Bottom: Chat interface
 *
 * Based on Stitch analysis_results design
 */
function Results({ data, onReset, theme }) {
  const isDark = theme === 'dark';

  // Download transcript
  const downloadTranscript = () => {
    const content = `Instagram Reel Analysis\n\n` +
      `Caption: ${data.caption}\n\n` +
      `Original Transcript (${data.detected_language}):\n${data.transcript}\n\n` +
      `Enhanced Transcript (AI-corrected):\n${data.corrected_transcript}\n`;

    const blob = new Blob([content], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'medreel-transcript.txt';
    a.click();
    URL.revokeObjectURL(url);
  };

  // Download analysis
  const downloadAnalysis = () => {
    const content = `MedReel Analysis Report\n\n` +
      `Caption: ${data.caption}\n\n` +
      `Analysis:\n${data.analysis.replace(/<[^>]*>/g, '')}\n\n` +
      `Citations:\n` +
      data.citations.map((c, i) => `[${i + 1}] ${c.title} (${c.year}) - ${c.url}`).join('\n');

    const blob = new Blob([content], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'medreel-analysis.txt';
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="min-h-screen py-8 px-6 md:px-12">
      {/* Header */}
      <div className="max-w-7xl mx-auto mb-8">
        <button
          onClick={onReset}
          className={`
            flex items-center gap-2 px-4 py-2 rounded-xl font-medium
            transition-all hover:scale-105
            ${isDark
              ? 'bg-cyber-bg-secondary hover:bg-cyber-accent/20 text-cyber-accent'
              : 'bg-white hover:bg-clinical-accent/20 text-clinical-accent'
            }
          `}
        >
          <ArrowLeft className="w-4 h-4" />
          New Analysis
        </button>
      </div>

      {/* Main Content - 3 Column Layout */}
      <div className="max-w-7xl mx-auto grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* LEFT COLUMN: Video Preview & Metadata (25%) */}
        <div className="lg:col-span-3 space-y-6">
          {/* Caption */}
          <div className={`
            p-6 rounded-2xl
            ${isDark ? 'glass-dark border-cyber-accent/20' : 'glass-light border-clinical-accent/20'}
            border
          `}>
            <h3 className="text-lg font-bold mb-3">📝 Caption</h3>
            <p className="text-sm leading-relaxed opacity-80">
              {data.caption}
            </p>
          </div>

          {/* Language Badge */}
          <div className={`
            p-4 rounded-xl text-center
            ${isDark ? 'bg-cyber-accent/20' : 'bg-clinical-accent/20'}
          `}>
            <div className="text-xs font-mono opacity-60 mb-1">Detected Language</div>
            <div className="font-bold text-lg">
              {data.detected_language}
            </div>
          </div>

          {/* Download Buttons */}
          <div className="space-y-2">
            <button
              onClick={downloadTranscript}
              className={`
                w-full p-3 rounded-xl flex items-center justify-center gap-2
                font-medium text-sm transition-all hover:scale-105
                ${isDark
                  ? 'bg-cyber-bg-secondary hover:bg-cyber-accent/20 border-cyber-accent/20'
                  : 'bg-white hover:bg-clinical-accent/20 border-clinical-accent/20'
                }
                border
              `}
            >
              <FileText className="w-4 h-4" />
              Download Transcript
            </button>
            <button
              onClick={downloadAnalysis}
              className={`
                w-full p-3 rounded-xl flex items-center justify-center gap-2
                font-medium text-sm transition-all hover:scale-105
                ${isDark
                  ? 'bg-gradient-to-r from-cyber-accent to-cyber-accent-secondary text-cyber-bg-primary'
                  : 'bg-gradient-to-r from-clinical-accent to-clinical-accent-secondary text-white'
                }
              `}
            >
              <Download className="w-4 h-4" />
              Download Analysis
            </button>
          </div>
        </div>

        {/* CENTER COLUMN: Analysis (50%) */}
        <div className="lg:col-span-6 space-y-6">
          {/* Original Transcript */}
          <div className={`
            p-6 rounded-2xl
            ${isDark ? 'glass-dark border-cyber-accent/20' : 'glass-light border-clinical-accent/20'}
            border
          `}>
            <h3 className="text-lg font-bold mb-3">
              📜 Original Transcript ({data.detected_language})
            </h3>
            <p className="text-sm leading-relaxed opacity-80 whitespace-pre-wrap">
              {data.transcript}
            </p>
          </div>

          {/* Enhanced Transcript */}
          <div className={`
            p-6 rounded-2xl
            ${isDark ? 'glass-dark border-verified/40' : 'glass-light border-verified/40'}
            border-l-4
          `}>
            <h3 className="text-lg font-bold mb-3">
              ✨ Enhanced Transcript (AI-corrected)
            </h3>
            <p className="text-sm leading-relaxed opacity-80 whitespace-pre-wrap mb-3">
              {data.corrected_transcript}
            </p>
            <div className={`
              p-3 rounded-lg text-xs
              ${isDark ? 'bg-verified/10' : 'bg-verified/10'}
              text-verified
            `}>
              ℹ️ The enhanced version has been corrected for grammar and spelling while keeping the original {data.detected_language} language.
            </div>
          </div>

          {/* Medical Analysis */}
          <div className={`
            p-6 rounded-2xl
            ${isDark ? 'glass-dark border-cyber-accent/20' : 'glass-light border-clinical-accent/20'}
            border
          `}>
            <h3 className="text-lg font-bold mb-4">
              🔬 Medical Analysis
            </h3>
            <div
              className="prose prose-sm max-w-none"
              dangerouslySetInnerHTML={{ __html: data.analysis }}
              style={{
                color: isDark ? '#e2e2e8' : '#0f172a',
              }}
            />
          </div>
        </div>

        {/* RIGHT COLUMN: Citations (25%) */}
        <div className="lg:col-span-3">
          <div className={`
            p-6 rounded-2xl sticky top-8
            ${isDark ? 'glass-dark border-cyber-accent/20' : 'glass-light border-clinical-accent/20'}
            border
          `}>
            <h3 className="text-lg font-bold mb-4">
              📚 Scientific References ({data.citations.length})
            </h3>

            {data.citations.length > 0 ? (
              <div className="space-y-3 max-h-[600px] overflow-y-auto pr-2">
                {data.citations.map((citation, i) => (
                  <CitationCard
                    key={i}
                    paper={citation}
                    index={i + 1}
                    theme={theme}
                  />
                ))}
              </div>
            ) : (
              <div className="text-center py-8 opacity-50">
                <p className="text-sm">No scientific citations found.</p>
                <p className="text-xs mt-2">
                  Analysis is based on general medical knowledge.
                </p>
              </div>
            )}

            {data.citations.length > 0 && (
              <div className={`
                mt-4 p-3 rounded-lg text-xs
                ${isDark ? 'bg-cyber-accent/10' : 'bg-clinical-accent/10'}
              `}>
                💡 Click citation numbers [1][2] in the analysis above to jump to the source.
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Chat Interface at Bottom */}
      <div className="max-w-4xl mx-auto mt-12">
        <ChatInterface
          context={{
            caption: data.caption,
            transcript: data.transcript,
            corrected_transcript: data.corrected_transcript,
            analysis: data.analysis,
          }}
          citations={data.citations}
          theme={theme}
        />
      </div>
    </div>
  );
}

export default Results;
