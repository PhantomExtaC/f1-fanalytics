import { useEffect, useState } from "react";

import TeamCard from "../components/cards/TeamCard";

import { getTeams } from "../services/teams";
import { getDrivers } from "../services/drivers";

import type { Team } from "../types/team";
import type { Driver } from "../types/driver";

export default function Teams() {
  const [teams, setTeams] = useState<Team[]>([]);
  const [drivers, setDrivers] = useState<Driver[]>([]);

  useEffect(() => {
    getTeams().then(setTeams);
    getDrivers().then(setDrivers);
  }, []);

  return (
    <div className="mx-auto max-w-7xl p-8">
      <h1 className="mb-8 text-4xl font-bold">
        Teams
      </h1>

      <div className="grid gap-6 md:grid-cols-2 xl:grid-cols-3">
        {teams.map((team) => {
          const teamDrivers = drivers.filter((driver) =>
            team.driverIds.includes(driver.id)
          );

          return (
            <TeamCard
              key={team.id}
              team={team}
              drivers={teamDrivers}
            />
          );
        })}
      </div>
    </div>
  );
}