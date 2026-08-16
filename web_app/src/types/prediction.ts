export interface Prediction {
  driverId: string;
  driverName: string;
  winProbability: number;
  predictedPosition: number;
  insights?: {
    trackMastery: number;
    teamMomentum: number;
    driverMomentum: number;
  };
}