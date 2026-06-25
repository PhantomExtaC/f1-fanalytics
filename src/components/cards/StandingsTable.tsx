interface StandingRow {
  position: number;
  name: string;
  points: number;
}

interface Props {
  title: string;
  rows: StandingRow[];
}

export default function StandingsTable({
  title,
  rows,
}: Props) {
  return (
    <div className="rounded-xl border border-slate-700 bg-slate-900 p-6">
      <h2 className="mb-4 text-2xl font-bold">{title}</h2>

      <table className="w-full">
        <thead>
          <tr>
            <th className="text-left">Pos</th>
            <th className="text-left">Name</th>
            <th className="text-left">Points</th>
          </tr>
        </thead>

        <tbody>
          {rows.map((row) => (
            <tr key={row.position}>
              <td>{row.position}</td>
              <td>{row.name}</td>
              <td>{row.points}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}