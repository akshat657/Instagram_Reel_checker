/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class', // Enable class-based dark mode for theme toggle
  theme: {
    extend: {
      colors: {
        // Cyber-Medical Interface (Dark Theme) - from Stitch designs
        'cyber-bg-primary': '#0a0e1a',
        'cyber-bg-secondary': '#131824',
        'cyber-accent': '#00d9ff',
        'cyber-accent-secondary': '#7c3aed',
        'cyber-text-primary': '#ffffff',
        'cyber-text-secondary': '#94a3b8',

        // Clinical Luminance (Light Theme) - from Stitch designs
        'clinical-bg-primary': '#ffffff',
        'clinical-bg-secondary': '#f8fafc',
        'clinical-accent': '#3b82f6',
        'clinical-accent-secondary': '#06b6d4',
        'clinical-text-primary': '#0f172a',
        'clinical-text-secondary': '#64748b',

        // Semantic colors (medical context)
        'verified': '#10b981',
        'caution': '#f59e0b',
        'danger': '#ef4444',
      },
      fontFamily: {
        sans: ['Sora', 'Inter', 'system-ui', 'sans-serif'],
        mono: ['JetBrains Mono', 'monospace'],
      },
      backdropBlur: {
        xs: '2px',
        sm: '4px',
        md: '8px',
        lg: '12px',
        xl: '16px',
      },
    },
  },
  plugins: [],
}
