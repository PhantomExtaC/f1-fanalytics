import { useEffect, useState } from "react";

import StandingsTable from "../components/cards/StandingsTable";

import { getStandings } from "../services/standings";
import { getDrivers } from "../services/drivers";
import { getTeams } from "../services/teams";
import type { Team } from "../types/team";
import type { Standings as StandingsType } from "../types/standings";
import type { Driver } from "../types/driver";

export default function Standings() {
  const [standings, setStandings] =
    useState<StandingsType | null>(null);

  const [drivers, setDrivers] =
    useState<Driver[]>([]);

  useEffect(() => {
    getStandings().then(setStandings);
    getDrivers().then(setDrivers);
  }, []);

  const [teams, setTeams] = useState<Team[]>([]);

  useEffect(() => {
    getStandings().then(setStandings);
    getDrivers().then(setDrivers);
    getTeams().then(setTeams);
  }, []);

  if (!standings) {
    return <div className="p-8">Loading...</div>;
  }

  const driverRows = standings.drivers.map((entry) => {
  const driver = drivers.find(
    (d) => d.id === entry.driverId
  );

  return {
    position: entry.position,
    name: driver?.fullName ?? "Unknown",
    points: entry.points,
    wins: entry.wins,
  };
});

const constructorRows = standings.constructors.map((entry) => {
  const team = teams.find(
    (t) => t.id === entry.teamId
  );

  return {
    position: entry.position,
    name: team?.name ?? "Unknown",
    points: entry.points,
  };
});

  return (
  <div className="mx-auto max-w-7xl space-y-8 p-8">
    <h1 className="text-4xl font-bold">
      Championship Standings
    </h1>

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