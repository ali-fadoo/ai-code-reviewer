const config = {
  high: "bg-red-500/10 text-red-400 border border-red-500/20",
  medium: "bg-yellow-500/10 text-yellow-400 border border-yellow-500/20",
  low: "bg-emerald-500/10 text-emerald-400 border border-emerald-500/20",
};

export default function SeverityBadge({
  severity,
}: {
  severity: "low" | "medium" | "high";
}) {
  return (
    <span
      className={`text-xs font-medium px-2 py-0.5 rounded-full uppercase tracking-wide ${config[severity]}`}
    >
      {severity}
    </span>
  );
}
