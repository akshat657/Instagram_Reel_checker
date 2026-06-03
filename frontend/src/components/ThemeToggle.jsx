import { Sun, Moon } from 'lucide-react';

/**
 * Theme Toggle Button Component
 *
 * Switches between Cyber-Medical (dark) and Clinical Luminance (light) themes
 */
function ThemeToggle({ theme, onToggle }) {
  return (
    <button
      onClick={onToggle}
      className={`
        p-3 rounded-full
        transition-all duration-300 transform hover:scale-110
        ${theme === 'dark'
          ? 'glass-dark hover:bg-cyber-accent/20'
          : 'glass-light hover:bg-clinical-accent/20'
        }
      `}
      aria-label="Toggle theme"
    >
      {theme === 'dark' ? (
        <Sun className="w-6 h-6 text-cyber-accent" />
      ) : (
        <Moon className="w-6 h-6 text-clinical-accent" />
      )}
    </button>
  );
}

export default ThemeToggle;
