import { useEffect, useState } from "react";
import { ShieldAlert, Bug, Paintbrush, GitMerge } from "lucide-react";
import { api, type ReviewSummary, type Stats } from "../api/client";
import ReviewCard from "../components/ReviewCard";

function StatCard({
  label,
  value,
  icon: Icon,
  color,
}: {
  label: string;
  value: number;
  icon: React.ElementType;
  color: string;
}) {
  return (
    <div className="bg-zinc-900 border border-zinc-800 rounded-xl p-5 flex items-center gap-4">
      <div className={`w-10 h-10 rounded-lg flex items-center justify-center ${color}`}>
        <Icon size={18} />
      </div>
      <div>
        <p className="text-2xl font-bold text-zinc-100">{value}</p>
        <p className="text-xs text-zinc-500">{label}</p>
      </div>
    </div>
  );
}

export default function Dashboard() {
  const [reviews, setReviews] = useState<ReviewSummary[]>([]);
  const [stats, setStats] = useState<Stats | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    Promise.all([api.listReviews(), api.getStats()])
      .then(([r, s]) => {
        setReviews(r);
        setStats(s);
      })
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, []);

  return (
    <div className="max-w-6xl mx-auto px-6 py-10">
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-zinc-100">Review Dashboard</h1>
        <p className="text-zinc-500 text-sm mt-1">
          Multi-agent AI reviews across security, logic, and style
        </p>
      </div>

      {stats && (
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-10">
          <StatCard
            label="Total Reviews"
            value={stats.total}
            icon={GitMerge}
            color="bg-violet-500/10 text-violet-400"
          />
          <StatCard
            label="High Severity"
            value={stats.high}
            icon={ShieldAlert}
            color="bg-red-500/10 text-red-400"
          />
          <StatCard
            label="Medium Severity"
            value={stats.medium}
            icon={Bug}
            color="bg-yellow-500/10 text-yellow-400"
          />
          <StatCard
            label="Low Severity"
            value={stats.low}
            icon={Paintbrush}
            color="bg-emerald-500/10 text-emerald-400"
          />
        </div>
      )}

      <div className="flex items-center justify-between mb-4">
        <h2 className="text-sm font-medium text-zinc-400 uppercase tracking-widest">
          Recent Reviews
        </h2>
      </div>

      {loading && (
        <div className="flex items-center justify-center py-20 text-zinc-600 text-sm">
          Loading reviews...
        </div>
      )}

      {error && (
        <div className="bg-red-500/10 border border-red-500/20 rounded-xl p-6 text-red-400 text-sm">
          Could not connect to backend: {error}
        </div>
      )}

      {!loading && !error && reviews.length === 0 && (
        <div className="border border-dashed border-zinc-800 rounded-xl p-16 text-center">
          <GitMerge size={32} className="text-zinc-700 mx-auto mb-3" />
          <p className="text-zinc-500 text-sm">No reviews yet.</p>
          <p className="text-zinc-600 text-xs mt-1">
            Open a pull request in a repo where this app is installed.
          </p>
        </div>
      )}

      <div className="space-y-3">
        {reviews.map((r) => (
          <ReviewCard key={r.id} review={r} />
        ))}
      </div>
    </div>
  );
}
