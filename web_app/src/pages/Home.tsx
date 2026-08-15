import { useEffect, useState } from "react";


import StatCard from "../components/cards/StatCard";
import SectionCard from "../components/cards/SectionCard";

import StandingsTable from "../components/cards/StandingsTable";
import { getDriverStandings, getConstructorStandings } from "../services/standings";
import type { DriverStanding, ConstructorStanding } from "../types/standings";

import { PointsProgressChart } from '../components/charts/PointsProgressChart';
import { getPointsProgression } from '../services/progression';
import type { PointsProgression } from '../types/progression';

import { getCalendar } from '../services/calendar';
import type { RaceEvent } from '../types/calendar';
import { getPredictions } from '../services/predictions';
import type { Prediction } from '../types/prediction';

export default function Home() {
  const [driverStandings, setDriverStandings] = useState<DriverStanding[]>([]);
  const [constructorStandings, setConstructorStandings] = useState<ConstructorStanding[]>([]);
  const [isLoadingStandings, setIsLoadingStandings] = useState(true);
  
  const [progressionData, setProgressionData] = useState<PointsProgression[]>([]);
  const [isLoadingProgression, setIsLoadingProgression] = useState<boolean>(true);

  const [nextRace, setNextRace] = useState<RaceEvent | null>(null);
  const [isLoadingNextRace, setIsLoadingNextRace] = useState(true);

  const [predictions, setPredictions] = useState<Prediction[]>([]);
  const [isLoadingPredictions, setIsLoadingPredictions] = useState(true);

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

  

  useEffect(() => {
    getCalendar()
      .then((data) => {
        // Automatically find the very next race on the schedule
        const upcoming = data.find(race => race.status === "upcoming" || race.status === "in_progress");
        setNextRace(upcoming || null);
      })
      .catch((err) => console.error("Error loading calendar:", err))
      .finally(() => setIsLoadingNextRace(false));
  }, []);

  useEffect(() => {
    getPredictions()
      .then((data) => setPredictions(data))
      .catch((err) => console.error("Error loading predictions:", err))
      .finally(() => setIsLoadingPredictions(false));
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
      <section className="rounded-xl bg-linear-to-r from-red-700 to-black p-8 text-white">
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

      {/* Bottom Section */}
      <section className="grid grid-cols-1 gap-6 text-white lg:grid-cols-2">
        <SectionCard title="Next Grand Prix">
          {isLoadingNextRace ? (
            <div className="flex h-32 items-center justify-center text-slate-400">Loading Calendar...</div>
          ) : nextRace ? (
            <div className="flex h-full flex-col justify-center space-y-2">
              <span className="text-sm font-bold uppercase tracking-wider text-red-500">
                Round {nextRace.round} {nextRace.sprintWeekend && "• Sprint Weekend"}
              </span>
              <span className="text-3xl font-bold">{nextRace.grandPrix}</span>
              <span className="text-lg text-slate-300">
                {new Date(nextRace.date).toLocaleDateString('en-US', { weekday: 'long', month: 'long', day: 'numeric' })}
              </span>
              {nextRace.status === "in_progress" && (
                <span className="mt-2 w-max rounded bg-green-600 px-3 py-1 text-xs font-bold uppercase tracking-widest text-white shadow-[0_0_10px_rgba(22,163,74,0.5)]">
                  Live This Weekend
                </span>
              )}
            </div>
          ) : (
            <div className="flex h-32 items-center justify-center text-slate-400">Season Completed</div>
          )}
        </SectionCard>

        <SectionCard title="Prediction Preview">
          {isLoadingPredictions ? (
            <div className="flex h-32 items-center justify-center text-slate-400">Running Models...</div>
          ) : predictions.length > 0 ? (
            <div className="space-y-4 pt-2">
              {predictions.slice(0, 3).map((pred) => (
                <div key={pred.driverId} className="flex items-center justify-between border-b border-slate-700/50 pb-3 last:border-0">
                  <div className="flex items-center gap-4">
                    <span className="text-xl font-bold text-slate-500">P{pred.predictedPosition}</span>
                    <span className="text-lg font-medium">{pred.driverName}</span>
                  </div>
                  <span className="font-mono text-lg font-bold text-emerald-400">
                    {(pred.winProbability * 100).toFixed(0)}%
                  </span>
                </div>
              ))}
            </div>
          ) : (
            <div className="flex h-32 items-center justify-center text-slate-400">No predictions available</div>
          )}
        </SectionCard>
      </section>
    </div>
  );
}