import { Link, useLocation } from "react-router-dom"

export default function Nav({ user, onLogout }) {
  const loc = useLocation()

  return (
    <nav className="nav">
      <Link to="/" className="nav-logo">Lead<span>Scout</span></Link>
      <div className="nav-links">
        {user ? (
          <>
            <Link to="/dashboard" className={`nav-link ${loc.pathname === "/dashboard" ? "active" : ""}`}>Dashboard</Link>
            <Link to="/profile"   className={`nav-link ${loc.pathname === "/profile"   ? "active" : ""}`}>Profile</Link>
            {user.role === "admin" && (
              <Link to="/admin" className={`nav-link ${loc.pathname === "/admin" ? "active" : ""}`}>Admin</Link>
            )}
            <div style={{ width: 1, height: 20, background: "var(--border)", margin: "0 8px" }} />
            <button className="btn btn-ghost" style={{ padding: "6px 14px" }} onClick={onLogout}>Sign out</button>
          </>
        ) : (
          <Link to="/login" className="btn btn-primary" style={{ padding: "8px 20px" }}>Sign in</Link>
        )}
      </div>
    </nav>
  )
}