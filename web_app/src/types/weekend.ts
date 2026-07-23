export interface WeatherData {
  airTemp: number;
  trackTemp: number;
  rainProbability: number;
  condition: string; // e.g., "Overcast", "Sunny"
}

export interface TrackData {
  circuitName: string;
  layoutType: string; // e.g., "High Speed", "Street"
  pitStopDelta: number; // Time lost in pit lane
  drsZones: number;
}

export interface LongRunPace {
  driverId: string;
  driverName: string;
  avgLapTime: string; // e.g., "1:35.4"
  tireCompound: string; // "Soft", "Medium", "Hard"
}

export interface WeekendState {
  track: TrackData;
  weather: WeatherData;
  telemetry: {
    fastestSectors: {
      sector1: string; // Driver Name
      sector2: string;
      sector3: string;
    };
    longRunPace: LongRunPace[];
  };
}