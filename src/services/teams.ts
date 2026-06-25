import type { Team } from "../types/team";
import { fetchJson } from "./fetchJson";

export async function getTeams(): Promise<Team[]> {
  return fetchJson<Team[]>("/data/teams.json");
}