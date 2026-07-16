import type { Weather } from "./weather";

export interface NextRace {
  round: number;

  grandPrix: string;

  trackId: string;

  country: string;

  date: string;

  weather: Weather;
}