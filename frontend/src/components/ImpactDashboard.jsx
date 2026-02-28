import React, { useEffect, useState } from 'react';
import { X, TrendingDown, Clock, Zap } from 'lucide-react';

export default function ImpactDashboard({ impact, onClose }) {
    const [show, setShow] = useState(false);

    useEffect(() => {
        // Entrance animation delay
        setTimeout(() => setShow(true), 100);
    }, []);

    return (
        <div className={`absolute inset-0 z-50 flex items-center justify-center p-8 bg-slate-950/80 backdrop-blur-sm transition-opacity duration-500 ${show ? 'opacity-100' : 'opacity-0 pointer-events-none'}`}>

            {/* Glowing Backdrop */}
            <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[400px] bg-gradient-to-tr from-indigo-500/30 to-emerald-500/30 blur-[100px] pointer-events-none"></div>

            <div className={`bg-slate-900 border border-slate-700/50 shadow-2xl shadow-indigo-500/20 rounded-2xl w-full max-w-2xl overflow-hidden transition-all duration-700 transform ${show ? 'translate-y-0 scale-100' : 'translate-y-12 scale-95'}`}>

                {/* Header */}
                <div className="bg-gradient-to-r from-indigo-600/20 to-emerald-600/20 p-6 flex justify-between items-start border-b border-white/5 relative">
                    <div>
                        <div className="text-indigo-400 text-xs font-bold uppercase tracking-widest mb-1">Impact Analysis</div>
                        <h3 className="text-2xl font-bold text-white tracking-tight">{impact.title}</h3>
                        {impact.note && <p className="text-slate-400 text-sm mt-1">{impact.note}</p>}
                    </div>
                    <button onClick={onClose} className="text-slate-500 hover:text-white transition-colors bg-white/5 hover:bg-white/10 p-2 rounded-full backdrop-blur">
                        <X size={20} />
                    </button>
                    <div className="absolute bottom-0 left-0 h-[2px] bg-gradient-to-r from-indigo-500 to-emerald-400 w-full"></div>
                </div>

                {/* Stats Grid */}
                <div className="p-8 grid grid-cols-1 md:grid-cols-3 gap-6 relative">
                    {/* Stat 1 */}
                    <div className="flex flex-col items-center justify-center p-4 bg-slate-800/30 rounded-xl border border-white/5 group hover:bg-slate-800/50 transition-all hover:-translate-y-1">
                        <div className="bg-indigo-500/20 p-3 rounded-full text-indigo-400 mb-3 group-hover:scale-110 transition-transform">
                            <TrendingDown size={24} />
                        </div>
                        <div className="text-3xl font-bold text-white mb-1"><span className="text-indigo-400">{impact.congestion}</span>%</div>
                        <div className="text-xs text-slate-500 uppercase tracking-wider font-semibold text-center mt-1 text-balance">Congestion<br />Reduced</div>
                    </div>

                    {/* Stat 2 */}
                    <div className="flex flex-col items-center justify-center p-4 bg-slate-800/30 rounded-xl border border-white/5 group hover:bg-slate-800/50 transition-all hover:-translate-y-1">
                        <div className="bg-emerald-500/20 p-3 rounded-full text-emerald-400 mb-3 group-hover:scale-110 transition-transform">
                            <Clock size={24} />
                        </div>
                        <div className="text-3xl font-bold text-white mb-1"><span className="text-emerald-400">{impact.downtime}</span>h</div>
                        <div className="text-xs text-slate-500 uppercase tracking-wider font-semibold text-center mt-1 text-balance">Downtime<br />Avoided</div>
                    </div>

                    {/* Stat 3 */}
                    <div className="flex flex-col items-center justify-center p-4 bg-slate-800/30 rounded-xl border border-white/5 group hover:bg-slate-800/50 transition-all hover:-translate-y-1">
                        <div className="bg-yellow-500/20 p-3 rounded-full text-yellow-400 mb-3 group-hover:scale-110 transition-transform">
                            <Zap size={24} />
                        </div>
                        <div className="text-3xl font-bold text-white mb-1">
                            {impact.energy > 0 ? <span className="text-emerald-400">+{impact.energy}%</span> : <span className="text-red-400">{impact.energy}%</span>}
                        </div>
                        <div className="text-xs text-slate-500 uppercase tracking-wider font-semibold text-center mt-1 text-balance">Est. Energy<br />Saved</div>
                    </div>
                </div>

                {/* Footer info */}
                <div className="bg-slate-950/50 p-4 border-t border-white/5 text-center flex justify-between items-center px-6">
                    <div className="text-[10px] text-slate-500 tracking-wider">PREDICTIVE DIGITAL TWIN AI ENGINE</div>
                    <button onClick={onClose} className="px-6 py-2 bg-indigo-600 hover:bg-indigo-500 text-white text-sm font-semibold rounded-lg transition-colors shadow-lg shadow-indigo-600/30">
                        Acknowledge
                    </button>
                </div>
            </div>
        </div>
    );
}
