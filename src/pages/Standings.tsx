import { useEffect, useState } from "react";

import StandingsTable from "../components/cards/StandingsTable";

import { getDriverStandings, getConstructorStandings } from "../services/standings";
import type { DriverStanding, ConstructorStanding } from "../types/standings";

export default function Standings() {
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
    wins: entry.wins, // Added wins here since the pipeline provides it!
  }));

  return (
    <div className="mx-auto max-w-7xl space-y-8 p-8 text-white">
      <h1 className="text-4xl font-bold">Championship Standings</h1>

      <StandingsTable
        title="Driver Championship"
        rows={driverRows}
      />

      <StandingsTable
        title="Constructor Championship"
        rows={constructorRows}
      />
    </div>
  );
}