import { Link } from "react-router-dom"
import Nav from "../components/Nav"
import SparklesBg from "../components/SparklesBg"

const STATS = [
  { value: "140K+", label: "Leads per profession" },
  { value: "50+",   label: "Countries covered" },
  { value: "15+",   label: "Data points per lead" },
  { value: "100%",  label: "Auto-enriched" },
]

const FEATURES = [
  { icon: "◈", title: "Global Coverage",  desc: "India, UAE, UK, USA, Europe — every city split into granular areas.", color: "var(--accent-cyan)" },
  { icon: "◉", title: "Auto Enrichment",  desc: "Owner names, emails, WhatsApp, LinkedIn from 5+ sources automatically.", color: "var(--accent-violet)" },
  { icon: "◈", title: "Dev Intelligence", desc: "Detects chatbot and mobile-friendliness. Flags every business to pitch.", color: "var(--accent-gold)" },
  { icon: "◉", title: "Zero Duplicates",  desc: "Persistent memory across all runs. Same business never collected twice.", color: "var(--accent-green)" },
  { icon: "◈", title: "Any Niche",        desc: "Dentist, gym, lawyer — one word change. Works for any profession.", color: "var(--accent-cyan)" },
  { icon: "◉", title: "Live Dashboard",   desc: "Watch leads appear in real time with progress tracking and CSV download.", color: "var(--accent-violet)" },
]

export default function HomePage() {
  return (
    <div className="page">
      <SparklesBg />
      <Nav />

      <section style={{ minHeight: "100vh", display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", textAlign: "center", padding: "120px 24px 80px" }}>
        <div className="stagger" style={{ maxWidth: 800 }}>
          <div className="stat-pill" style={{ marginBottom: 32, display: "inline-flex" }}>
            <span className="dot" /> Live intelligence engine
          </div>
          <h1 style={{fontSize: "clamp(36px, 5vw, 68px)", fontWeight: 800, lineHeight: 1.0, letterSpacing: "-0.04em", marginBottom: 24 }}>
            Find every lead.<br />
            <span style={{ color: "var(--accent-cyan)" }}>
              Own every market.
            </span>
          </h1>
          <p style={{ fontSize: 18, color: "var(--text-secondary)", lineHeight: 1.7, maxWidth: 560, margin: "0 auto 40px" }}>
            The most advanced Google Maps lead scraper ever built. Auto-enriched with owner details, social media, and dev opportunity scoring.
          </p>
          <div style={{ display: "flex", gap: 12, justifyContent: "center" }}>
            <Link to="/login" className="btn btn-primary" style={{ padding: "14px 32px", fontSize: 14 }}>Start scraping →</Link>
            <a href="#features" className="btn btn-ghost" style={{ padding: "14px 32px", fontSize: 14 }}>See features</a>
          </div>
        </div>

        <div style={{ display: "grid", gridTemplateColumns: "repeat(4,1fr)", marginTop: 80, maxWidth: 700, width: "100%", border: "1px solid var(--border)", borderRadius: "var(--radius-lg)", overflow: "hidden" }}>
          {STATS.map((s, i) => (
            <div key={i} style={{ background: "var(--bg-card)", padding: "20px 16px", textAlign: "center", borderRight: i < 3 ? "1px solid var(--border)" : "none" }}>
              <div style={{ fontSize: "clamp(22px,3vw,30px)", fontWeight: 800, color: i % 2 === 0 ? "var(--accent-cyan)" : "var(--accent-violet)", letterSpacing: "-0.02em", marginBottom: 4 }}>{s.value}</div>
              <div style={{ fontSize: 11, color: "var(--text-muted)", textTransform: "uppercase", letterSpacing: "0.08em" }}>{s.label}</div>
            </div>
          ))}
        </div>
      </section>

      <section id="features" style={{ padding: "80px 24px", maxWidth: 1100, margin: "0 auto" }}>
        <div style={{ textAlign: "center", marginBottom: 60 }}>
          <p style={{ fontSize: 11, letterSpacing: "0.15em", textTransform: "uppercase", color: "var(--text-muted)", marginBottom: 16 }}>Capabilities</p>
          <h2 style={{ fontSize: "clamp(32px,5vw,52px)", fontWeight: 800, letterSpacing: "-0.03em" }}>Built different.</h2>
        </div>
        <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit,minmax(300px,1fr))", gap: 16 }}>
          {FEATURES.map((f, i) => (
            <div key={i} className="card"
              onMouseEnter={e => e.currentTarget.style.borderColor = f.color + "40"}
              onMouseLeave={e => e.currentTarget.style.borderColor = "var(--border)"}
            >
              <div style={{ width: 40, height: 40, borderRadius: "var(--radius-md)", background: f.color + "15", border: `1px solid ${f.color}30`, display: "flex", alignItems: "center", justifyContent: "center", fontSize: 18, color: f.color, marginBottom: 16 }}>{f.icon}</div>
              <h3 style={{ fontSize: 15, fontWeight: 700, marginBottom: 8 }}>{f.title}</h3>
              <p style={{ fontSize: 13, color: "var(--text-secondary)", lineHeight: 1.6 }}>{f.desc}</p>
            </div>
          ))}
        </div>
      </section>

      <section style={{ textAlign: "center", padding: "80px 24px 120px", maxWidth: 600, margin: "0 auto" }}>
        <h2 style={{ fontSize: "clamp(28px,4vw,44px)", fontWeight: 800, letterSpacing: "-0.03em", marginBottom: 16 }}>
          Ready to collect<br /><span style={{ color: "var(--accent-cyan)" }}>140,000 leads?</span>
        </h2>
        <p style={{ color: "var(--text-secondary)", marginBottom: 32, fontSize: 15 }}>Every business. Every city. Every niche. Enriched with owner details.</p>
        <Link to="/login" className="btn btn-primary" style={{ padding: "14px 40px", fontSize: 14 }}>Get started →</Link>
      </section>

      <footer style={{ borderTop: "1px solid var(--border)", padding: "24px 40px", display: "flex", justifyContent: "space-between", color: "var(--text-muted)", fontSize: 12 }}>
        <span>LeadScout — Universal lead intelligence</span>
        <span>Powered by automaticxai.online</span>
      </footer>
    </div>
  )
}