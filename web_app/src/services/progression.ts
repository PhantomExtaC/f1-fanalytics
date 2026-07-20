import type { PointsProgression } from "../types/progression";
import { fetchJson } from "./fetchJson"; // Assumes you have this utility already

export function getPointsProgression(): Promise<PointsProgression[]> {
  return fetchJson<PointsProgression[]>("/data/pointsProgression.json");
}