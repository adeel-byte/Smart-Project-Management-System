
import {
  Search,
  Bell,
  ChevronDown,
  HelpCircle,
} from "lucide-react";

function Topbar({ activePage }) {
  return (
    <header className="flex h-20 items-center justify-between border-b border-slate-200 bg-white px-8">

      {/* Page Information */}
      <div>
        <div className="flex items-center gap-2 text-xs text-slate-400">
          <span>SPMS</span>
          <span>/</span>
          <span className="text-blue-600">{activePage}</span>
        </div>

        <h2 className="mt-1 text-xl font-bold text-slate-800">
          {activePage}
        </h2>
      </div>

      {/* Right Side */}
      <div className="flex items-center gap-5">

        {/* Search */}
        <div className="flex w-64 items-center gap-2 rounded-lg border border-slate-200 bg-slate-50 px-3 py-2">
          <Search size={18} className="text-slate-400" />

          <input
            type="text"
            placeholder="Search anything..."
            className="w-full bg-transparent text-sm text-slate-700 outline-none placeholder:text-slate-400"
          />

          <span className="rounded border border-slate-200 bg-white px-1.5 py-0.5 text-xs text-slate-400">
            /
          </span>
        </div>

        {/* Help */}
        <button
          type="button"
          aria-label="Help"
          className="text-slate-400 transition hover:text-blue-600"
        >
          <HelpCircle size={20} />
        </button>

        {/* Notifications */}
        <button
          type="button"
          aria-label="Notifications"
          className="relative rounded-lg p-2 text-slate-500 transition hover:bg-slate-100 hover:text-blue-600"
        >
          <Bell size={21} />

          <span className="absolute right-1.5 top-1.5 h-2 w-2 rounded-full border-2 border-white bg-red-500"></span>
        </button>

        {/* User Profile */}
        <button
          type="button"
          className="flex items-center gap-3 border-l border-slate-200 pl-5"
        >
          <div className="flex h-10 w-10 items-center justify-center rounded-full bg-blue-100 font-bold text-blue-700">
            A
          </div>

          <div className="text-left">
            <p className="text-sm font-semibold text-slate-800">
              Muhammad Adeel
            </p>

            <p className="text-xs text-slate-400">
              Project Manager
            </p>
          </div>

          <ChevronDown size={16} className="text-slate-400" />
        </button>

      </div>
    </header>
  );
}

export default Topbar;
