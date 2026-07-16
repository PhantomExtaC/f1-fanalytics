import { useState } from "react";

export default function Simulator() {
  const [driver, setDriver] = useState("");
  const [track, setTrack] = useState("");
  const [weather, setWeather] = useState("");

  return (
    <div className="mx-auto max-w-4xl p-8">
      <h1 className="mb-8 text-4xl font-bold">
        Race Simulator
      </h1>

      <div className="space-y-4">
        <input
          className="w-full rounded border p-2"
          placeholder="Driver"
          value={driver}
          onChange={(e) => setDriver(e.target.value)}
        />

        <input
          className="w-full rounded border p-2"
          placeholder="Track"
          value={track}
          onChange={(e) => setTrack(e.target.value)}
        />

        <input
          className="w-full rounded border p-2"
          placeholder="Weather"
          value={weather}
          onChange={(e) => setWeather(e.target.value)}
        />

        <button className="rounded bg-red-600 px-4 py-2">
          Simulate
        </button>
      </div>
    </div>
  );
}