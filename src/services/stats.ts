import type { Stats } from "../types/stats";
import { fetchJson } from "./fetchJson";

export async function getStats(): Promise<Stats> {
  return fetchJson<Stats>("/data/stats.json");
}