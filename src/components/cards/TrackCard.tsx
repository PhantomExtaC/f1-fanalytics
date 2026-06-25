import type { Track } from "../../types/track";

interface TrackCardProps {
  track: Track;
}

export default function TrackCard({
  track,
}: TrackCardProps) {
  return (
    <div className="rounded-xl border border-slate-700 bg-slate-900 p-5 shadow-lg">
      <img
        src={track.layout}
        alt={track.name}
        className="h-48 w-full object-contain"
      />

      <h2 className="mt-4 text-2xl font-bold">
        {track.name}
      </h2>

      <p className="text-slate-400">
        {track.country}
      </p>

      <div className="mt-4 grid grid-cols-2 gap-2 text-sm">
        <div>Length: {track.lengthKm} km</div>
        <div>Corners: {track.corners}</div>
        <div>Laps: {track.laps}</div>
        <div>DRS Zones: {track.drsZones}</div>
      </div>
    </div>
  );
}