import { useState } from 'react';
import { ChevronDown, ChevronUp, ExternalLink } from 'lucide-react';

/**
 * Citation Card Component
 *
 * Displays a research paper with expand/collapse functionality
 */
function CitationCard({ paper, index, theme }) {
  const [expanded, setExpanded] = useState(false);
  const isDark = theme === 'dark';

  return (
    <div
      id={`citation-${index}`}
      className={`
        p-5 rounded-xl mb-4 transition-all duration-300
        ${isDark ? 'glass-dark border-cyber-accent/20' : 'glass-light border-clinical-accent/20'}
        border hover:scale-[1.02]
      `}
    >
      <div className="flex items-start gap-3">
        {/* Citation Number Badge */}
        <span className={`
          font-bold text-lg shrink-0 w-8 h-8 rounded-lg flex items-center justify-center
          ${isDark ? 'bg-cyber-accent/20 text-cyber-accent' : 'bg-clinical-accent/20 text-clinical-accent'}
        `}>
          {index}
        </span>

        <div className="flex-1 min-w-0">
          {/* Paper Title */}
          <h4 className="font-semibold text-base mb-2 leading-tight">
            {paper.title}
          </h4>

          {/* Metadata */}
          <div className="flex flex-wrap gap-3 mb-3 text-xs opacity-70">
            {paper.source && (
              <span className={`
                px-2 py-1 rounded font-mono
                ${isDark ? 'bg-cyber-accent/10' : 'bg-clinical-accent/10'}
              `}>
                {paper.source}
              </span>
            )}
            {paper.year && paper.year !== 'N/A' && (
              <span>{paper.year}</span>
            )}
            {paper.pmid && (
              <span>PMID: {paper.pmid}</span>
            )}
          </div>

          {/* Authors (if available) */}
          {paper.authors && (
            <p className="text-sm opacity-60 mb-2">{paper.authors}</p>
          )}

          {/* Abstract (expandable) */}
          {expanded && paper.abstract && (
            <p className="text-sm opacity-80 mb-3 leading-relaxed">
              {paper.abstract}
            </p>
          )}

          {/* Action Buttons */}
          <div className="flex gap-2 mt-3">
            {/* Toggle Abstract */}
            {paper.abstract && (
              <button
                onClick={() => setExpanded(!expanded)}
                className={`
                  text-xs px-3 py-1.5 rounded-lg flex items-center gap-1
                  transition-colors font-medium
                  ${isDark
                    ? 'bg-cyber-bg-secondary hover:bg-cyber-accent/20 text-cyber-accent'
                    : 'bg-white hover:bg-clinical-accent/20 text-clinical-accent'
                  }
                `}
              >
                {expanded ? (
                  <>
                    <ChevronUp className="w-3 h-3" />
                    Hide abstract
                  </>
                ) : (
                  <>
                    <ChevronDown className="w-3 h-3" />
                    Read abstract
                  </>
                )}
              </button>
            )}

            {/* View Full Paper */}
            {paper.url && (
              <a
                href={paper.url}
                target="_blank"
                rel="noopener noreferrer"
                className={`
                  text-xs px-3 py-1.5 rounded-lg flex items-center gap-1
                  transition-colors font-medium
                  ${isDark
                    ? 'bg-cyber-accent/20 hover:bg-cyber-accent/30 text-cyber-accent'
                    : 'bg-clinical-accent/20 hover:bg-clinical-accent/30 text-clinical-accent'
                  }
                `}
              >
                <ExternalLink className="w-3 h-3" />
                View paper
              </a>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default CitationCard;
