import { useState } from "react";
import { NavLink } from "react-router-dom";

const links = [
  { to: "/", label: "Home" },
  { to: "/drivers", label: "Drivers" },
  { to: "/teams", label: "Teams" },
  { to: "/tracks", label: "Tracks" },
  { to: "/calendar", label: "Calendar" },
  { to: "/simulator", label: "Simulator" },
];

export default function Navbar() {
  const [isOpen, setIsOpen] = useState(false);

  const toggleMenu = () => setIsOpen(!isOpen);
  const closeMenu = () => setIsOpen(false);

  return (
    <header className="sticky top-0 z-50 border-b border-gray-700 bg-black">
      <div className="mx-auto flex max-w-7xl items-center justify-between p-4">
        {/* Logo */}
        <h1 className="text-2xl font-bold text-red-600">LapLogic</h1>

        {/* Desktop Navigation */}
        <nav className="hidden gap-6 md:flex">
          {links.map((link) => (
            <NavLink
              key={link.to}
              to={link.to}
              className={({ isActive }) =>
                isActive
                  ? "text-red-500 font-semibold transition-colors"
                  : "text-white hover:text-red-400 transition-colors"
              }
            >
              {link.label}
            </NavLink>
          ))}
        </nav>

        {/* Hamburger Menu Button (Mobile Only) */}
        <button
          onClick={toggleMenu}
          className="text-white focus:outline-none md:hidden"
          aria-label="Toggle menu"
        >
          {isOpen ? (
            // X (Close) Icon
            <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          ) : (
            // Hamburger Icon
            <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
            </svg>
          )}
        </button>
      </div>

      {/* Mobile Navigation Dropdown */}
      {isOpen && (
        <nav className="border-t border-gray-700 bg-black px-4 py-4 md:hidden">
          <ul className="flex flex-col space-y-4">
            {links.map((link) => (
              <li key={link.to}>
                <NavLink
                  to={link.to}
                  onClick={closeMenu}
                  className={({ isActive }) =>
                    isActive
                      ? "block text-red-500 font-semibold text-lg"
                      : "block text-white hover:text-red-400 text-lg"
                  }
                >
                  {link.label}
                </NavLink>
              </li>
            ))}
          </ul>
        </nav>
      )}
    </header>
  );
}