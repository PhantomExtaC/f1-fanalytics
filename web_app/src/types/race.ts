export interface Race {
  round: number;

  grandPrix: string;

  trackId: string;

  country: string;

  date: string;

  sprintWeekend: boolean;

  status: "upcoming" | "in_progress" | "completed" | "cancelled";
}