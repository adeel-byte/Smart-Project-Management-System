
import {
  FolderKanban,
  CheckCircle2,
  Clock3,
  ListTodo,
  TrendingUp,
  CalendarDays,
} from "lucide-react";

import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  PieChart,
  Pie,
  Cell,
} from "recharts";

import StatCard from "../components/StatCard";

const projectProgress = [
  { name: "SPMS", progress: 75 },
  { name: "Website", progress: 60 },
  { name: "Mobile App", progress: 45 },
  { name: "Database", progress: 90 },
];

const taskStatus = [
  { name: "Completed", value: 12 },
  { name: "In Progress", value: 8 },
  { name: "Pending", value: 5 },
  { name: "Blocked", value: 2 },
];

const COLORS = ["#10b981", "#3b82f6", "#f59e0b", "#ef4444"];

const recentProjects = [
  {
    name: "SPMS Development",
    manager: "Muhammad Adeel",
    progress: 75,
    status: "Active",
  },
  {
    name: "Website Redesign",
    manager: "Muhammad Taha",
    progress: 60,
    status: "Active",
  },
  {
    name: "Database Management",
    manager: "Muhammad Sufiyan",
    progress: 90,
    status: "Active",
  },
];

const deadlines = [
  {
    title: "Authentication Module",
    project: "SPMS Development",
    date: "25 Nov 2026",
    priority: "High",
  },
  {
    title: "Dashboard Design",
    project: "SPMS Development",
    date: "28 Nov 2026",
    priority: "Medium",
  },
  {
    title: "API Integration",
    project: "Website Redesign",
    date: "02 Dec 2026",
    priority: "High",
  },
];

