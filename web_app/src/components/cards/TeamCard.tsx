import type { Team } from "../../types/team";
import type { Driver } from "../../types/driver";

interface TeamCardProps {
  team: Team;
  drivers: Driver[];
}

export default function TeamCard({
  team,
  drivers,
}: TeamCardProps) {
  return (
    <div className="rounded-xl border border-slate-700 bg-slate-900 p-5 shadow-lg">
      <img
        src={team.logo}
        alt={team.name}
        className="mx-auto h-28 object-contain"
      />

      <h2 className="mt-4 text-center text-2xl font-bold">
        {team.name}
      </h2>

      <p className="text-center text-slate-400">
        {team.principal}
      </p>

      <div className="mt-4">
        <p className="font-semibold">Drivers</p>

        <ul className="list-inside list-disc text-sm text-slate-300">
          {drivers.map((driver) => (
            <li key={driver.id}>{driver.fullName}</li>
          ))}
        </ul>
      </div>

      <div className="mt-4 grid grid-cols-2 gap-2 text-sm">
        <div>Wins: {team.wins}</div>
        <div>Podiums: {team.podiums}</div>
        <div>Titles: {team.championships}</div>
        <div>Points: {team.points}</div>
      </div>
    </div>
  );
}