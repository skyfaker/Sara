import { defineConfig, Plugin } from 'vite'
import path from 'path'
import tailwindcss from '@tailwindcss/vite'
import react from '@vitejs/plugin-react'

function figmaAssetStub(): Plugin {
  // 1x1 transparent PNG used as placeholder for missing Figma exports
  const PLACEHOLDER =
    'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=='
  return {
    name: 'figma-asset-stub',
    enforce: 'pre',
    resolveId(id) {
      if (id.startsWith('figma:asset/')) {
        return `\0figma-stub:${id}`
      }
    },
    load(id) {
      if (id.startsWith('\0figma-stub:')) {
        return `export default "${PLACEHOLDER}"`
      }
    },
  }
}

export default defineConfig({
  plugins: [
    figmaAssetStub(),
    // The React and Tailwind plugins are both required for Make, even if
    // Tailwind is not being actively used – do not remove them
    react(),
    tailwindcss(),
  ],
  resolve: {
    alias: {
      // Alias @ to the src directory
      '@': path.resolve(__dirname, './src'),
    },
  },

  server: {
    proxy: {
      '/api': 'http://localhost:5001',
    },
  },

  // File types to support raw imports. Never add .css, .tsx, or .ts files to this.
  assetsInclude: ['**/*.svg', '**/*.csv'],
})
