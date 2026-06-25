import type { Predictions } from "../types/prediction";
import { fetchJson } from "./fetchJson";

export async function getPredictions(): Promise<Predictions> {
  return fetchJson<Predictions>("/data/predictions.json");
}