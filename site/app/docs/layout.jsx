import Sidebar from "../../components/Sidebar";
import index from "../../lib/content-index.json";

// Standalone docs layout: sidebar + content. No nav bar anywhere.
// NOTE: only metadata goes to the client component — the full markdown
// content must stay server-side (keeps every page payload small).
export default function DocsLayout({ children }) {
  const guides = index.guides || ["developers", "users"];
  const navDocs = index.docs.map(({ content, ...meta }) => meta);
  return (
    <div className="docs-shell">
      <Sidebar docs={navDocs} guides={guides} />
      <main className="content">{children}</main>
    </div>
  );
}
