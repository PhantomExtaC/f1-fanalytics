import { useEffect, useState } from "react";

import TrackCard from "../components/cards/TrackCard";

import { getTracks } from "../services/tracks";

import type { Track } from "../types/track";

export default function Tracks() {
  const [tracks, setTracks] = useState<Track[]>([]);

  useEffect(() => {
    getTracks().then(setTracks);
  }, []);

  return (
    <div className="mx-auto max-w-7xl p-8">
      <h1 className="mb-8 text-4xl font-bold">
        Tracks
      </h1>

      <div className="grid gap-6 md:grid-cols-2 xl:grid-cols-3">
        {tracks.map((track) => (
          <TrackCard
            key={track.id}
            track={track}
          />
        ))}
      </div>
    </div>
  );
}