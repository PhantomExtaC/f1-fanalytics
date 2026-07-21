export interface RaceEvent {
  round: number;
  grandPrix: string;
  date: string;
  sprintWeekend: boolean;
  status: "completed" | "in_progress" | "upcoming";
}