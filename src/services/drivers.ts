import type { Driver } from "../types/driver";
import { fetchJson } from "./fetchJson";

export function getDrivers(): Promise<Driver[]> {
  return fetchJson<Driver[]>("/data/drivers.json");
}