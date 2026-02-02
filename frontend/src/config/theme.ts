/**
 * Tailor Home Finder — Centralized Theme Configuration
 * 
 * This is the SINGLE source of truth for all colors, fonts, and design tokens.
 * Both the public site and admin panel pull from here.
 * 
 * To update the theme:
 *   1. Change colors here
 *   2. Update the daisyUI theme object below if needed
 *   3. Everything updates automatically
 */

// ─── Core Color Palette ─────────────────────────────────────────────────────
export const COLORS = {
  // Luxury Gold (primary brand color)
  gold: {
    400: '#D4AF37',
    500: '#C5A028',
    600: '#B8941F',
  },

  // Dark Backgrounds
  dark: {
    base: '#0c0c0c',       // Page background
    surface: '#141414',    // Cards, panels
    elevated: '#1a1a1a',   // Hover states, modals
    border: 'rgba(255, 255, 255, 0.05)',
  },

  // Text
  text: {
    primary: '#ffffff',
    secondary: '#9ca3af',
    muted: '#6b7280',
  },

  // Status
  status: {
    success: '#10b981',
    error: '#ef4444',
    warning: '#f59e0b',
    info: '#3b82f6',
    pending: '#f59e0b',
  },
} as const;

// ─── Typography ─────────────────────────────────────────────────────────────
export const FONTS = {
  sans: ['-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'Roboto', 'sans-serif'],
  serif: ['Georgia', 'Times New Roman', 'serif'],
  display: ['Playfair Display', 'Georgia', 'serif'],  // Hero titles, property names
} as const;

// ─── DaisyUI Theme Definition ───────────────────────────────────────────────
// This maps your brand colors into daisyUI's theme system.
// DaisyUI uses these to style all its components automatically.
export const DAISY_LUXURY_THEME = {
  name: 'luxury',
  // daisyUI color tokens
  '--color-primary': COLORS.gold[500],
  '--color-primary-content': '#000000',
  '--color-secondary': COLORS.gold[600],
  '--color-secondary-content': '#000000',
  '--color-accent': COLORS.gold[400],
  '--color-accent-content': '#000000',
  '--color-base-100': COLORS.dark.base,
  '--color-base-200': COLORS.dark.surface,
  '--color-base-300': COLORS.dark.elevated,
  '--color-base-content': COLORS.text.primary,
  '--color-neutral': COLORS.dark.elevated,
  '--color-neutral-content': COLORS.text.secondary,
  '--color-info': COLORS.status.info,
  '--color-success': COLORS.status.success,
  '--color-warning': COLORS.status.warning,
  '--color-error': COLORS.status.error,
} as const;

// ─── Admin Panel Theme ──────────────────────────────────────────────────────
// Slightly different surface colors for the admin panel
export const ADMIN_THEME = {
  ...DAISY_LUXURY_THEME,
  name: 'admin',
  '--color-base-100': '#0f0f0f',
  '--color-base-200': '#1a1a1a',
  '--color-base-300': '#242424',
} as const;

// ─── Easy Access Helpers ────────────────────────────────────────────────────
export const theme = {
  gold: COLORS.gold[500],
  goldLight: COLORS.gold[400],
  goldDark: COLORS.gold[600],
  background: COLORS.dark.base,
  surface: COLORS.dark.surface,
  text: COLORS.text.primary,
  textSecondary: COLORS.text.secondary,
} as const;