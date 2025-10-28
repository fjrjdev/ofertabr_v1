/** @type {import('next').NextConfig} */
const nextConfig = {
  // Habilitar standalone output para Docker otimizado
  output: "standalone",

  // Configurações de imagem (se usar next/image)
  images: {
    remotePatterns: [
      {
        protocol: "https",
        hostname: "**",
      },
    ],
  },

  // Variáveis de ambiente públicas
  env: {
    NEXT_PUBLIC_API_URL:
      process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000",
  },
};

module.exports = nextConfig;
