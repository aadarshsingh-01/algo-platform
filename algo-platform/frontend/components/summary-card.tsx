type SummaryCardProps = {
  title: string;
  value: string;
};

export function SummaryCard({ title, value }: SummaryCardProps) {
  return (
    <div className="card">
      <p className="text-sm text-slate-400">{title}</p>
      <p className="mt-2 text-2xl font-semibold text-slate-100">{value}</p>
    </div>
  );
}
