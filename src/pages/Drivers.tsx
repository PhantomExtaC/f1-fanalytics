import { useEffect, useState } from "react";

import DriverCard from "../components/cards/DriverCard";

import { getDrivers } from "../services/drivers";
import { getTeams } from "../services/teams";

import type { Driver } from "../types/driver";
import type { Team } from "../types/team";

export default function Drivers() {
  const [drivers, setDrivers] = useState<Driver[]>([]);
  const [teams, setTeams] = useState<Team[]>([]);

  useEffect(() => {
    getDrivers().then(setDrivers);
    getTeams().then(setTeams);
  }, []);

  return (
    <div className="mx-auto max-w-7xl p-8">
      <h1 className="mb-8 text-4xl font-bold">
        Drivers
      </h1>

      <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
        {drivers.map((driver) => {
          const team = teams.find(
            (t) => t.id === driver.currentTeamId
          );

          return (
            <DriverCard
              key={driver.id}
              driver={driver}
              teamName={team?.name ?? "Unknown Team"}
            />
          );
        })}
      </div>
    </div>
  );
}