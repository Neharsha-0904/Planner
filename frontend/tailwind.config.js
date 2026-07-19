/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        bg: {
          app: '#0F1117',
          sidebar: '#161B27',
          card: '#1A2130',
          cardMuted: '#151A26',
        },
        border: {
          DEFAULT: '#2A3346',
        },
        text: {
          primary: '#E7EAF0',
          secondary: '#9AA3B2',
          muted: '#6B7486',
        },
        accent: {
          DEFAULT: '#7C6BF0',
          hover: '#8E7FF3',
        },
        priority: {
          p0: '#EF4E52',
          p1: '#F5A524',
          p2: '#6B7486',
        },
        status: {
          inProgress: '#7C6BF0',
          done: '#34D399',
          backlog: '#6B7486',
        },
      },
    },
  },
  plugins: [],
}
