const BASE = import.meta.env.VITE_API_URL
  ? `${import.meta.env.VITE_API_URL}/api`
  : "/api";

export interface ReviewSummary {
  id: number;
  pr_number: number;
  repo_full_name: string;
  pr_title: string;
  pr_url: string;
  pr_author: string;
  severity: "low" | "medium" | "high";
  status: string;
  created_at: string;
}

export interface ReviewDetail extends ReviewSummary {
  security_review: string;
  logic_review: string;
  style_review: string;
  final_review: string;
}

export interface Stats {
  total: number;
  high: number;
  medium: number;
  low: number;
}

async function get<T>(path: string): Promise<T> {
  const res = await fetch(`${BASE}${path}`);
  if (!res.ok) throw new Error(`${res.status} ${res.statusText}`);
  return res.json();
}

export const api = {
  listReviews: () => get<ReviewSummary[]>("/reviews"),
  getReview: (id: number) => get<ReviewDetail>(`/reviews/${id}`),
  getStats: () => get<Stats>("/reviews/stats"),
};
