import { useEffect, useState } from "react";
import { fetchJson } from "../services/fetchJson";
import SectionCard from "../components/cards/SectionCard"; 
import type { WeekendState } from "../types/weekend";
import ScrollWrapper from "../components/layout/ScrollWrapper";
import { getPredictions } from '../services/predictions';
import type { Prediction } from '../types/prediction';

// Helper for Rain Probability text colors
function getRainColorClass(probability: number): string {
  if (probability < 30) return "text-yellow-400";
  if (probability <= 70) return "text-emerald-400"; // Tailwind's standard green
  return "text-sky-400";
}

// Helper for Tire Compound badge styling
function getTireStyles(compound: string): string {
  const norm = compound.toLowerCase();
  
  switch (norm) {
    case "soft":
    case "softs":
      return "bg-red-950 text-red-400 border-red-800/50";
    case "medium":
    case "mediums":
      return "bg-yellow-950 text-yellow-400 border-yellow-800/50";
    case "hard":
    case "hards":
      return "bg-neutral-800 text-neutral-100 border-neutral-600/50";
    case "inter":
    case "inters":
    case "intermediate":
      return "bg-emerald-950 text-emerald-400 border-emerald-800/50";
    case "wet":
    case "wets":
      return "bg-blue-950 text-blue-400 border-blue-800/50";
    default:
      return "bg-neutral-900 text-neutral-400 border-neutral-800";
  }
}


