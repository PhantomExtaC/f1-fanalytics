import { useEffect, useState } from "react";
import { fetchJson } from "../services/fetchJson";
import SectionCard from "../components/cards/SectionCard"; 
import type { WeekendState } from "../types/weekend";

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

  useEffect(() => {
    fetchJson("/data/weekend_state.json")
      .then((data) => setWeekendData(data as WeekendState))
      .catch((err) => console.error("Error loading weekend state:", err))
      .finally(() => setIsLoading(false));
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
      <h1 className="font-mono text-4xl font-black uppercase tracking-tight text-white">
        {track.circuitName}
      </h1>
      <p className="text-sm font-semibold uppercase tracking-widest text-red-500">
        Live Race Weekend Hub
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
        <div className="overflow-x-auto">
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
                  {/* Updated Dynamic Tire Compound Badge */}
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
        </div>
      </SectionCard>

    </main>
  </div>
);

}
