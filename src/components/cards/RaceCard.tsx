interface RaceCardProps {
  grandPrix: string;
  date: string;
  country: string;
  weather: string;
}

export default function RaceCard({
  grandPrix,
  date,
  country,
  weather,
}: RaceCardProps) {
  return (
    <div className="rounded-xl border border-slate-700 bg-slate-900 p-5">
      <h2 className="text-2xl font-bold">
        {grandPrix}
      </h2>

      <p className="mt-2">{country}</p>
      <p>{date}</p>

      <p className="mt-4 text-slate-400">
        Weather: {weather}
      </p>
    </div>
  );
}