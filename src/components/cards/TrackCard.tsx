import type { Track } from "../../types/track";

interface TrackCardProps {
  track: Track;
}

export default function TrackCard({ track }: TrackCardProps) {
  return (
    <div className="rounded-xl border border-slate-700 bg-slate-900 p-5 shadow-lg">
      <img
        src={track.layout}
        alt={track.name}
        className="h-48 w-full object-contain"
      />

      <h2 className="mt-4 text-2xl font-bold text-white">
        {track.name}
      </h2>

      <p className="text-slate-400">
        {track.country}, {track.city}
      </p>

      <div className="mt-4 grid grid-cols-2 gap-y-2 gap-x-4 text-sm text-slate-300">
        <div><span className="font-semibold text-white">Length:</span> {track.lengthKm} km</div>
        
        {/* ✅ Safely accessing the object properties */}
        <div className="col-span-2">
          <span className="font-semibold text-white">Track Record:</span>{" "}
          {track.lapRecord ? (
            `${track.lapRecord.time} (${track.lapRecord.driver}, ${track.lapRecord.year})`
          ) : (
            "N/A"
          )}
        </div>
        
        <div><span className="font-semibold text-white">First GP:</span> {track.firstGrandPrix}</div>
        <div><span className="font-semibold text-white">Last GP:</span> {track.lastGrandPrix}</div>
        
      </div>
    </div>
  );
}