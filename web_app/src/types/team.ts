export interface Team {
  id: string;

  name: string;

  principal: string;

  base: string;

  engine: string;

  driverIds: string[];

  wins: number;
  podiums: number;
  championships: number;

  points: number;

  active: boolean;

  logo: string;
}