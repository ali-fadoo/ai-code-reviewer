import { Bot, Github } from "lucide-react";

export default function Navbar() {
  return (
    <nav className="border-b border-zinc-800 bg-zinc-950/80 backdrop-blur sticky top-0 z-10">
      <div className="max-w-6xl mx-auto px-6 h-14 flex items-center justify-between">
        <div className="flex items-center gap-2.5">
          <div className="w-7 h-7 rounded-md bg-violet-600 flex items-center justify-center">
            <Bot size={15} className="text-white" />
          </div>
          <span className="font-semibold text-zinc-100 tracking-tight">
            AI Code Reviewer
          </span>
          <span className="text-xs text-zinc-500 font-mono bg-zinc-900 px-1.5 py-0.5 rounded">
            v1.0
          </span>
        </div>
        <a
          href="https://github.com/ali-fadoo/ai-code-reviewer"
          target="_blank"
          rel="noopener noreferrer"
          className="flex items-center gap-1.5 text-sm text-zinc-400 hover:text-zinc-100 transition-colors"
        >
          <Github size={15} />
          <span>GitHub</span>
        </a>
      </div>
    </nav>
  );
}
