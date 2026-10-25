
import { useState } from "react";
import api from "./api";
import Dashboard from "./components/Dashboard.jsx";
import "./App.css";

const initialForm = {
  email: "",
  password: "",
  first_name: "",
  last_name: "",
};

function getErrorMessage(error) {
  const data = error.response?.data;

  if (!data) {
    return "Cannot connect to the server. Make sure Django is running.";
  }

  if (typeof data.detail === "string") {
    return data.detail;
  }

  if (typeof data === "object") {
    return Object.entries(data)
      .map(([field, messages]) => {
        const text = Array.isArray(messages)
          ? messages.join(" ")
          : String(messages);

        return `${
          field === "non_field_errors"
            ? "Error"
            : field.replaceAll("_", " ")
        }: ${text}`;
      })
      .join(" ");
  }

  return "Something went wrong. Please try again.";
}

function App() {
  const [mode, setMode] = useState("login");
  const [form, setForm] = useState(initialForm);
  const [error, setError] = useState("");
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);

  const [userEmail, setUserEmail] = useState(
    () => sessionStorage.getItem("petUserEmail") || "",
  );

  const [accessToken, setAccessToken] = useState(
    () => sessionStorage.getItem("petAccessToken") || "",
  );

  const isRegister = mode === "register";
  const isSignedIn = Boolean(accessToken);

  function handleChange(event) {
    const { name, value } = event.target;

    setForm((previous) => ({
      ...previous,
      [name]: value,
    }));

    setError("");
    setMessage("");
  }

  function switchMode(nextMode) {
    setMode(nextMode);
    setForm(initialForm);
    setError("");
    setMessage("");
  }

  async function handleSubmit(event) {
    event.preventDefault();
    setError("");
    setMessage("");

    if (!form.email.trim() || !form.password) {
      setError("Please enter your email and password.");
      return;
    }

    if (isRegister && form.password.length < 8) {
      setError("Your password must contain at least 8 characters.");
      return;
    }

    setLoading(true);

    try {
      const email = form.email.trim().toLowerCase();

      if (isRegister) {
        await api.post("/auth/register/", {
          email,
          password: form.password,
          first_name: form.first_name.trim(),
          last_name: form.last_name.trim(),
        });

        setMessage("Account created successfully. You can now log in.");
        setForm({
          ...initialForm,
          email,
        });
        setMode("login");
      } else {
        const response = await api.post("/auth/login/", {
          email,
          password: form.password,
        });

        sessionStorage.setItem("petAccessToken", response.data.access);
        sessionStorage.setItem("petRefreshToken", response.data.refresh);
        sessionStorage.setItem("petUserEmail", email);

        setAccessToken(response.data.access);
        setUserEmail(email);
        setForm(initialForm);
      }
    } catch (requestError) {
      setError(getErrorMessage(requestError));
    } finally {
      setLoading(false);
    }
  }

  function handleLogout() {
    sessionStorage.removeItem("petAccessToken");
    sessionStorage.removeItem("petRefreshToken");
    sessionStorage.removeItem("petUserEmail");

    setAccessToken("");
    setUserEmail("");
    setForm(initialForm);
    setError("");
    setMessage("You have logged out.");
    setMode("login");
  }

  if (isSignedIn) {
    return (
      <Dashboard
        email={userEmail}
        onLogout={handleLogout}
      />
    );
  }

  return (
    <main className="pet-app">
      <header className="topbar">
        <a className="brand" href="#home" aria-label="PetFriendly home">
          <span className="brand-icon" aria-hidden="true">🐾</span>
          <span>
            pet<span className="brand-accent">friendly</span>
          </span>
        </a>

        <div className="topbar-note">A happier life for every pet</div>
      </header>

      <section className="auth-layout">
        <div className="hero-panel">
          <span className="eyebrow">MORE LOVE. MORE WAGGING. MORE LIFE.</span>

          <h1>
            Every pet deserves a little more <span>love.</span>
          </h1>

          <p>
            Your companion for pet care, adoption, trusted services, and
            everyday moments with the animals you love.
          </p>

          <div
            className="pet-illustration"
            aria-label="Illustrations of a dog, cat, and rabbit"
          >
            <span className="pet-bubble bubble-one">🐶</span>
            <span className="pet-bubble bubble-two">🐱</span>
            <span className="pet-bubble bubble-three">🐰</span>
            <span className="pet-heart heart-one">♥</span>
            <span className="pet-heart heart-two">♥</span>
          </div>

          <div className="hero-benefits">
            <span><span aria-hidden="true">✓</span> Care for different kinds of pets</span>
            <span><span aria-hidden="true">✓</span> Discover adoption and pet services</span>
            <span><span aria-hidden="true">✓</span> Keep important care details together</span>
          </div>
        </div>

        <div className="auth-panel">
          <div className="auth-heading">
            <span className="eyebrow">
              {isRegister ? "JOIN OUR PET COMMUNITY" : "WELCOME BACK"}
            </span>

            <h2>
              {isRegister ? "Create your account" : "Let’s get you home."}
            </h2>

            <p>
              {isRegister
                ? "Create an account to begin your pet-friendly journey."
                : "Sign in to continue your pet-friendly journey."}
            </p>
          </div>

          <div className="auth-tabs" role="tablist" aria-label="Account options">
            <button
              type="button"
              role="tab"
              aria-selected={!isRegister}
              className={!isRegister ? "auth-tab active" : "auth-tab"}
              onClick={() => switchMode("login")}
            >
              Log in
            </button>

            <button
              type="button"
              role="tab"
              aria-selected={isRegister}
              className={isRegister ? "auth-tab active" : "auth-tab"}
              onClick={() => switchMode("register")}
            >
              Sign up
            </button>
          </div>

          {error && (
            <div className="form-message error-message" role="alert">
              {error}
            </div>
          )}

          {message && (
            <div className="form-message success-message" role="status">
              {message}
            </div>
          )}

          <form className="auth-form" onSubmit={handleSubmit}>
            {isRegister && (
              <div className="name-fields">
                <label>
                  First name
                  <input
                    type="text"
                    name="first_name"
                    value={form.first_name}
                    onChange={handleChange}
                    autoComplete="given-name"
                    maxLength={150}
                    placeholder="Your first name"
                  />
                </label>

                <label>
                  Last name
                  <input
                    type="text"
                    name="last_name"
                    value={form.last_name}
                    onChange={handleChange}
                    autoComplete="family-name"
                    maxLength={150}
                    placeholder="Your last name"
                  />
                </label>
              </div>
            )}

            <label>
              Email address
              <input
                type="email"
                name="email"
                value={form.email}
                onChange={handleChange}
                autoComplete="email"
                placeholder="you@example.com"
                maxLength={254}
                required
              />
            </label>

            <label>
              Password
              <input
                type="password"
                name="password"
                value={form.password}
                onChange={handleChange}
                autoComplete={isRegister ? "new-password" : "current-password"}
                placeholder={
                  isRegister ? "Create a strong password" : "Enter your password"
                }
                required
              />
            </label>

            {isRegister && (
              <p className="field-hint">
                Use a strong password. Your password is never displayed in
                your account details.
              </p>
            )}

            <button
              className="button button-primary submit-button"
              type="submit"
              disabled={loading}
            >
              {loading
                ? "Please wait…"
                : isRegister
                  ? "Create account"
                  : "Log in"}

              {!loading && <span aria-hidden="true">→</span>}
            </button>
          </form>

          <p className="switch-prompt">
            {isRegister ? "Already have an account?" : "New to PetFriendly?"}{" "}
            <button
              type="button"
              className="text-button"
              onClick={() => switchMode(isRegister ? "login" : "register")}
            >
              {isRegister ? "Log in" : "Create an account"}
            </button>
          </p>

          <p className="privacy-note">
            By continuing, you agree to use the platform responsibly and
            protect your account details.
          </p>
        </div>
      </section>

      <footer className="site-footer">
        Made for every paw, wing, fin, and little friend.{" "}
        <span aria-hidden="true">♥</span>
      </footer>
    </main>
  );
}

export default App;
