/**
 * Theme configuration extracted from Stitch designs
 *
 * Two complete design systems:
 * 1. Cyber-Medical Interface (Dark) - Futuristic, Gen-Z aesthetic
 * 2. Clinical Luminance (Light) - Professional, sterile aesthetic
 */

export const themes = {
  dark: {
    name: 'cyber-medical',
    displayName: 'Cyber-Medical',
    colors: {
      // Background colors
      bgPrimary: '#0a0e1a',
      bgSecondary: '#131824',

      // Accent colors
      accent: '#00d9ff',
      accentSecondary: '#7c3aed',

      // Text colors
      textPrimary: '#ffffff',
      textSecondary: '#94a3b8',

      // Semantic colors
      verified: '#10b981',
      caution: '#f59e0b',
      danger: '#ef4444',
    },
    glassmorphism: {
      background: 'rgba(19, 24, 36, 0.7)',
      backdropBlur: '12px',
      border: '1px solid rgba(255, 255, 255, 0.1)',
      boxShadow: '0 8px 32px 0 rgba(0, 0, 0, 0.37)',
    },
    gradients: {
      hero: 'linear-gradient(135deg, #0a0e1a 0%, #1a1f35 100%)',
      card: 'linear-gradient(135deg, rgba(0, 217, 255, 0.1) 0%, rgba(124, 58, 237, 0.1) 100%)',
      button: 'linear-gradient(135deg, #00d9ff 0%, #7c3aed 100%)',
    }
  },

  light: {
    name: 'clinical-luminance',
    displayName: 'Clinical Luminance',
    colors: {
      // Background colors
      bgPrimary: '#ffffff',
      bgSecondary: '#f8fafc',

      // Accent colors
      accent: '#3b82f6',
      accentSecondary: '#06b6d4',

      // Text colors
      textPrimary: '#0f172a',
      textSecondary: '#64748b',

      // Semantic colors
      verified: '#10b981',
      caution: '#f59e0b',
      danger: '#ef4444',
    },
    glassmorphism: {
      background: 'rgba(248, 250, 252, 0.8)',
      backdropBlur: '8px',
      border: '1px solid rgba(0, 0, 0, 0.05)',
      boxShadow: '0 8px 32px 0 rgba(0, 0, 0, 0.07)',
    },
    gradients: {
      hero: 'linear-gradient(135deg, #ffffff 0%, #f8fafc 100%)',
      card: 'linear-gradient(135deg, rgba(59, 130, 246, 0.05) 0%, rgba(6, 182, 212, 0.05) 100%)',
      button: 'linear-gradient(135deg, #3b82f6 0%, #06b6d4 100%)',
    }
  }
};

/**
 * Get the current theme from localStorage or default to dark
 */
export const getInitialTheme = () => {
  const saved = localStorage.getItem('theme');
  return saved === 'light' ? 'light' : 'dark';
};

/**
 * Save theme preference to localStorage
 */
export const saveTheme = (themeName) => {
  localStorage.setItem('theme', themeName);
};

/**
 * Apply theme to document element (for Tailwind dark mode)
 */
export const applyTheme = (themeName) => {
  if (themeName === 'dark') {
    document.documentElement.classList.add('dark');
  } else {
    document.documentElement.classList.remove('dark');
  }
  saveTheme(themeName);
};

export default themes;
