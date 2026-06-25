export interface PredictionEntry {
  driverId: string;

  probability: number;
}

export interface Predictions {
  generatedAt: string;

  winner: PredictionEntry;

  podium: PredictionEntry[];
}