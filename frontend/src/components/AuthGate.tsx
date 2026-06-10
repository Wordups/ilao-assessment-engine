import { useEffect, useState } from "react";

import { hasSupabaseConfig, supabase } from "../lib/auth";
import type { SessionState } from "../lib/api";

interface AuthGateProps {
  onReady: (session: SessionState) => void;
}

export function AuthGate({ onReady }: AuthGateProps) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [mode, setMode] = useState<"loading" | "supabase" | "development">("loading");
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!hasSupabaseConfig || !supabase) {
      setMode("development");
      return;
    }

    supabase.auth.getSession().then(({ data }) => {
      const token = data.session?.access_token;
      if (token) {
        onReady({ token });
      } else {
        setMode("supabase");
      }
    });
  }, [onReady]);

  const loginWithSupabase = async () => {
    if (!supabase) {
      return;
    }
    const { data, error: signInError } = await supabase.auth.signInWithPassword({ email, password });
    if (signInError) {
      setError(signInError.message);
      return;
    }
    onReady({ token: data.session.access_token });
  };

  if (mode === "loading") {
    return <section className="auth-card">Loading authentication...</section>;
  }

  if (mode === "development") {
    return (
      <section className="auth-card">
        <h2>Development Access</h2>
        <p>Supabase credentials were not provided, so the app is running with development authentication.</p>
        <button className="primary-button" onClick={() => onReady({ devUserId: "dev-user" })}>
          Continue as Demo User
        </button>
      </section>
    );
  }

  return (
    <section className="auth-card">
      <h2>Sign In</h2>
      <p>Use your Supabase Auth email and password to access saved assessments.</p>
      <label>
        Email
        <input value={email} onChange={(event) => setEmail(event.target.value)} type="email" />
      </label>
      <label>
        Password
        <input value={password} onChange={(event) => setPassword(event.target.value)} type="password" />
      </label>
      {error ? <p className="error-text">{error}</p> : null}
      <button className="primary-button" onClick={loginWithSupabase}>
        Sign In
      </button>
    </section>
  );
}
