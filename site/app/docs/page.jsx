import Link from "next/link";
import index from "../../lib/content-index.json";

export default function DocsHome() {
  const guides = index.guides || ["developers", "users"];
  return (
    <article>
      <h1>Mozhi (mz) Documentation</h1>
      <p className="doc-meta">
        <span className="badge">developers guide</span>
        <span className="badge">users guide</span>
      </p>
      <p>
        Mozhi is a full-stack programming language with a C interpreter and a Rust
        bytecode VM (<code>mozhi-fast</code>). This site is the standalone docs home:
        install the <code>mz</code> binary, deploy packages, use the NxDB SDK and read
        everything through a public API that LLMs can search without credentials.
      </p>

      <h2>Install mz in one line</h2>
      <pre className="code"><code>{`curl -fsSL https://mz.netlify.app/install.sh | sh`}</code></pre>
      <p>
        Manual install straight from this site — platform detection, SHA-256
        verification and the latest <em>allowed</em> release included. Prefer npm?
        <code>npm install -g @crossberryweb/mozhi</code> works too.
      </p>

      <h2>Browse the guides</h2>
      <div className="docs-home-cards">
        {guides.map(g => (
          <div key={g}>
            <h3 style={{ marginTop: 0 }}>{g} guide</h3>
            {index.docs.filter(d => d.guide === g).map(d => (
              <Link key={d.slug} href={`/docs/${d.slug}/`} className="card" style={{ marginBottom: 10 }}>
                <div className="ct">{d.title}</div>
                <div className="cd">{d.description}</div>
              </Link>
            ))}
          </div>
        ))}
      </div>

      <h2>For LLMs and agents</h2>
      <p>
        Every page is readable without any login. Search and read via the docs API:
      </p>
      <pre className="code"><code>{`GET https://mz.netlify.app/api/docs?q=install
GET https://mz.netlify.app/api/docs?path=developers/01-install-mz
GET https://mz.netlify.app/api/releases`}</code></pre>
    </article>
  );
}
