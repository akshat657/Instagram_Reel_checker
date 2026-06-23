import { ExternalLink, Code } from 'lucide-react';

/**
 * Left Sidebar Component
 *
 * Shows developer social links
 */
function LeftSidebar({ theme }) {
  const isDark = theme === 'dark';

  return (
    <div className="fixed left-6 top-6 z-40">
      {/* LinkedIn */}
      <a
        href="https://www.linkedin.com/in/akshat-khandelwal-79647a245/"
        target="_blank"
        rel="noopener noreferrer"
        className={`
          flex items-center gap-3 px-4 py-3 rounded-xl
          ${isDark ? 'glass-dark border-cyber-accent/30 hover:border-cyber-accent' : 'glass-light border-clinical-accent/30 hover:border-clinical-accent'}
          border transition-all hover:scale-105
          ${isDark ? 'hover:shadow-lg hover:shadow-cyber-accent/20' : 'hover:shadow-lg hover:shadow-clinical-accent/20'}
        `}
        title="Connect on LinkedIn"
      >
        <ExternalLink className={`w-5 h-5 ${isDark ? 'text-cyber-accent' : 'text-clinical-accent'}`} />
        <span className="font-semibold text-sm">Akshat's LinkedIn</span>
      </a>
    </div>
  );
}

export default LeftSidebar;
