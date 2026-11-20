
function StatCard({ title, value, subtitle, icon: Icon, color }) {
  const colorStyles = {
    blue: "bg-blue-50 text-blue-600",
    green: "bg-emerald-50 text-emerald-600",
    purple: "bg-purple-50 text-purple-600",
    orange: "bg-orange-50 text-orange-600",
  };

  return (
    <div className="rounded-xl border border-slate-200 bg-white p-5 shadow-sm transition duration-200 hover:-translate-y-1 hover:shadow-md">

      <div className="flex items-center justify-between">
        <p className="text-sm font-medium text-slate-500">
          {title}
        </p>

        <div className={`rounded-xl p-3 ${colorStyles[color] || colorStyles.blue}`}>
          {Icon && <Icon size={21} />}
        </div>
      </div>

      <div className="mt-4">
        <h3 className="text-3xl font-bold tracking-tight text-slate-800">
          {value}
        </h3>

        <p className="mt-2 text-xs text-slate-400">
          {subtitle}
        </p>
      </div>

    </div>
  );
}

export default StatCard;
