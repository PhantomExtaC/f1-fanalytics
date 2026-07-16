import { useEffect, useState, useMemo } from "react";

import TeamCard from "../components/cards/TeamCard";

import { getTeams } from "../services/teams";
import { getDrivers } from "../services/drivers";

import type { Team } from "../types/team";
import type { Driver } from "../types/driver";

export default function Teams() {
  const [teams, setTeams] = useState<Team[]>([]);
  const [drivers, setDrivers] = useState<Driver[]>([]);
  const [showActiveOnly, setShowActiveOnly] = useState(false);
  const [sortBy, setSortBy] = useState("alphabetical");

  useEffect(() => {
    getTeams().then(setTeams);
    getDrivers().then(setDrivers);
  }, []);

  const sortedTeams = useMemo(() => {
    // ✅ Create a shallow copy to prevent direct state mutation
    let filteredTeams = [...teams];

    // Filter
    if (showActiveOnly) {
      filteredTeams = filteredTeams.filter((team) => team.active);
    }

    // Sort
    return filteredTeams.sort((a, b) => {
      if (sortBy === "alphabetical") {
        return a.name.localeCompare(b.name);
      }
      if (sortBy === "wins") {
        // Sort from highest wins to lowest wins
        return b.wins - a.wins;
      }
      return 0;
    });
  }, [teams, showActiveOnly, sortBy]);

  return (
    <div className="mx-auto max-w-7xl p-8 text-white">
      <h1 className="mb-8 text-4xl font-bold">Teams</h1>

      {/* ✅ Filtering and Sorting UI Layer */}
      <div className="mb-6 flex flex-wrap gap-4 items-center">
        <label className="flex items-center gap-2 cursor-pointer select-none">
          <input
            type="checkbox"
            checked={showActiveOnly}
            onChange={(e) => setShowActiveOnly(e.target.checked)}
            className="rounded border-slate-600 bg-slate-800 accent-red-500 h-4 w-4"
          />
          <span>Active Only</span>
        </label>

        <select
          value={sortBy}
          onChange={(e) => setSortBy(e.target.value)}
          className="rounded border border-slate-600 bg-slate-800 p-2 text-white outline-none focus:border-red-500"
        >
          <option value="alphabetical">Alphabetical (A-Z)</option>
          <option value="wins">Most Race Wins</option>
        </select>
      </div>

      {/* Grid Layout for Cards */}
      <div className="grid gap-6 md:grid-cols-2 xl:grid-cols-3">
        {sortedTeams.map((team) => {
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