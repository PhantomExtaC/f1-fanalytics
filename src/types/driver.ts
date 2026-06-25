export interface Driver {
  id: string;

  fullName: string;
  abbreviation: string;

  number: number;

  nationality: string;
  dateOfBirth: string;
  age: number;

  currentTeamId: string;

  active: boolean;

  raceStarts: number;
  raceFinishes: number;
  dnfs: number;

  wins: number;
  podiums: number;
  poles: number;
  fastestLaps: number;

  championships: number;

  currentPoints: number;

  image: string;
}