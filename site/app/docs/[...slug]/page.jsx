import { notFound } from "next/navigation";
import index from "../../../lib/content-index.json";
import { renderMarkdown } from "../../../lib/md";

// /docs/<guide>/<page>/ — renders the markdown page statically at build time.
// Content is embedded in the build-time index, so no runtime fetch can produce
// an "undefined" render: a missing page is a real 404, never a blank article.
export function generateStaticParams() {
  return index.docs.map(d => ({ slug: d.slug.split("/") }));
}

export default async function DocPage({ params }) {
  const slug = (params.slug || []).join("/");
  const doc = index.docs.find(d => d.slug === slug);
  if (!doc) notFound();

  const html = renderMarkdown(doc.content || "");
  if (!html) notFound();

  return (
    <article>
      <h1>{doc.title}</h1>
      <p className="doc-meta">
        <span className="badge">{doc.guide} guide</span>
        <span>{doc.words} words · mz.netlify.app</span>
      </p>
      <div dangerouslySetInnerHTML={{ __html: html }} />
    </article>
  );
}
