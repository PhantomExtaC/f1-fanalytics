import type { RaceEvent } from "../types/calendar";
import { fetchJson } from "./fetchJson";

export function getCalendar(): Promise<RaceEvent[]> {
  return fetchJson<RaceEvent[]>("/data/calendar.json");
}