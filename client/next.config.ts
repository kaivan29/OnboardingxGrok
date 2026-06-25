import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // 'standalone' is required for the Docker/Cloud Run image (see Dockerfile),
  // but it breaks Vercel's serverless runtime (FUNCTION_INVOCATION_FAILED).
  // Vercel sets VERCEL=1 at build time, so only enable standalone elsewhere.
  ...(process.env.VERCEL ? {} : { output: "standalone" as const }),
};

export default nextConfig;
