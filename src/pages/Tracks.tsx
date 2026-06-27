import { useEffect, useState, useMemo } from "react";

import TrackCard from "../components/cards/TrackCard";

import { getTracks } from "../services/tracks";

import type { Track } from "../types/track";

export default function Tracks() {
  const [tracks, setTracks] = useState<Track[]>([]);
  const [sortBy, setSortBy] = useState("alphabetical");

  useEffect(() => {
    getTracks().then(setTracks);
  }, []);

  const sortedTracks = useMemo(() => {
    let updatedTracks = [...tracks];

    return updatedTracks.sort((a, b) => {
      if (sortBy === "alphabetical") {
        // Safe string comparison fallback
        const nameA = a.name || "";
        const nameB = b.name || "";
        return nameA.localeCompare(nameB);
      }

      if (sortBy === "lengthAsc" || sortBy === "lengthDesc") {
        // Safely convert to string first to handle both nulls and numbers, then parse
        const lengthA = parseFloat(String(a.lengthKm || "0")) || 0;
        const lengthB = parseFloat(String(b.lengthKm || "0")) || 0;
        
        return sortBy === "lengthAsc" ? lengthA - lengthB : lengthB - lengthA;
      }

      if (sortBy === "recency") {
        // Only call substring if lastGrandPrix is a valid string
        const yearA = typeof a.lastGrandPrix === "string" 
          ? parseInt(a.lastGrandPrix.substring(0, 4), 10) 
          : 0;
          
        const yearB = typeof b.lastGrandPrix === "string" 
          ? parseInt(b.lastGrandPrix.substring(0, 4), 10) 
          : 0;
        
        return yearB - yearA;
      }

      return 0;
    });
  }, [tracks, sortBy]);

  return (
    <div className="mx-auto max-w-7xl p-8 text-white">
      <h1 className="mb-8 text-4xl font-bold">Tracks</h1>

      <div className="mb-6 flex flex-wrap gap-4 items-center">
        <select
          value={sortBy}
          onChange={(e) => setSortBy(e.target.value)}
          className="rounded border border-slate-600 bg-slate-800 p-2 text-white outline-none focus:border-red-500"
        >
          <option value="alphabetical">Alphabetical (A-Z)</option>
          <option value="lengthAsc">Track Length (Shortest to Longest)</option>
          <option value="lengthDesc">Track Length (Longest to Shortest)</option>
          <option value="recency">Recency (Most Recent First)</option>
        </select>
      </div>

      <div className="grid gap-6 md:grid-cols-2 xl:grid-cols-3">
        {sortedTracks.map((track) => (
          <TrackCard
            key={track.id}
            track={track}
          />
        ))}
      </div>
    </div>
  );
}