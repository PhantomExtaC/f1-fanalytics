import type { NextRace } from "../types/nextRace";
import { fetchJson } from "./fetchJson";

export async function getNextRace(): Promise<NextRace> {
  return fetchJson<NextRace>("/data/next_race.json");
}