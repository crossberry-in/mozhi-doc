import "./globals.css";

export const metadata = {
  title: "Mozhi (mz) Docs",
  description: "Mozhi programming language documentation — install mz, deploy packages, use the SDK and the docs API. Site: mz.netlify.app",
};

// Deliberately minimal shell — NO navigation bar, NO main-site layout.
// The docs site is standalone: a sidebar + a content pane, nothing else.
export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
