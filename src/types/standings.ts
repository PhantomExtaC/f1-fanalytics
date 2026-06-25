export interface DriverStanding {
  position: number;

  driverId: string;

  points: number;

  wins: number;
}

export interface ConstructorStanding {
  position: number;

  teamId: string;

  points: number;
}

export interface Standings {
  drivers: DriverStanding[];

  constructors: ConstructorStanding[];
}