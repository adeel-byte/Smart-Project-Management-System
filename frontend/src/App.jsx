
import { useState } from "react";

import Sidebar from "./components/Sidebar";
import Topbar from "./components/Topbar";
import Dashboard from "./pages/Dashboard";
import Login from "./pages/Login";

function App() {
  const [accessToken, setAccessToken] = useState(
    () => localStorage.getItem("access_token")
  );

  const [activePage, setActivePage] = useState("Dashboard");

  const handleLogin = (access, refresh) => {
    localStorage.setItem("access_token", access);
    localStorage.setItem("refresh_token", refresh);
    setAccessToken(access);
  };

  if (!accessToken) {
    return <Login onLogin={handleLogin} />;
  }

  return (
    <div className="flex min-h-screen bg-slate-50">
      <Sidebar
        activePage={activePage}
        setActivePage={setActivePage}
      />

      <div className="flex min-w-0 flex-1 flex-col">
        <Topbar activePage={activePage} />

        <main className="flex-1 overflow-y-auto p-8">
          {activePage === "Dashboard" ? (
            <Dashboard />
          ) : (
            <div className="flex min-h-96 items-center justify-center rounded-xl border border-dashed border-slate-300 bg-white">
              <div className="text-center">
                <h2 className="text-xl font-bold text-slate-700">
                  {activePage}
                </h2>
                <p className="mt-2 text-sm text-slate-400">
                  This module will be developed soon.
                </p>
              </div>
            </div>
          )}
        </main>
      </div>
    </div>
  );
}

export default App;
