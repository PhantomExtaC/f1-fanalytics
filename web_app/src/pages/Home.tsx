import StatCard from "../components/cards/StatCard";
import SectionCard from "../components/cards/SectionCard";
import { useEffect, useState } from "react";
import StandingsTable from "../components/cards/StandingsTable";
import { getDriverStandings, getConstructorStandings } from "../services/standings";
import type { DriverStanding, ConstructorStanding } from "../types/standings";

export default function Home() {
  const [driverStandings, setDriverStandings] = useState<DriverStanding[]>([]);
  const [constructorStandings, setConstructorStandings] = useState<ConstructorStanding[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Fetch both standalone JSON files in parallel
    Promise.all([getDriverStandings(), getConstructorStandings()])
      .then(([driversData, constructorsData]) => {
        setDriverStandings(driversData);
        setConstructorStandings(constructorsData);
      })
      .catch((err) => console.error("Error loading standings data:", err))
      .finally(() => setIsLoading(false));
  }, []);

  if (isLoading) {
    return <div className="p-8 text-center text-white">Loading Standings...</div>;
  }

  // Map the flat pipeline data format directly to the rows format expected by StandingsTable
  const driverRows = driverStandings.map((entry) => ({
    position: entry.position,
    name: entry.driverName,
    points: entry.points,
    wins: entry.wins,
  }));

  const constructorRows = constructorStandings.map((entry) => ({
    position: entry.position,
    name: entry.teamName,
    points: entry.points,
    wins: entry.wins, 
  }));

  return (
    <div className="mx-auto max-w-7xl p-8 space-y-8">
      {/* Hero */}
      <section className="rounded-xl bg-gradient-to-r from-red-700 to-black p-8 text-white">
        <h1 className="text-5xl font-bold">Fanalytics</h1>
        <p className="mt-4 max-w-3xl text-lg">
          Formula 1 analytics platform with standings, statistics, race insights and prediction models.
        </p>
      </section>

      {/* Stats */}
      <section className="grid grid-cols-2 gap-4 lg:grid-cols-4">
        <StatCard title="Drivers" value={20} />
        <StatCard title="Teams" value={10} />
        <StatCard title="Circuits" value={24} />
        <StatCard title="Season" value="2026" />
      </section>

      {/* Main grid - Fixed the layout to properly use grid columns */}
      <section className="space-y-6 text-white">
        <h1 className="text-4xl font-bold">Championship Standings</h1>
        <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
          <StandingsTable
            title="Driver Championship"
            rows={driverRows}
          />
          <StandingsTable
            title="Constructor Championship"
            rows={constructorRows}
          />
        </div>
      </section>

      <SectionCard title="Championship Progression">
        <div className="flex h-64 items-center justify-center rounded-lg border border-dashed border-slate-600 text-white">
          Chart placeholder
        </div>
      </SectionCard>

      <section className="grid grid-cols-1 gap-6 lg:grid-cols-2 text-white">
        <SectionCard title="Next Grand Prix">
          <p>Will load from next_race.json</p>
        </SectionCard>
        <SectionCard title="Prediction Preview">
          <p>Will load from predictions.json</p>
        </SectionCard>
      </section>
    </div>
  );
}