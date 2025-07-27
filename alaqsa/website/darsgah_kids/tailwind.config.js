module.exports = {
  content: ["./pages/*.{html,js}", "./index.html", "./js/*.js"],
  theme: {
    extend: {
      colors: {
        // Primary Colors - Islamic Green
        primary: {
          DEFAULT: "#2D5A27", // Islamic tradition meets growth mindset
          50: "#F0F7EF", // green-50
          100: "#D9EDD6", // green-100
          200: "#B8DCB2", // green-200
          300: "#8FC485", // green-300
          400: "#6BAC5E", // green-400
          500: "#4A8F42", // green-500
          600: "#2D5A27", // green-600
          700: "#234521", // green-700
          800: "#1A331A", // green-800
          900: "#122214", // green-900
        },
        
        // Secondary Colors - Divine Gold
        secondary: {
          DEFAULT: "#D4AF37", // Divine knowledge and scholarly excellence
          50: "#FEFCF3", // yellow-50
          100: "#FDF6E0", // yellow-100
          200: "#FAECC2", // yellow-200
          300: "#F6DD95", // yellow-300
          400: "#F0CA66", // yellow-400
          500: "#E8B84A", // yellow-500
          600: "#D4AF37", // yellow-600
          700: "#B8942E", // yellow-700
          800: "#947626", // yellow-800
          900: "#785F20", // yellow-900
        },
        
        // Accent Colors - Warm Earth
        accent: {
          DEFAULT: "#8B4513", // Warm earth tones for approachability
          50: "#F7F2ED", // orange-50
          100: "#EDE0D1", // orange-100
          200: "#D9BFA3", // orange-200
          300: "#C19A70", // orange-300
          400: "#A67C4A", // orange-400
          500: "#8B4513", // orange-500
          600: "#7A3D11", // orange-600
          700: "#66320E", // orange-700
          800: "#52280B", // orange-800
          900: "#3D1E08", // orange-900
        },
        
        // Background Colors
        background: "#FEFEFE", // Pure canvas for content clarity - white
        surface: {
          DEFAULT: "#F7F5F3", // Subtle warmth without distraction - stone-50
          50: "#FDFCFB", // stone-50
          100: "#F7F5F3", // stone-100
          200: "#F0EDEA", // stone-200
          300: "#E8E4E0", // stone-300
          400: "#DDD8D3", // stone-400
          500: "#D1CBC5", // stone-500
        },
        
        // Text Colors
        text: {
          primary: "#1A1A1A", // Maximum readability - gray-900
          secondary: "#4A5568", // Clear hierarchy - gray-600
          muted: "#718096", // gray-500
          light: "#A0AEC0", // gray-400
        },
        
        // Status Colors
        success: {
          DEFAULT: "#22C55E", // green-500
          50: "#F0FDF4", // green-50
          100: "#DCFCE7", // green-100
          500: "#22C55E", // green-500
          600: "#16A34A", // green-600
        },
        
        warning: {
          DEFAULT: "#F59E0B", // amber-500
          50: "#FFFBEB", // amber-50
          100: "#FEF3C7", // amber-100
          500: "#F59E0B", // amber-500
          600: "#D97706", // amber-600
        },
        
        error: {
          DEFAULT: "#DC2626", // red-600
          50: "#FEF2F2", // red-50
          100: "#FEE2E2", // red-100
          500: "#EF4444", // red-500
          600: "#DC2626", // red-600
        },
        
        // Border Colors
        border: {
          DEFAULT: "#E2E8F0", // slate-200
          light: "#F1F5F9", // slate-100
          muted: "#CBD5E1", // slate-300
        },
      },
      
      fontFamily: {
        // Headlines - Scholarly elegance
        crimson: ['Crimson Text', 'serif'],
        
        // Body text - Exceptional clarity
        inter: ['Inter', 'sans-serif'],
        
        // Arabic text - Authentic typography
        amiri: ['Amiri', 'serif'],
        
        // Default sans-serif
        sans: ['Inter', 'sans-serif'],
        
        // Default serif
        serif: ['Crimson Text', 'serif'],
      },
      
      fontSize: {
        'hero': ['3.5rem', { lineHeight: '1.1', letterSpacing: '-0.02em' }],
        'display': ['2.5rem', { lineHeight: '1.2', letterSpacing: '-0.01em' }],
        'heading': ['2rem', { lineHeight: '1.3' }],
        'subheading': ['1.5rem', { lineHeight: '1.4' }],
        'body': ['1rem', { lineHeight: '1.6' }],
        'small': ['0.875rem', { lineHeight: '1.5' }],
        'caption': ['0.75rem', { lineHeight: '1.4' }],
      },
      
      boxShadow: {
        'islamic': '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
        'gentle': '0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06)',
        'elevated': '0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)',
      },
      
      animation: {
        'fade-in': 'fadeIn 300ms ease-out',
        'slide-up': 'slideUp 400ms ease-out',
        'prayer-update': 'prayerUpdate 400ms ease-out',
      },
      
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        slideUp: {
          '0%': { transform: 'translateY(20px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        },
        prayerUpdate: {
          '0%': { transform: 'scale(0.95)', opacity: '0.8' },
          '100%': { transform: 'scale(1)', opacity: '1' },
        },
      },
      
      transitionDuration: {
        'gentle': '300ms',
        'prayer': '400ms',
      },
      
      transitionTimingFunction: {
        'gentle': 'ease-out',
      },
      
      spacing: {
        '18': '4.5rem',
        '88': '22rem',
        '128': '32rem',
      },
      
      borderRadius: {
        'islamic': '0.5rem',
      },
      
      backdropBlur: {
        'gentle': '8px',
      },
    },
  },
  plugins: [],
}