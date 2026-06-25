import type { Track } from "../types/track";
import { fetchJson } from "./fetchJson";

export async function getTracks(): Promise<Track[]> {
  return fetchJson<Track[]>("/data/tracks.json");
}