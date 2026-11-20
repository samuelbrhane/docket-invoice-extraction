import type { NextConfig } from "next";

const API_URL = process.env.API_URL ?? "http://localhost:8000";

const nextConfig: NextConfig = {
  cacheComponents: true,
  // Next.js gzips responses by default, which holds back the extraction stream until it ends.
  // Vercel compresses at its edge anyway, so turning this off costs nothing there.
  compress: false,
  partialPrefetching: true,
  turbopack: {
    rules: {
      "*.css": {
        loaders: ["@tailwindcss/turbopack"],
        as: "*.css",
      },
    },
  },
  // The browser only talks to this app. Every /api request is forwarded to FastAPI,
  // so the visitor cookie and the extraction stream work on one domain with no CORS.
  async rewrites() {
    return [{ source: "/api/:path*", destination: `${API_URL}/api/:path*` }];
  },
};

export default nextConfig;