export default function RaceHub() {
  // 1. Pass the type to useState so TypeScript knows the shape of your data
  const [weekendData, setWeekendData] = useState<WeekendState | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(true);

  const [predictions, setPredictions] = useState<Prediction[]>([]);
  const [isLoadingPredictions, setIsLoadingPredictions] = useState(true);

  useEffect(() => {
    fetchJson("/data/weekend_state.json")
      .then((data) => setWeekendData(data as WeekendState))
      .catch((err) => console.error("Error loading weekend state:", err))
      .finally(() => setIsLoading(false));
  }, []);
  useEffect(() => {
    getPredictions()
      .then((data) => setPredictions(data))
      .catch((err) => console.error("Error loading predictions:", err))
      .finally(() => setIsLoadingPredictions(false));
  }, []);

  // 2. Wrap bare text in a JSX element (e.g., <div> or <p>)
  if (isLoading || !weekendData) {
    return <div>Loading Pit Wall Data...</div>;
  }

  const { track, weather, telemetry } = weekendData;

  return (
  <div className="min-h-screen bg-neutral-950 p-6 text-neutral-100 font-sans">
    {/* Header Section */}
    <header className="mb-8 border-b border-neutral-800 pb-4">
      <div className="flex items-center gap-3">
        <h1 className="font-mono text-4xl font-black uppercase tracking-tight text-white">
          {track.circuitName}
        </h1>
        <span className="rounded bg-neutral-800 border border-neutral-700 px-2.5 py-0.5 text-xs font-semibold text-neutral-300">
        Round Projected
        </span>
      </div>
      <p className="text-sm font-semibold uppercase tracking-widest text-red-500 mt-1">
        Race Weekend Hub
      </p>
    </header>

    {/* Dashboard Layout Grid with explicit gaps */}
    <main className="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-3">
      
      {/* Environment: Weather */}
      <SectionCard title="Weather">
        <div className="space-y-3 font-mono text-sm">
          <div className="flex justify-between border-b border-neutral-800/50 pb-1">
            <span className="text-neutral-400">Track Temp</span>
            <span className="font-bold text-white">{weather.trackTemp}°C</span>
          </div>
          <div className="flex justify-between border-b border-neutral-800/50 pb-1">
            <span className="text-neutral-400">Air Temp</span>
            <span className="font-bold text-white">{weather.airTemp}°C</span>
          </div>
          {/* Updated Rain Probability Row */}
        <div className="flex justify-between pb-1">
  <span className="text-neutral-400">Rain Probability</span>
  <span className={`font-bold ${getRainColorClass(weather.rainProbability)}`}>
    {weather.rainProbability}% ({weather.condition})
  </span>
</div>

        </div>
      </SectionCard>

      {/* Environment: Track Profile */}
      <SectionCard title="Track Profile">
        <div className="space-y-3 font-mono text-sm">
          <div className="flex justify-between border-b border-neutral-800/50 pb-1">
            <span className="text-neutral-400">Setup Bias</span>
            <span className="font-bold text-white uppercase">{track.layoutType}</span>
          </div>
          <div className="flex justify-between border-b border-neutral-800/50 pb-1">
            <span className="text-neutral-400">Pit Stop Delta</span>
            <span className="font-bold text-white">{track.pitStopDelta}s</span>
          </div>
          <div className="flex justify-between pb-1">
            <span className="text-neutral-400">DRS Zones</span>
            <span className="font-bold text-white">{track.drsZones}</span>
          </div>
        </div>
      </SectionCard>

      {/* Performance: Telemetry (Long Run Pace) */}
      <SectionCard title="Telemetry">
        <ScrollWrapper minWidth="min-w-[500px]">
          <table className="w-full text-left font-mono text-sm">
            <thead>
              <tr className="border-b border-neutral-800 text-xs uppercase text-neutral-400">
                <th className="pb-2 font-medium">Driver</th>
                <th className="pb-2 font-medium text-center">Compound</th>
                <th className="pb-2 font-medium text-right">Avg Lap</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-neutral-800/40">
              {telemetry.longRunPace.map((run, index) => (
                <tr key={run.driverName + index} className="hover:bg-neutral-900/40">
                  <td className="py-2.5 font-bold text-white">{run.driverName}</td>
                  <td className="py-2.5 text-center">
                    <span className={`inline-block rounded px-2 py-0.5 text-xs font-black uppercase border ${getTireStyles(run.tireCompound)}`}>
                        {run.tireCompound}
                    </span>
                  </td>
                  <td className="py-2.5 text-right font-bold text-neutral-200">{run.avgLapTime}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </ScrollWrapper>
      </SectionCard>

{/* Machine Learning Predictions - Spans full width of the grid */}
      <div className="col-span-1 md:col-span-2 lg:col-span-3">
        <SectionCard title="Random Forest Race Predictor">
          {isLoadingPredictions ? (
            <div className="flex h-32 items-center justify-center text-neutral-500 font-mono">
              Processing Telemetry...
            </div>
          ) : predictions.length > 0 ? (
            <ScrollWrapper minWidth="min-w-[700px]">
              <table className="w-full text-left font-mono text-sm">
                <thead>
                  <tr className="border-b border-neutral-800 text-xs uppercase text-neutral-400">
                    <th className="pb-3 font-medium pl-2">Pos</th>
                    <th className="pb-3 font-medium">Driver</th>
                    <th className="pb-3 font-medium text-right">Win Probability</th>
                    <th className="pb-3 font-medium text-right sm:table-cell">Track Mastery</th>
                    <th className="pb-3 font-medium text-right md:table-cell">Driver Form</th>
                    <th className="pb-3 font-medium text-right md:table-cell pr-2">Car Momentum</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-neutral-800/40">
                  {predictions.slice(0, 10).map((pred) => (
                    <tr key={pred.driverId} className="hover:bg-neutral-900/40 transition-colors">
                      <td className="py-3 pl-2">
                        <span className="text-neutral-500 font-bold">P{pred.predictedPosition}</span>
                      </td>
                      <td className="py-3 font-bold text-white uppercase">{pred.driverName}</td>
                      <td className="py-3 text-right">
                        <span className="text-lg font-black text-emerald-400">
                          {(pred.winProbability * 100).toFixed(1)}%
                        </span>
                      </td>
                      <td className="py-3 text-right sm:table-cell text-sky-400">
                        {pred.insights?.trackMastery ? pred.insights.trackMastery.toFixed(1) : "N/A"}
                      </td>
                      <td className="py-3 text-right md:table-cell text-neutral-300">
                        {pred.insights?.driverMomentum ? pred.insights.driverMomentum.toFixed(1) : "N/A"}
                      </td>
                      <td className="py-3 text-right md:table-cell text-neutral-300 pr-2">
                        {pred.insights?.teamMomentum ? pred.insights.teamMomentum.toFixed(1) : "N/A"}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </ScrollWrapper>
          ) : (
            <div className="flex h-32 items-center justify-center text-neutral-500 font-mono">
              No predictions available
            </div>
          )}
        </SectionCard>
      </div>
    </main>
  </div>
  );
}
