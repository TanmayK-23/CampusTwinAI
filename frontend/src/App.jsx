import React, { useState, useEffect } from 'react';
import CampusMap from './components/CampusMap';
import Dashboard from './components/Dashboard';
import SimulationPanel from './components/SimulationPanel';
import ImpactDashboard from './components/ImpactDashboard';

function App() {
  const [crowdData, setCrowdData] = useState([]);
  const [shuttleData, setShuttleData] = useState(null);
  const [benchmarkData, setBenchmarkData] = useState(null);
  const [simulationImpact, setSimulationImpact] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [crowdRes, shutRes, benchRes] = await Promise.all([
          fetch('http://localhost:8000/crowd/current'),
          fetch('http://localhost:8000/route/optimize'),
          fetch('http://localhost:8000/benchmark/inference')
        ]);

        const crowd = await crowdRes.json();
        const shut = await shutRes.json();
        const bench = await benchRes.json();

        setCrowdData(crowd);
        setShuttleData(shut);
        setBenchmarkData(bench);
      } catch (e) {
        console.error("Failed to fetch data:", e);
      }
    };

    fetchData();
    const interval = setInterval(fetchData, 10000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="h-screen w-full bg-slate-950 text-slate-100 flex flex-col font-sans overflow-hidden">
      <header className="p-4 border-b border-white/5 flex justify-between items-center bg-slate-900/80 backdrop-blur-md z-10 shadow-lg">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center font-bold text-white shadow-lg shadow-indigo-500/20">CT</div>
          <h1 className="text-xl font-bold bg-gradient-to-r from-indigo-400 to-purple-400 bg-clip-text text-transparent tracking-tight">
            Campus Twin AI
          </h1>
        </div>
        <div className="flex gap-4 text-sm items-center">
          {benchmarkData && (
            <div className="px-4 py-1.5 rounded-full bg-slate-800/80 border border-slate-700/50 flex align-center gap-4">
              <span className="text-slate-400 tracking-wide text-xs uppercase font-semibold mt-1">Live Backend</span>
              <div className="h-4 w-[1px] bg-slate-700"></div>
              <span>CPU: <span className="text-slate-300 font-mono">{benchmarkData.cpu_time_ms}ms</span></span>
              <span>GPU: <span className="text-emerald-400 font-mono font-medium">{benchmarkData.gpu_time_ms}ms</span></span>
              <span className="text-emerald-400 font-bold bg-emerald-400/10 px-2 rounded">{benchmarkData.speedup}x</span>
            </div>
          )}
        </div>
      </header>

      <main className="flex-1 p-4 grid grid-cols-1 lg:grid-cols-4 gap-4 overflow-hidden h-[calc(100vh-73px)]">
        {/* Left col: Controls & Models */}
        <div className="lg:col-span-1 flex flex-col gap-4 overflow-y-auto pr-2 custom-scrollbar">
          <Dashboard crowd={crowdData} shuttle={shuttleData} />
          <SimulationPanel
            onSimulate={(res) => setSimulationImpact(res)}
            shuttleData={shuttleData}
            crowdData={crowdData}
          />
        </div>

        {/* Middle/Right col: 3D Map */}
        <div className="lg:col-span-3 rounded-2xl overflow-hidden border border-white/5 bg-slate-900 shadow-2xl relative shadow-black/50">
          <CampusMap crowdData={crowdData} />
          {simulationImpact && <ImpactDashboard impact={simulationImpact} onClose={() => setSimulationImpact(null)} />}

          {/* Overlay Map Key */}
          <div className="absolute top-4 right-4 bg-slate-950/80 backdrop-blur p-3 rounded-xl border border-white/5 text-xs text-slate-400 shadow-xl">
            <div className="font-semibold text-slate-200 mb-2">Crowd Density</div>
            <div className="flex items-center gap-2 mb-1"><div className="w-3 h-3 rounded-full bg-emerald-500/80 shadow-[0_0_10px_rgba(16,185,129,0.5)]"></div> Normal</div>
            <div className="flex items-center gap-2 mb-1"><div className="w-3 h-3 rounded-full bg-yellow-400/80 shadow-[0_0_10px_rgba(250,204,21,0.5)]"></div> Moderate</div>
            <div className="flex items-center gap-2"><div className="w-3 h-3 rounded-full bg-red-500/80 shadow-[0_0_10px_rgba(239,68,68,0.5)]"></div> High Alert</div>
          </div>
        </div>
      </main>
    </div>
  )
}
export default App;
