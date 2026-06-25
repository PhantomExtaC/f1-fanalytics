export interface Track {
  id: string;

  name: string;

  country: string;
  city: string;

  lengthKm: number;

  corners: number;

  laps: number;

  drsZones: number;

  lapRecord: string;

  active: boolean;

  layout: string;
}