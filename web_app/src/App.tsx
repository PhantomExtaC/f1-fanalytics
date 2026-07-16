import { BrowserRouter, Routes, Route } from "react-router-dom";

import Navbar from "./components/layout/Navbar";
import Footer from "./components/layout/Footer";

import Home from "./pages/Home";
import Drivers from "./pages/Drivers";
import Teams from "./pages/Teams";
import Tracks from "./pages/Tracks";
import Calendar from "./pages/Calendar";
import Standings from "./pages/Standings";
import Simulator from "./pages/Simulator";

export default function App() {
  return (
    <BrowserRouter>
      <Navbar />

      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/drivers" element={<Drivers />} />
        <Route path="/teams" element={<Teams />} />
        <Route path="/tracks" element={<Tracks />} />
        <Route path="/calendar" element={<Calendar />} />
        <Route path="/standings" element={<Standings />} />
        <Route path="/simulator" element={<Simulator />} />
      </Routes>

      <Footer />
    </BrowserRouter>
  );
}