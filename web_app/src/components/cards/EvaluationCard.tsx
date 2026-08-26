import { useEffect, useState } from "react";
import { fetchJson } from "../../services/fetchJson";
import SectionCard from "./SectionCard";
import type { EvaluationMetrics } from "../../types/evaluation";

export default function EvaluationCard() {
  const [metrics, setMetrics] = useState<EvaluationMetrics | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    fetchJson("/data/evaluation_metrics.json")
      .then((data) => setMetrics(data as EvaluationMetrics))
      .catch((err) => console.error("Error loading metrics:", err))
      .finally(() => setIsLoading(false));
  }, []);

  if (isLoading) {
    return (
      <SectionCard title="Model Performance">
        <div className="flex h-32 items-center justify-center text-neutral-500 font-mono">
          Loading Metrics...
        </div>
      </SectionCard>
    );
  }

  if (!metrics) return null;

  return (
    <SectionCard title="Model Backtesting (2024-2026)">
      <div className="space-y-4 font-mono text-sm">
        
        {/* Random Forest Accuracy vs Baseline */}
        <div className="flex flex-col gap-2 border-b border-neutral-800/50 pb-4">
          <div className="flex justify-between items-end">
            <span className="text-neutral-400">Random Forest Accuracy</span>
            <span className={`text-2xl font-black ${metrics.isOutperforming ? 'text-emerald-400' : 'text-neutral-100'}`}>
              {metrics.rfAccuracy}%
            </span>
          </div>
          <div className="flex justify-between items-center text-xs">
            <span className="text-neutral-500">Grid Baseline (Pole = Win)</span>
            <span className="font-bold text-neutral-300">{metrics.baselineAccuracy}%</span>
          </div>
        </div>

        {/* Top 3 Coverage */}
        <div className="flex justify-between items-center border-b border-neutral-800/50 pb-3 pt-1">
          <span className="text-neutral-400">Podium Coverage (Top 3)</span>
          <span className="font-bold text-sky-400 text-lg">{metrics.rfTop3Coverage}%</span>
        </div>

        {/* Context Footer */}
        <div className="pt-1 text-xs text-neutral-600 text-center">
          Evaluated on {metrics.totalRaces} unseen races.
        </div>

      </div>
    </SectionCard>
  );
}