import type { Race } from "../types/race";
import { fetchJson } from "./fetchJson";

export async function getCalendar(): Promise<Race[]> {
  return fetchJson<Race[]>("/data/calendar.json");
}