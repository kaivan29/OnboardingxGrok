import type { ReactNode } from "react";

export const metadata = {
  title: "Onboarding Wiki API",
  description: "API backend for onboarding codebase summaries",
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
