import { useEffect, useState } from "react"
import { Navigate, Route, BrowserRouter as Router, Routes } from "react-router-dom"
import AdminPage from "./pages/AdminPage"
import DashboardPage from "./pages/DashboardPage"
import HomePage from "./pages/HomePage"
import LoginPage from "./pages/LoginPage"
import ProfilePage from "./pages/ProfilePage"

export default function App() {
  const [user, setUser] = useState(null)

  useEffect(() => {
    const stored = localStorage.getItem("ls_user")
    if (stored) setUser(JSON.parse(stored))
  }, [])

  const login = (userData) => {
    localStorage.setItem("ls_user", JSON.stringify(userData))
    setUser(userData)
  }

  const logout = () => {
    localStorage.removeItem("ls_user")
    setUser(null)
  }

  return (
    <Router>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/login" element={<LoginPage onLogin={login} />} />
        <Route path="/dashboard" element={user ? <DashboardPage user={user} onLogout={logout} /> : <Navigate to="/login" />} />
        <Route path="/profile" element={user ? <ProfilePage user={user} onLogout={logout} /> : <Navigate to="/login" />} />
        <Route path="/admin" element={user?.role === "admin" ? <AdminPage user={user} onLogout={logout} /> : <Navigate to="/dashboard" />} />
      </Routes>
    </Router>
  )
}