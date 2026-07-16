import type { ReactNode } from "react";

interface CardProps {
  title?: string;
  children: ReactNode;
}

export default function Card({ title, children }: CardProps) {
  return (
    <div className="rounded-xl border border-slate-700 bg-slate-900 p-5 shadow-sm">
      {title && (
        <h2 className="mb-4 text-xl font-semibold">
          {title}
        </h2>
      )}
      {children}
    </div>
  );
}