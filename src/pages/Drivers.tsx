import { useEffect, useState, useMemo } from "react";

import DriverCard from "../components/cards/DriverCard";

import { getDrivers } from "../services/drivers";
import { getTeams } from "../services/teams";

import type { Driver } from "../types/driver";
import type { Team } from "../types/team";


export default function Drivers() {
  const [drivers, setDrivers] = useState<Driver[]>([]);
  const [teams, setTeams] = useState<Team[]>([]);
  const [showActiveOnly, setShowActiveOnly] = useState(false);
const [sortBy, setSortBy] = useState("alphabetical");
  useEffect(() => {
    getDrivers().then(setDrivers);
    getTeams().then(setTeams);
  }, []);

  const displayedDrivers = useMemo(() => {
  let filtered = [...drivers];

  // Filter
  if (showActiveOnly) {
    filtered = filtered.filter(driver => driver.active);
  }

  // Sort
  switch (sortBy) {
    case "alphabetical":
      filtered.sort((a, b) =>
        a.fullName.localeCompare(b.fullName)
      );
      break;

    case "winsAsc":
      filtered.sort((a, b) => a.wins - b.wins);
      break;

    case "winsDesc":
      filtered.sort((a, b) => b.wins - a.wins);
      break;

    default:
      break;
  }

  return filtered;
}, [drivers, showActiveOnly, sortBy]);

  return (
    <div className="mx-auto max-w-7xl p-8">
      <h1 className="mb-8 text-4xl font-bold">
        Drivers
      </h1>
      <div className="mb-6 flex flex-wrap gap-4">

  <label className="flex items-center gap-2">
    <input
      type="checkbox"
      checked={showActiveOnly}
      onChange={(e) => setShowActiveOnly(e.target.checked)}
    />
    Active Only
  </label>

  <select
    value={sortBy}
    onChange={(e) => setSortBy(e.target.value)}
    className="rounded border border-slate-600 bg-slate-800 p-2"
  >
    <option value="alphabetical">
      Alphabetical (A-Z)
    </option>

    <option value="winsAsc">
      Race Wins (Ascending)
    </option>

    <option value="winsDesc">
      Race Wins (Descending)
    </option>
  </select>

</div>
      <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
        {displayedDrivers.map((driver) => {
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