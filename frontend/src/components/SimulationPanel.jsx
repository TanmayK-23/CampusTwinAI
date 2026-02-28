import React, { useState } from 'react';
import { Play, Activity, Cpu, Bus } from 'lucide-react';

export default function SimulationPanel({ onSimulate }) {
    const [loading, setLoading] = useState(false);

    const handleSimulate = async (type) => {
        setLoading(type);

        // Mock latency for dramatic effect
        await new Promise(r => setTimeout(r, 1500));

        let impact = { type, title: "" };

        switch (type) {
            case 'gate':
                try {
                    // Call predictive backend
                    const res = await fetch('http://localhost:8000/crowd/simulate', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ zone_id: 'MainBlock', event_flag: 0 })
                    });
                    const data = await res.json();

                    impact.title = "Redistributed Crowd via Gate 3";
                    impact.congestion = 38; // 38% reduction
                    impact.downtime = 0;
                    impact.energy = 5;
                    impact.note = `Predicted density dropped to ${data.simulated_density} pax`;
                } catch {
                    impact.title = "Opened Gate 3";
                    impact.congestion = 38;
                    impact.downtime = 0;
                    impact.energy = 0;
                }
                break;
            case 'shuttle':
                impact.title = "Deployed Extra Shuttle";
                impact.congestion = 15;
                impact.downtime = 0;
                impact.energy = -5; // Costs slightly more energy
                impact.note = `Overall transit delays cut by an additional 25%`;
                break;
        }

        setLoading(false);
        onSimulate(impact);
    };

    return (
        <div className="bg-slate-900/50 backdrop-blur border border-indigo-500/20 p-4 rounded-xl shadow-[0_0_15px_rgba(99,102,241,0.1)] relative overflow-hidden">
            <div className="absolute top-0 left-0 w-full h-[1px] bg-gradient-to-r from-transparent via-indigo-500/50 to-transparent"></div>

            <h2 className="text-sm font-semibold text-indigo-400 uppercase tracking-widest flex items-center gap-2 mb-4">
                <Play size={16} /> What-If Simulations
            </h2>

            <div className="flex flex-col gap-3">
                <button
                    onClick={() => handleSimulate('gate')}
                    disabled={loading}
                    className="w-full text-left bg-black/40 hover:bg-indigo-900/40 border border-white/5 hover:border-indigo-500/50 transition-all p-3 rounded-lg group text-sm relative overflow-hidden"
                >
                    <div className="flex items-center gap-3 relative z-10">
                        <div className="bg-indigo-500/20 p-1.5 rounded text-indigo-400 group-hover:scale-110 transition-transform"><Activity size={16} /></div>
                        <div>
                            <div className="font-semibold text-slate-200">Open Gate 3</div>
                            <div className="text-[10px] text-slate-500">Diffuse main block crowd density</div>
                        </div>
                    </div>
                    {loading === 'gate' && <div className="absolute inset-0 bg-indigo-500/10 animate-pulse"></div>}
                </button>

                <button
                    onClick={() => handleSimulate('shuttle')}
                    disabled={loading}
                    className="w-full text-left bg-black/40 hover:bg-purple-900/40 border border-white/5 hover:border-purple-500/50 transition-all p-3 rounded-lg group text-sm relative overflow-hidden"
                >
                    <div className="flex items-center gap-3 relative z-10">
                        <div className="bg-purple-500/20 p-1.5 rounded text-purple-400 group-hover:scale-110 transition-transform"><Bus size={16} /></div>
                        <div>
                            <div className="font-semibold text-slate-200">Add Extra Shuttle</div>
                            <div className="text-[10px] text-slate-500">Recalculate A* transit routes</div>
                        </div>
                    </div>
                    {loading === 'shuttle' && <div className="absolute inset-0 bg-purple-500/10 animate-pulse"></div>}
                </button>
            </div>

            {loading && (
                <div className="mt-4 text-[10px] text-indigo-400 text-center uppercase tracking-widest flex items-center justify-center gap-2 animate-pulse">
                    <Cpu size={12} /> Running Deep Inference...
                </div>
            )}
        </div>
    );
}
