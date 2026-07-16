import StatCard from "../components/cards/StatCard";
import SectionCard from "../components/cards/SectionCard";

export default function Home() {
  return (
    <div className="mx-auto max-w-7xl p-8 space-y-8">
      {/* Hero */}
      <section className="rounded-xl bg-gradient-to-r from-red-700 to-black p-8">
        <h1 className="text-5xl font-bold">
          Fanalytics
        </h1>

        <p className="mt-4 max-w-3xl text-lg">
          Formula 1 analytics platform with standings,
          statistics, race insights and prediction models.
        </p>
      </section>

      {/* Stats */}
      <section className="grid grid-cols-2 gap-4 lg:grid-cols-4">
        <StatCard title="Drivers" value={20} />
        <StatCard title="Teams" value={10} />
        <StatCard title="Circuits" value={24} />
        <StatCard title="Season" value="2026" />
      </section>

      {/* Main grid */}
      <section className="grid grid-cols-1 gap-6 lg:grid-cols-2">
        <SectionCard title="Driver Standings">
          <p>Will load from standings.json</p>
        </SectionCard>

        <SectionCard title="Constructor Standings">
          <p>Will load from standings.json</p>
        </SectionCard>
      </section>

      <SectionCard title="Championship Progression">
        <div className="flex h-64 items-center justify-center rounded-lg border border-dashed border-slate-600">
          Chart placeholder
        </div>
      </SectionCard>

      <section className="grid grid-cols-1 gap-6 lg:grid-cols-2">
        <SectionCard title="Next Grand Prix">
          <p>Will load from next_race.json</p>
        </SectionCard>

        <SectionCard title="Prediction Preview">
          <p>Will load from predictions.json</p>
        </SectionCard>
      </section>
    </div>
  );
}