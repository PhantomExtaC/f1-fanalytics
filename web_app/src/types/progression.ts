export interface PointsProgression {
  round: number;
  // This tells TypeScript: "There will be other string keys (driver abbreviations) containing number values"
  [driverId: string]: number;
}