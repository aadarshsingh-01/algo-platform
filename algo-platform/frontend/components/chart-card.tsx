"use client";

import { Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";

const data = [
  { t: "09:15", equity: 100000 },
  { t: "10:00", equity: 100650 },
  { t: "11:00", equity: 101200 },
  { t: "12:00", equity: 100900 },
  { t: "13:00", equity: 101850 },
  { t: "14:00", equity: 102400 }
];

export function ChartCard() {
  return (
    <div className="card">
      <h3 className="mb-4 text-lg font-semibold">Equity Curve</h3>
      <div className="h-72 w-full">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={data}>
            <XAxis dataKey="t" stroke="#7c8ca8" />
            <YAxis stroke="#7c8ca8" />
            <Tooltip />
            <Line type="monotone" dataKey="equity" stroke="#22d3ee" strokeWidth={2} dot={false} />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
