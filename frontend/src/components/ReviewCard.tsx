import { GitPullRequest, User, ExternalLink } from "lucide-react";
import { useNavigate } from "react-router-dom";
import type { ReviewSummary } from "../api/client";
import SeverityBadge from "./SeverityBadge";

export default function ReviewCard({ review }: { review: ReviewSummary }) {
  const navigate = useNavigate();
  const date = new Date(review.created_at).toLocaleDateString("en-US", {
    month: "short",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });

  return (
    <div
      onClick={() => navigate(`/review/${review.id}`)}
      className="group bg-zinc-900 border border-zinc-800 rounded-xl p-5 cursor-pointer hover:border-zinc-700 hover:bg-zinc-800/60 transition-all duration-150"
    >
      <div className="flex items-start justify-between gap-3">
        <div className="flex items-center gap-2 min-w-0">
          <GitPullRequest size={15} className="text-violet-400 shrink-0" />
          <span className="text-sm font-mono text-zinc-400 shrink-0">
            #{review.pr_number}
          </span>
          <span className="text-sm text-zinc-100 font-medium truncate">
            {review.pr_title}
          </span>
        </div>
        <SeverityBadge severity={review.severity} />
      </div>

      <div className="mt-3 flex items-center gap-4 text-xs text-zinc-500">
        <span className="flex items-center gap-1">
          <User size={11} />
          {review.pr_author}
        </span>
        <span className="font-mono">{review.repo_full_name}</span>
        <span className="ml-auto">{date}</span>
      </div>

      <div className="mt-3 flex items-center gap-3">
        <a
          href={review.pr_url}
          target="_blank"
          rel="noopener noreferrer"
          onClick={(e) => e.stopPropagation()}
          className="flex items-center gap-1 text-xs text-zinc-500 hover:text-violet-400 transition-colors"
        >
          <ExternalLink size={11} />
          View PR
        </a>
        <span className="text-xs text-zinc-600 group-hover:text-zinc-400 transition-colors ml-auto">
          See full review →
        </span>
      </div>
    </div>
  );
}
