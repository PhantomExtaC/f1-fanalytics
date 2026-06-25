import { NavLink } from "react-router-dom";

const links = [
  { to: "/", label: "Home" },
  { to: "/drivers", label: "Drivers" },
  { to: "/teams", label: "Teams" },
  { to: "/tracks", label: "Tracks" },
  { to: "/calendar", label: "Calendar" },
  { to: "/standings", label: "Standings" },
  { to: "/simulator", label: "Simulator" },
];

export default function Navbar() {
  return (
    <header className="sticky top-0 border-b border-gray-700 bg-black">
      <div className="mx-auto flex max-w-7xl items-center justify-between p-4">
        <h1 className="text-2xl font-bold text-red-600">Fanalytics</h1>

        <nav className="flex flex-wrap gap-4">
          {links.map((link) => (
            <NavLink
              key={link.to}
              to={link.to}
              className={({ isActive }) =>
                isActive ? "text-red-500" : "text-white"
              }
            >
              {link.label}
            </NavLink>
          ))}
        </nav>
      </div>
    </header>
  );
}