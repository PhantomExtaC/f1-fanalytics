import type { ReactNode } from "react";

interface SectionCardProps {
  title: string;
  children: ReactNode;
}

export default function SectionCard({ title, children }: SectionCardProps) {
  return (
    <section className="relative overflow-hidden rounded-xl border-l-4 border-l-red-600 border-y-slate-800 border-r-slate-800 border bg-gradient-to-br from-neutral-950 via-slate-950 to-neutral-950 p-6 shadow-2xl shadow-red-950/10">
      {/* Decorative F1 Red Accent Line on Top Grid */}
      <div className="absolute top-0 right-0 h-[2px] w-1/3 bg-gradient-to-l from-red-600 to-transparent opacity-60" />
      
      <h2 className="mb-5 flex items-center gap-3 font-mono text-xl font-black uppercase tracking-wider text-neutral-100">
        {/* Neon Red Dot Indicator */}
        <span className="h-2.5 w-2.5 animate-pulse rounded-full bg-red-600 ring-4 ring-red-950" />
        {title}
      </h2>
      
      <div className="font-sans text-neutral-300">
        {children}
      </div>
    </section>
  );
}
