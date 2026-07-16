export interface LapRecord {
  time: string;
  driver: string;
  year: string | number;
  milliseconds: number;
}

export interface Track {
  id: string;
  name: string;
  country: string;
  city: string;
  lengthKm: number;
  corners: number;
  firstGrandPrix: string;
  lastGrandPrix: string;
  laps: number;
  drsZones: number;
  // ✅ Changed from string to our new object type (and allow null just in case)
  lapRecord: LapRecord | null; 
  active: boolean;
  layout: string;
}