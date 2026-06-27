import type { DriverStanding, ConstructorStanding } from "../types/standings";

export async function getDriverStandings(): Promise<DriverStanding[]> {
  const res = await fetch("/data/driver_standings.json");
  if (!res.ok) throw new Error("Failed to fetch driver standings");
  return res.json();
}

export async function getConstructorStandings(): Promise<ConstructorStanding[]> {
  const res = await fetch("/data/constructor_standings.json");
  if (!res.ok) throw new Error("Failed to fetch constructor standings");
  return res.json();
}