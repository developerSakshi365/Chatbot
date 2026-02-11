import { useEffect, useState, useCallback } from "react";
import "../styles/Login.css";
import "../styles/responsive.css";

const GOOGLE_CLIENT_ID = process.env.REACT_APP_GOOGLE_CLIENT_ID;
const API_URL = process.env.REACT_APP_API_URL;

function Login({ onLogin }) {
  const [isLogin, setIsLogin] = useState(true);
  const [formData, setFormData] = useState({
    email: "",
    password: "",
    name: ""
  });
  const [loading, setLoading] = useState(false);

  const handleGoogleLogin = useCallback(async (response) => {
    setLoading(true);

    try {
      const res = await fetch(`${API_URL}/google-login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ token: response.credential })
      });

      const data = await res.json();

      if (!res.ok) {
        alert("Google login failed");
        return;
      }

      localStorage.setItem("user", JSON.stringify(data));
      onLogin(data);
    } catch (err) {
      alert("Google login error");
    } finally {
      setLoading(false);
    }
  }, [onLogin]);

  useEffect(() => {
    if (!GOOGLE_CLIENT_ID) {
      console.error("❌ Google Client ID is missing");
      return;
    }

    const interval = setInterval(() => {
      if (window.google) {
        clearInterval(interval);

        window.google.accounts.id.initialize({
          client_id: GOOGLE_CLIENT_ID,
          callback: handleGoogleLogin
        });

        window.google.accounts.id.renderButton(
          document.getElementById("google-login-btn"),
          {
            theme: "outline",
            size: "large",
            width: 350,
            text: "signin_with",
            shape: "rectangular"
          }
        );
      }
    }, 300);

    return () => clearInterval(interval);
  }, [handleGoogleLogin]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    const endpoint = isLogin ? "login" : "signup";

    try {
      const res = await fetch(`${API_URL}/${endpoint}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData)
      });

      const data = await res.json();

      if (!res.ok) {
        alert(data.detail || "Error");
        return;
      }

      localStorage.setItem("user", JSON.stringify(data));
      onLogin(data);
    } catch (err) {
      alert("Connection error. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  return (
    <div className="login-container">
      <div className="login-box">
        <div className="logo-section">
          <div className="logo-icon">🤖</div>
          <h1>ChatBot AI</h1>
          <p className="subtitle">Welcome back! Please sign in to continue</p>
        </div>

        <form onSubmit={handleSubmit}>
          {!isLogin && (
            <div className="input-group">
              <label>Full Name</label>
              <input
                name="name"
                placeholder="Enter your full name"
                value={formData.name}
                onChange={handleChange}
                required
                disabled={loading}
              />
            </div>
          )}

          <div className="input-group">
            <label>Email Address</label>
            <input
              name="email"
              type="email"
              placeholder="Enter your email"
              value={formData.email}
              onChange={handleChange}
              required
              disabled={loading}
            />
          </div>

          <div className="input-group">
            <label>Password</label>
            <input
              name="password"
              type="password"
              placeholder="Enter your password"
              value={formData.password}
              onChange={handleChange}
              required
              disabled={loading}
            />
          </div>

          <button type="submit" className="submit-btn" disabled={loading}>
            {loading ? "Please wait..." : isLogin ? "Sign In" : "Create Account"}
          </button>
        </form>

        <div className="divider">
          <span>OR CONTINUE WITH</span>
        </div>

        <div className="google-btn-wrapper">
          <div id="google-login-btn"></div>
        </div>

        <p className="toggle" onClick={() => !loading && setIsLogin(!isLogin)}>
          {isLogin ? "Don't have an account? Sign Up" : "Already have an account? Sign In"}
        </p>
      </div>
    </div>
  );
}

export default Login;
