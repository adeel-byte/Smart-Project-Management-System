
import {
  LayoutDashboard,
  FolderKanban,
  CheckSquare,
  CalendarDays,
  ShieldAlert,
  BarChart3,
  Bell,
  Users,
  Settings,
  LogOut,
  BriefcaseBusiness,
  ChevronLeft,
  ChevronRight,
} from "lucide-react";

const navigation = [
  {
    title: "WORKSPACE",
    items: [
      { name: "Dashboard", icon: LayoutDashboard },
      { name: "Projects", icon: FolderKanban },
      { name: "My Tasks", icon: CheckSquare },
      { name: "Milestones", icon: CalendarDays },
    ],
  },
  {
    title: "MANAGEMENT",
    items: [
      { name: "Risk Management", icon: ShieldAlert },
      { name: "Reports & Analytics", icon: BarChart3 },
      { name: "Team Members", icon: Users },
      { name: "Notifications", icon: Bell },
    ],
  },
];

function Sidebar({ activePage, setActivePage }) {
  return (
    <aside className="flex h-screen w-64 flex-col bg-slate-950 text-slate-300">

      {/* Brand */}
      <div className="flex h-20 items-center gap-3 border-b border-white/10 px-6">
        <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-blue-600">
          <BriefcaseBusiness size={22} className="text-white" />
        </div>

        <div>
          <h1 className="text-lg font-bold tracking-wide text-white">
            SPMS
          </h1>
          <p className="text-xs text-slate-400">
            Project Management
          </p>
        </div>
      </div>

      {/* Navigation */}
      <nav className="flex-1 space-y-8 overflow-y-auto px-4 py-7">
        {navigation.map((section) => (
          <div key={section.title}>
            <p className="mb-3 px-3 text-xs font-semibold tracking-widest text-slate-500">
              {section.title}
            </p>

            <div className="space-y-1">
              {section.items.map((item) => {
                const Icon = item.icon;
                const isActive = activePage === item.name;

                return (
                  <button
                    key={item.name}
                    onClick={() => setActivePage(item.name)}
                    className={`flex w-full items-center gap-3 rounded-lg px-3 py-3 text-sm font-medium transition-all ${
                      isActive
                        ? "bg-blue-600 text-white shadow-lg shadow-blue-950/40"
                        : "text-slate-400 hover:bg-white/5 hover:text-white"
                    }`}
                  >
                    <Icon size={19} />
                    <span>{item.name}</span>
                  </button>
                );
              })}
            </div>
          </div>
        ))}
      </nav>

      {/* Settings */}
      <div className="border-t border-white/10 p-4">
        <button
          onClick={() => setActivePage("Settings")}
          className={`flex w-full items-center gap-3 rounded-lg px-3 py-3 text-sm transition ${
            activePage === "Settings"
              ? "bg-blue-600 text-white"
              : "text-slate-400 hover:bg-white/5 hover:text-white"
          }`}
        >
          <Settings size={19} />
          Settings
        </button>

        <div className="mt-3 flex items-center gap-3 rounded-lg bg-white/5 p-3">
          <div className="flex h-9 w-9 items-center justify-center rounded-full bg-blue-500 text-sm font-bold text-white">
            A
          </div>
          <div className="min-w-0 flex-1">
            <p className="truncate text-sm font-semibold text-white">
              Muhammad Adeel
            </p>
            <p className="text-xs text-slate-400">
              Project Manager
            </p>
          </div>
          <LogOut size={17} className="cursor-pointer text-slate-400 hover:text-white" />
        </div>
      </div>
    </aside>
  );
}

export default Sidebar;
