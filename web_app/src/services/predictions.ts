import type { Prediction } from "../types/prediction";
import { fetchJson } from "./fetchJson";

export function getPredictions(): Promise<Prediction[]> {
  return fetchJson<Prediction[]>("/data/predictions.json");
}