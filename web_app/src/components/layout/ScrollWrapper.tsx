import { type ReactNode } from 'react';

interface ScrollWrapperProps {
  children: ReactNode;
  minWidth?: string; 
}

export default function ScrollWrapper({ children, minWidth = "min-w-[600px]" }: ScrollWrapperProps) {
  return (
    <div className="relative w-full">
      {/* Scoped CSS: Affects only this specific component's scrollbar */}
      <style>{`
        .scoped-scrollbar::-webkit-scrollbar {
          height: 6px;
        }
        .scoped-scrollbar::-webkit-scrollbar-track {
          background: rgba(38, 38, 38, 0.5);
          border-radius: 4px;
        }
        .scoped-scrollbar::-webkit-scrollbar-thumb {
          background: rgba(82, 82, 82, 0.8);
          border-radius: 4px;
        }
        .scoped-scrollbar {
          scrollbar-width: thin;
          scrollbar-color: rgba(82, 82, 82, 0.8) rgba(38, 38, 38, 0.5);
        }
      `}</style>
      
      <div className="scoped-scrollbar overflow-x-auto pb-4">
        <div className={`${minWidth} whitespace-nowrap`}>
          {children}
        </div>
      </div>
    </div>
  );
}