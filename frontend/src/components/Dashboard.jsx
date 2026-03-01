import React from 'react';
import { BarChart, Bar, XAxis, Tooltip, ResponsiveContainer } from 'recharts';
import { Users, Bus, Gauge, Activity } from 'lucide-react';

export default function Dashboard({ crowd, shuttle }) {
    // Current total campus density
    const totalDensity = crowd.reduce((sum, zone) => sum + (zone.density || 0), 0);

    return (
        <div className="flex flex-col gap-4">
            <h2 className="text-sm font-semibold text-slate-400 uppercase tracking-widest flex items-center gap-2">
                <Activity size={16} /> Live Telemetry
            </h2>

            {/* Top Stat Cards */}
            <div className="bg-slate-900/50 backdrop-blur border border-white/5 p-4 rounded-xl">
                <div className="text-slate-500 text-xs mb-1 flex items-center gap-1"><Users size={12} /> Total Crowd</div>
                <div className="text-2xl font-bold text-white">{Math.round(totalDensity)}</div>
            </div>

            {/* AI Optimization (Shuttle) */}
            <div className="bg-gradient-to-br from-indigo-900/20 to-purple-900/10 border border-indigo-500/20 p-4 rounded-xl">
                <div className="text-indigo-400 text-xs font-semibold mb-2 flex items-center gap-1"><Bus size={14} /> Ai Route Optimizer</div>
                {shuttle ? (
                    <div>
                        <div className="text-sm font-medium text-slate-200 mb-2 leading-relaxed">
                            {shuttle.suggested_route.join(" → ")}
                        </div>
                        <div className="flex justify-between items-end border-t border-indigo-500/10 pt-2 mt-2">
                            <div>
                                <div className="text-[10px] text-slate-500">Delay Avoided</div>
                                <div className="text-emerald-400 font-bold text-sm">↓ {shuttle.expected_delay_reduction_pct}%</div>
                            </div>
                            <div>
                                <div className="text-[10px] text-slate-500">Est. Time</div>
                                <div className="text-indigo-300 font-bold text-sm">{shuttle.total_time_mins}m</div>
                            </div>
                        </div>
                    </div>
                ) : (
                    <div className="text-sm text-slate-500 animate-pulse">Calculating route...</div>
                )}
            </div>

            {/* Crowd Distribution Chart */}
            <div className="bg-slate-900/50 backdrop-blur border border-white/5 p-4 rounded-xl flex-1 min-h-[160px] flex flex-col">
                <div className="text-slate-400 text-xs font-semibold mb-3 flex items-center gap-1"><Gauge size={14} /> Density by Zone</div>
                <div className="flex-1 w-full h-full">
                    {crowd.length > 0 ? (
                        <ResponsiveContainer width="100%" height="100%">
                            <BarChart data={crowd.map(c => ({ name: c.zone_id.substring(0, 6), density: Math.round(c.density) }))}>
                                <XAxis dataKey="name" stroke="#64748b" tick={{ fill: '#64748b', fontSize: 10 }} axisLine={false} tickLine={false} />
                                <Tooltip cursor={{ fill: 'transparent' }} contentStyle={{ backgroundColor: '#0f172a', borderColor: '#1e293b', color: '#f8fafc', fontSize: 12 }} />
                                <Bar dataKey="density" fill="#6366f1" radius={[4, 4, 0, 0]} />
                            </BarChart>
                        </ResponsiveContainer>
                    ) : (
                        <div className="h-full flex items-center justify-center text-slate-600 text-xs">Waiting for sensors...</div>
                    )}
                </div>
            </div>
        </div>
    );
}
