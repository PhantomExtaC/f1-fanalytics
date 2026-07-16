import type { Driver } from "../../types/driver";

interface DriverCardProps {
  driver: Driver;
  teamName: string;
}

export default function DriverCard({
  driver,
  teamName,
}: DriverCardProps) {
  return (
    <div className="overflow-hidden rounded-xl border border-slate-700 bg-slate-900 shadow-lg transition hover:border-red-600">
      <img
        src={driver.image}
        alt={driver.fullName}
        className="h-64 w-full object-cover"
      />

      <div className="p-5">
        <div className="flex items-center justify-between">
          <h2 className="text-xl font-bold">{driver.fullName}</h2>

          <span className="rounded bg-red-600 px-2 py-1 text-sm font-semibold">
            #{driver.number}
          </span>
        </div>

        <p className="mt-1 text-slate-400">{teamName}</p>

        <div className="mt-5 grid grid-cols-2 gap-3 text-sm">
          <div>
            <p className="text-slate-500">Wins</p>
            <p>{driver.wins}</p>
          </div>

          <div>
            <p className="text-slate-500">Podiums</p>
            <p>{driver.podiums}</p>
          </div>

          <div>
            <p className="text-slate-500">Starts</p>
            <p>{driver.raceStarts}</p>
          </div>

          <div>
            <p className="text-slate-500">Points</p>
            <p>{driver.currentPoints}</p>
          </div>
        </div>
      </div>
    </div>
  );
}