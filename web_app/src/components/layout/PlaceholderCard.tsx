interface Props {
  title: string;
}

export default function PlaceholderCard({ title }: Props) {
  return (
    <div className="rounded-xl border border-slate-700 bg-slate-900 p-6">
      <h2 className="mb-4 text-xl font-semibold">
        {title}
      </h2>

      <div className="h-48 rounded-lg border border-dashed border-slate-600 flex items-center justify-center text-slate-400">
        Content will go here
      </div>
    </div>
  );
}