interface PredictionCardProps {
  winner: string;
  probability: number;
}

export default function PredictionCard({
  winner,
  probability,
}: PredictionCardProps) {
  return (
    <div className="rounded-xl border border-slate-700 bg-slate-900 p-5">
      <h2 className="text-xl font-bold">
        Predicted Winner
      </h2>

      <p className="mt-4 text-2xl">
        {winner}
      </p>

      <p className="text-slate-400">
        {(probability * 100).toFixed(1)}%
      </p>
    </div>
  );
}