function Dashboard() {
  return (
    <div className="space-y-7">

      {/* Welcome Section */}
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-slate-800">
            Welcome back, Adeel!
          </h1>
          <p className="mt-1 text-sm text-slate-500">
            Here's what's happening with your projects today.
          </p>
        </div>

        <div className="flex items-center gap-2 rounded-lg border border-slate-200 bg-white px-4 py-2 text-sm text-slate-600">
          <CalendarDays size={17} />
          November 2026
        </div>
      </div>

      {/* Statistics Cards */}
      <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 xl:grid-cols-4">

        <StatCard
          title="Total Projects"
          value="8"
          subtitle="Across your workspace"
          icon={FolderKanban}
          color="blue"
        />

        <StatCard
          title="Active Projects"
          value="5"
          subtitle="Currently in progress"
          icon={TrendingUp}
          color="green"
        />

        <StatCard
          title="Completed Tasks"
          value="42"
          subtitle="Successfully completed"
          icon={CheckCircle2}
          color="purple"
        />

        <StatCard
          title="Pending Tasks"
          value="15"
          subtitle="Waiting for completion"
          icon={Clock3}
          color="orange"
        />

      </div>

      {/* Charts Section */}
      <div className="grid grid-cols-1 gap-6 xl:grid-cols-3">

        {/* Project Progress Chart */}
        <div className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm xl:col-span-2">

          <div className="mb-6">
            <h3 className="font-bold text-slate-800">
              Project Progress
            </h3>
            <p className="mt-1 text-sm text-slate-400">
              Completion percentage by project
            </p>
          </div>

          <ResponsiveContainer width="100%" height={280}>
            <BarChart data={projectProgress} layout="vertical">
              <CartesianGrid strokeDasharray="3 3" horizontal={false} />
              <XAxis
                type="number"
                domain={[0, 100]}
                tickFormatter={(value) => `${value}%`}
                fontSize={12}
              />
              <YAxis
                type="category"
                dataKey="name"
                width={85}
                fontSize={12}
              />
              <Tooltip formatter={(value) => `${value}%`} />
              <Bar
                dataKey="progress"
                fill="#3b82f6"
                radius={[0, 6, 6, 0]}
                barSize={22}
              />
            </BarChart>
          </ResponsiveContainer>

        </div>

        {/* Task Status Chart */}
        <div className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">

          <h3 className="font-bold text-slate-800">
            Task Status
          </h3>

          <p className="mt-1 text-sm text-slate-400">
            Distribution of all tasks
          </p>

          <div className="mt-3">
            <ResponsiveContainer width="100%" height={210}>
              <PieChart>
                <Pie
                  data={taskStatus}
                  dataKey="value"
                  nameKey="name"
                  cx="50%"
                  cy="50%"
                  innerRadius={55}
                  outerRadius={85}
                  paddingAngle={4}
                >
                  {taskStatus.map((entry, index) => (
                    <Cell
                      key={entry.name}
                      fill={COLORS[index]}
                    />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </div>

          <div className="grid grid-cols-2 gap-3">
            {taskStatus.map((item, index) => (
              <div key={item.name} className="flex items-center gap-2">
                <span
                  className="h-2.5 w-2.5 rounded-full"
                  style={{ backgroundColor: COLORS[index] }}
                />
                <span className="text-xs text-slate-500">
                  {item.name} ({item.value})
                </span>
              </div>
            ))}
          </div>

        </div>
      </div>

      {/* Recent Projects and Deadlines */}
      <div className="grid grid-cols-1 gap-6 xl:grid-cols-3">

        {/* Recent Projects */}
        <div className="overflow-hidden rounded-xl border border-slate-200 bg-white shadow-sm xl:col-span-2">

          <div className="border-b border-slate-100 p-6">
            <h3 className="font-bold text-slate-800">
              Recent Projects
            </h3>
            <p className="mt-1 text-sm text-slate-400">
              Overview of your latest projects
            </p>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left text-sm">
              <thead className="bg-slate-50 text-xs uppercase text-slate-400">
                <tr>
                  <th className="px-6 py-4">Project</th>
                  <th className="px-6 py-4">Manager</th>
                  <th className="px-6 py-4">Progress</th>
                  <th className="px-6 py-4">Status</th>
                </tr>
              </thead>

              <tbody className="divide-y divide-slate-100">
                {recentProjects.map((project) => (
                  <tr key={project.name}>
                    <td className="whitespace-nowrap px-6 py-4 font-semibold text-slate-700">
                      {project.name}
                    </td>

                    <td className="whitespace-nowrap px-6 py-4 text-slate-500">
                      {project.manager}
                    </td>

                    <td className="min-w-36 px-6 py-4">
                      <div className="flex items-center gap-3">
                        <div className="h-2 flex-1 overflow-hidden rounded-full bg-slate-100">
                          <div
                            className="h-full rounded-full bg-blue-600"
                            style={{ width: `${project.progress}%` }}
                          />
                        </div>
                        <span className="text-xs font-semibold text-slate-600">
                          {project.progress}%
                        </span>
                      </div>
                    </td>

                    <td className="px-6 py-4">
                      <span className="rounded-full bg-emerald-50 px-3 py-1 text-xs font-semibold text-emerald-700">
                        {project.status}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

        </div>

        {/* Upcoming Deadlines */}
        <div className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">

          <div className="mb-5">
            <h3 className="font-bold text-slate-800">
              Upcoming Deadlines
            </h3>
            <p className="mt-1 text-sm text-slate-400">
              Tasks that need attention
            </p>
          </div>

          <div className="space-y-5">
            {deadlines.map((deadline) => (
              <div
                key={deadline.title}
                className="border-b border-slate-100 pb-4 last:border-0 last:pb-0"
              >
                <div className="flex items-start justify-between gap-2">
                  <div>
                    <h4 className="text-sm font-semibold text-slate-700">
                      {deadline.title}
                    </h4>

                    <p className="mt-1 text-xs text-slate-400">
                      {deadline.project}
                    </p>
                  </div>

                  <span
                    className={`rounded-md px-2 py-1 text-xs font-semibold ${
                      deadline.priority === "High"
                        ? "bg-red-50 text-red-600"
                        : "bg-amber-50 text-amber-600"
                    }`}
                  >
                    {deadline.priority}
                  </span>
                </div>

                <div className="mt-3 flex items-center gap-2 text-xs text-slate-500">
                  <CalendarDays size={14} />
                  {deadline.date}
                </div>
              </div>
            ))}
          </div>

        </div>
      </div>

    </div>
  );
}

export default Dashboard;
