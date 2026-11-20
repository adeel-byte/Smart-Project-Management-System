
import { useState } from "react";
import {
  FolderKanban,
  LockKeyhole,
  User,
  Eye,
  EyeOff,
  LoaderCircle,
} from "lucide-react";

function Login({ onLogin }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleLogin = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      const response = await fetch(
        "http://127.0.0.1:8000/api/accounts/login/",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ username, password }),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail || "Invalid username or password."
        );
      }

      onLogin(data.access, data.refresh);
    } catch (err) {
      setError(err.message || "Unable to connect to the server.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex min-h-screen items-center justify-center bg-slate-100 px-4">
      <div className="grid w-full max-w-5xl overflow-hidden rounded-2xl bg-white shadow-xl md:grid-cols-2">

        <div className="hidden flex-col justify-between bg-slate-950 p-12 text-white md:flex">
          <div>
            <div className="flex items-center gap-3">
              <div className="rounded-xl bg-blue-600 p-3">
                <FolderKanban size={26} />
              </div>
              <span className="text-2xl font-bold">SPMS</span>
            </div>

            <h1 className="mt-20 text-4xl font-bold leading-tight">
              Manage projects.
              <br />
              Empower teams.
            </h1>

            <p className="mt-5 max-w-sm text-sm leading-7 text-slate-400">
              A centralized workspace to organize projects, manage tasks,
              monitor progress, and keep your team connected.
            </p>
          </div>

          <p className="text-xs text-slate-500">
            Smart Project Management System
          </p>
        </div>

        <div className="flex items-center justify-center p-8 sm:p-12">
          <div className="w-full max-w-sm">

            <div className="mb-8 md:hidden">
              <div className="flex items-center gap-3">
                <div className="rounded-xl bg-blue-600 p-3 text-white">
                  <FolderKanban size={24} />
                </div>
                <span className="text-2xl font-bold text-slate-900">
                  SPMS
                </span>
              </div>
            </div>

            <h2 className="text-3xl font-bold text-slate-900">
              Welcome back
            </h2>
            <p className="mt-2 text-sm text-slate-500">
              Sign in to access your workspace.
            </p>

            <form onSubmit={handleLogin} className="mt-8 space-y-5">
              <div>
                <label className="mb-2 block text-sm font-semibold text-slate-700">
                  Username
                </label>
                <div className="flex items-center rounded-lg border border-slate-200 px-4 focus-within:border-blue-500">
                  <User size={18} className="text-slate-400" />
                  <input
                    type="text"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    placeholder="Enter your username"
                    required
                    className="w-full bg-transparent px-3 py-3 text-sm outline-none"
                  />
                </div>
              </div>

              <div>
                <label className="mb-2 block text-sm font-semibold text-slate-700">
                  Password
                </label>
                <div className="flex items-center rounded-lg border border-slate-200 px-4 focus-within:border-blue-500">
                  <LockKeyhole size={18} className="text-slate-400" />
                  <input
                    type={showPassword ? "text" : "password"}
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    placeholder="Enter your password"
                    required
                    className="w-full bg-transparent px-3 py-3 text-sm outline-none"
                  />
                  <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    className="text-slate-400 hover:text-slate-700"
                  >
                    {showPassword ? <EyeOff size={18} /> : <Eye size={18} />}
                  </button>
                </div>
              </div>

              {error && (
                <p className="rounded-lg bg-red-50 p-3 text-sm text-red-600">
                  {error}
                </p>
              )}

              <button
                type="submit"
                disabled={loading}
                className="flex w-full items-center justify-center gap-2 rounded-lg bg-blue-600 py-3 font-semibold text-white transition hover:bg-blue-700 disabled:cursor-not-allowed disabled:opacity-60"
              >
                {loading ? (
                  <>
                    <LoaderCircle size={18} className="animate-spin" />
                    Signing in...
                  </>
                ) : (
                  "Sign In"
                )}
              </button>
            </form>

            <p className="mt-8 text-center text-xs text-slate-400">
              © 2026 Smart Project Management System
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Login;
