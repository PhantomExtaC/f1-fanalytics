import { useEffect, useState } from "react";


import StatCard from "../components/cards/StatCard";
import SectionCard from "../components/cards/SectionCard";

import StandingsTable from "../components/cards/StandingsTable";
import { getDriverStandings, getConstructorStandings } from "../services/standings";
import type { DriverStanding, ConstructorStanding } from "../types/standings";

import { PointsProgressChart } from '../components/charts/PointsProgressChart';
import { getPointsProgression } from '../services/progression';
import type { PointsProgression } from '../types/progression';


export default function Home() {
  const [driverStandings, setDriverStandings] = useState<DriverStanding[]>([]);
  const [constructorStandings, setConstructorStandings] = useState<ConstructorStanding[]>([]);
  const [isLoadingStandings, setIsLoadingStandings] = useState(true);
  
  const [progressionData, setProgressionData] = useState<PointsProgression[]>([]);
  const [isLoadingProgression, setIsLoadingProgression] = useState<boolean>(true);
  // Fetch driver and constructor standings on component mount
  useEffect(() => {
    // Fetch both standalone JSON files in parallel
    Promise.all([getDriverStandings(), getConstructorStandings()])
      .then(([driversData, constructorsData]) => {
        setDriverStandings(driversData);
        setConstructorStandings(constructorsData);
      })
      .catch((err) => console.error("Error loading standings data:", err))
      .finally(() => setIsLoadingStandings(false));
  }, []);
//driver season progression
  useEffect(() => {
    // Fetch data using your strongly-typed service
    getPointsProgression()
      .then((data) => {
        setProgressionData(data);
      })
      .catch((error) => console.error("Failed to load points progression:", error))
      .finally(() => setIsLoadingProgression(false));
  }, []);

  if (isLoadingStandings) {
    return <div className="p-8 text-center text-white">Loading LapLogic Dashboard...</div>;
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
        <h1 className="text-5xl font-bold">LapLogic</h1>
        <p className="mt-4 max-w-3xl text-lg">
          Formula 1 analytics platform with standings, statistics, race insights and prediction models.
        </p>
      </section>

      {/* Stats */}
      <section className="grid grid-cols-2 gap-4 lg:grid-cols-4">
        <StatCard title="Drivers" value={22} />
        <StatCard title="Teams" value={11} />
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

      {/* Progression Chart */}
      <SectionCard title="Championship Progression">
        {isLoadingProgression ? (
          <div className="flex h-64 items-center justify-center rounded-lg border border-dashed border-slate-600 text-slate-400">
            Loading Championship Data...
          </div>
        ) : (
          <PointsProgressChart data={progressionData} />
        )}
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