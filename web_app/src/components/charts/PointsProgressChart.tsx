import React, { useMemo } from 'react';
import { 
  LineChart, Line, XAxis, YAxis, CartesianGrid, 
  Tooltip, Legend, ResponsiveContainer 
} from 'recharts';
import type { PointsProgression } from '../../types/progression';

// Fallback color map for top contenders
const DRIVER_COLORS: Record<string, string> = {
  // --- Your Explicit Requests ---
  //ferrari 
  hamilton:   "#580202", // Pink
  leclerc:    "#E8002D", // Red

  //mclaren boi
  piastri:    "#FFD700", // Yellow
  norris:     "#CCFF00", // Neon Yellow

  //merc
  russell:    "#71db47", // Sky Green
  antonelli:  "#27F4D2", // Mercedes Neon Blue

  // Red Bull
  verstappen: "#FF8C00", // Orange
  hadjar:     "#000080", // Navy Blue (Isac)

  // VCARB
  lindblad:   "#14c3e2", // Sky Blue 
  lawson:     "#04818a", // Teal 

  // --- Rest of the Grid (Team Colors with slight variations to avoid repetition) ---
  // Aston Martin
  alonso:     "#229971", // Standard AM Green
  stroll:     "#166B4E", // Darker AM Green

  // Williams
  sainz:      "#005AFF", // Vibrant Williams Blue
  albon:      "#041E42", // Dark Williams Navy

  // Alpine
  gasly:      "#FD4BC7", // Alpine BWT Pink
  colapinto:  "#00A0FE", // Light Blue

  // Haas
  ocon:       "#B6BABD", // Haas Light Grey
  bearman:    "#787878", // Haas Dark Grey

  // Audi
  hulkenberg: "#52E252", // Kick Neon Green
  bortoleto:  "#000000", // Sauber Black

  // Fallbacks / Reserves (Just in case they appear in the data)
  perez:      "#faea0c", // Cadillac Yellow
  
};

interface PointsProgressChartProps {
  data: PointsProgression[];
}

export const PointsProgressChart: React.FC<PointsProgressChartProps> = ({ data }) => {
  // Extract the Top 6 drivers based on the most recent round
  const topDrivers = useMemo(() => {
    if (!data || data.length === 0) return [];

    const latestRound = data[data.length - 1];
    
    // Extract keys, filter out "round", and sort by highest points
    const driverKeys = Object.keys(latestRound).filter(key => key !== "round");
    
    return driverKeys
      .sort((a, b) => latestRound[b] - latestRound[a])
      .slice(0, 6);
  }, [data]);

  if (!data.length) {
    return <div className="flex h-64 items-center justify-center text-gray-500">Loading Chart...</div>;
  }

  return (
    <div className="h-[450px] w-full">
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={data} margin={{ top: 20, right: 30, left: 10, bottom: 20 }}>
          <CartesianGrid strokeDasharray="3 3" opacity={0.3} vertical={false} />
          
          <XAxis 
            dataKey="round" 
            label={{ value: 'Round', position: 'insideBottom', offset: -10 }} 
            tick={{ fill: '#666' }}
            axisLine={false}
            tickLine={false}
          />
          <YAxis 
            tick={{ fill: '#666' }}
            axisLine={false}
            tickLine={false}
          />
          
          <Tooltip 
            contentStyle={{ backgroundColor: '#1a1a1a', borderRadius: '8px', border: 'none', color: '#fff' }}
            itemStyle={{ color: '#fff' }}
            labelFormatter={(label) => `Round ${label}`}
          />
          
          <Legend verticalAlign="top" height={36} wrapperStyle={{ textTransform: 'capitalize' }} />
          
          {topDrivers.map((driverId, index) => (
            <Line
              key={driverId}
              type="monotone"
              dataKey={driverId}
              name={driverId.replace('_', ' ')} 
              stroke={DRIVER_COLORS[driverId] || `hsl(${index * 50}, 70%, 50%)`}
              strokeWidth={3}
              dot={false}
              activeDot={{ r: 6, strokeWidth: 0 }}
            />
          ))}
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};