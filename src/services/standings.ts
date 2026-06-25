import type { Standings } from "../types/standings";
import { fetchJson } from "./fetchJson";

export async function getStandings(): Promise<Standings> {
  return fetchJson<Standings>("/data/standings.json");
}