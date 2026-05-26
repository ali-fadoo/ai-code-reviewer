import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import ReactMarkdown from "react-markdown";
import { ArrowLeft, ShieldAlert, Bug, Paintbrush, Sparkles, ExternalLink } from "lucide-react";
import { api, type ReviewDetail } from "../api/client";
import SeverityBadge from "../components/SeverityBadge";

type TabKey = "final" | "security" | "logic" | "style";

const TABS: { key: TabKey; label: string; icon: React.ElementType }[] = [
  { key: "final", label: "Summary", icon: Sparkles },
  { key: "security", label: "Security", icon: ShieldAlert },
  { key: "logic", label: "Logic", icon: Bug },
  { key: "style", label: "Style", icon: Paintbrush },
];

export default function ReviewDetailPage() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [review, setReview] = useState<ReviewDetail | null>(null);
  const [tab, setTab] = useState<TabKey>("final");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api
      .getReview(Number(id))
      .then(setReview)
      .finally(() => setLoading(false));
  }, [id]);

  const content: Record<TabKey, string | null> = review
    ? {
        final: review.final_review,
        security: review.security_review,
        logic: review.logic_review,
        style: review.style_review,
      }
    : { final: null, security: null, logic: null, style: null };

  return (
    <div className="max-w-4xl mx-auto px-6 py-10">
      <button
        onClick={() => navigate("/")}
        className="flex items-center gap-1.5 text-sm text-zinc-500 hover:text-zinc-100 transition-colors mb-8"
      >
        <ArrowLeft size={14} />
        Back to dashboard
      </button>

      {loading && (
        <div className="text-zinc-600 text-sm py-20 text-center">
          Loading review...
        </div>
      )}

      {review && (
        <>
          <div className="mb-6">
            <div className="flex items-start justify-between gap-4">
              <div>
                <h1 className="text-xl font-bold text-zinc-100">
                  {review.pr_title}
                </h1>
                <div className="flex items-center gap-3 mt-2 text-sm text-zinc-500">
                  <span className="font-mono">{review.repo_full_name}</span>
                  <span>·</span>
                  <span>PR #{review.pr_number}</span>
                  <span>·</span>
                  <span>by {review.pr_author}</span>
                </div>
              </div>
              <div className="flex items-center gap-2 shrink-0">
                <SeverityBadge severity={review.severity} />
                <a
                  href={review.pr_url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="flex items-center gap-1 text-xs text-zinc-500 hover:text-violet-400 transition-colors"
                >
                  <ExternalLink size={12} />
                  PR
                </a>
              </div>
            </div>
          </div>

          <div className="flex gap-1 mb-6 border-b border-zinc-800">
            {TABS.map(({ key, label, icon: Icon }) => (
              <button
                key={key}
                onClick={() => setTab(key)}
                className={`flex items-center gap-1.5 px-4 py-2.5 text-sm font-medium border-b-2 -mb-px transition-colors ${
                  tab === key
                    ? "border-violet-500 text-violet-400"
                    : "border-transparent text-zinc-500 hover:text-zinc-300"
                }`}
              >
                <Icon size={13} />
                {label}
              </button>
            ))}
          </div>

          <div className="bg-zinc-900 border border-zinc-800 rounded-xl p-6">
            <div className="prose-dark">
              <ReactMarkdown>{content[tab] || "_No content._"}</ReactMarkdown>
            </div>
          </div>
        </>
      )}
    </div>
  );
}
