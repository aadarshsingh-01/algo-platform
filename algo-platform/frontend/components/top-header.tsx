export function TopHeader() {
  return (
    <header className="flex h-16 items-center justify-between border-b border-border bg-surface px-6">
      <p className="text-sm text-slate-400">Paper Trading V1</p>
      <div className="rounded-full bg-cyan-500/20 px-3 py-1 text-xs font-medium text-cyan-300">Demo Mode</div>
    </header>
  );
}
