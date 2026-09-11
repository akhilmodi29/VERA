with open('frontend/src/layouts/MainLayout.tsx', 'w', encoding='utf-8') as f:
    f.write('''import React, { useEffect, useState } from 'react';
import { Outlet, NavLink, useLocation } from 'react-router-dom';
import { 
  ShieldAlert, 
  LayoutDashboard, 
  Activity, 
  Users, 
  FileCheck,
  Server,
  Bell,
  Search,
  ChevronRight
} from 'lucide-react';
import { api } from '../services/api';

const MainLayout: React.FC = () => {
  const [isApiConnected, setIsApiConnected] = useState<boolean | null>(null);
  const location = useLocation();

  useEffect(() => {
    const checkStatus = async () => {
      try {
        await api.checkHealth();
        setIsApiConnected(true);
      } catch (err) {
        setIsApiConnected(false);
      }
    };
    
    checkStatus();
    const interval = setInterval(checkStatus, 30000);
    return () => clearInterval(interval);
  }, []);

  const getPageTitle = () => {
    switch (location.pathname) {
      case '/': return 'Threat Dashboard';
      case '/sessions': return 'Active Sessions';
      case '/voice-profiles': return 'Voice Identity Registry';
      case '/evidence': return 'Evidence Ledger';
      default: return 'Overview';
    }
  };

  return (
    <div className="flex h-screen bg-vera-darker text-vera-text font-sans overflow-hidden selection:bg-vera-accent/30">
      {/* Sidebar */}
      <aside className="w-[280px] bg-[#0A0D14] border-r border-vera-border flex flex-col shadow-2xl z-20 relative">
        <div className="absolute inset-0 bg-gradient-to-b from-vera-accent/5 to-transparent opacity-50 pointer-events-none" />
        
        <div className="h-20 flex items-center px-8 border-b border-vera-border bg-[#0A0D14] relative z-10">
          <div className="relative">
            <ShieldAlert className="w-8 h-8 text-vera-accent mr-4" />
            <div className="absolute -top-1 -right-1 w-2 h-2 rounded-full bg-vera-accent animate-ping-slow" />
          </div>
          <div>
            <span className="font-bold text-xl tracking-widest text-white block leading-tight">VERA</span>
            <span className="text-[10px] text-vera-accent uppercase tracking-[0.2em] block font-semibold mt-0.5">SOC / SIH2026</span>
          </div>
        </div>
        
        <div className="px-6 py-4">
          <div className="text-[10px] text-vera-textMuted uppercase tracking-widest font-semibold mb-3">Detection Modules</div>
          <nav className="space-y-1">
            <NavItem to="/" icon={<LayoutDashboard size={18} />} label="Threat Dashboard" exact />
            <NavItem to="/sessions" icon={<Activity size={18} />} label="Live Sessions" />
          </nav>
        </div>

        <div className="px-6 py-4">
          <div className="text-[10px] text-vera-textMuted uppercase tracking-widest font-semibold mb-3">Intelligence</div>
          <nav className="space-y-1">
            <NavItem to="/voice-profiles" icon={<Users size={18} />} label="Identity Registry" />
            <NavItem to="/evidence" icon={<FileCheck size={18} />} label="Evidence Ledger" />
          </nav>
        </div>

        <div className="mt-auto p-6 relative z-10">
          <div className="p-4 rounded-xl border border-vera-border bg-vera-panel/50 backdrop-blur-md">
            <div className="flex items-center text-xs font-medium text-vera-text">
              <Server size={14} className="mr-2 text-vera-textMuted" />
              <span>System Status</span>
              <div className={ + 'ml-auto flex items-center space-x-2 px-2 py-1 rounded text-[10px] uppercase tracking-wider font-bold  + '}>
                {isApiConnected ? <span className="w-1.5 h-1.5 rounded-full bg-vera-success animate-pulse" /> : null}
                <span>{isApiConnected === null ? "SYNC" : isApiConnected ? "ONLINE" : "OFFLINE"}</span>
              </div>
            </div>
            {isApiConnected === false && (
              <div className="mt-3 text-[10px] text-vera-danger/80 leading-relaxed">
                Critical: Connection to VERA Core Engine lost. Please restart FastAPI service.
              </div>
            )}
          </div>
        </div>
      </aside>

      {/* Main Content */}
      <div className="flex-1 flex flex-col min-w-0 bg-[#06080D] relative">
        <div className="absolute inset-0 bg-[linear-gradient(to_right,#80808012_1px,transparent_1px),linear-gradient(to_bottom,#80808012_1px,transparent_1px)] bg-[size:24px_24px] pointer-events-none" />

        <header className="h-20 bg-[#0A0D14]/90 backdrop-blur-md border-b border-vera-border flex items-center justify-between px-8 z-10 sticky top-0 shadow-sm">
          <div className="flex items-center text-sm font-medium">
            <span className="text-vera-textMuted hover:text-white transition-colors cursor-pointer">VERA Command Center</span>
            <ChevronRight className="w-4 h-4 mx-2 text-vera-border" />
            <span className="text-white tracking-wide">{getPageTitle()}</span>
          </div>
          
          <div className="flex items-center space-x-6">
            <div className="flex items-center text-vera-textMuted hover:text-white transition-colors cursor-pointer">
              <Search className="w-4 h-4 mr-2" />
              <span className="text-xs font-medium uppercase tracking-widest">Query</span>
            </div>
            <div className="relative cursor-pointer text-vera-textMuted hover:text-white transition-colors">
              <Bell className="w-4 h-4" />
              <div className="absolute -top-1 -right-1 w-2 h-2 rounded-full bg-vera-accent animate-pulse" />
            </div>
            <div className="flex items-center space-x-3 pl-6 border-l border-vera-border cursor-pointer group">
              <div className="text-right hidden md:block">
                <div className="text-xs font-bold text-white group-hover:text-vera-accent transition-colors">Operator Alpha</div>
                <div className="text-[10px] text-vera-textMuted uppercase tracking-widest">Lvl 4 Clearance</div>
              </div>
              <div className="w-9 h-9 rounded-full bg-vera-accent/10 border border-vera-accent/30 flex items-center justify-center text-vera-accent font-bold text-xs shadow-[0_0_10px_rgba(59,130,246,0.2)]">
                OA
              </div>
            </div>
          </div>
        </header>
        
        <main className="flex-1 overflow-y-auto p-8 relative z-0">
          <div className="max-w-7xl mx-auto">
            <Outlet />
          </div>
        </main>
      </div>
    </div>
  );
};

interface NavItemProps {
  to: string;
  icon: React.ReactNode;
  label: string;
  exact?: boolean;
}

const NavItem: React.FC<NavItemProps> = ({ to, icon, label, exact }) => (
  <NavLink
    to={to}
    end={exact}
    className={({ isActive }) =>
       + 'lex items-center px-4 py-3 rounded-lg transition-all duration-300 relative group overflow-hidden  + '
    }
  >
    {({ isActive }) => (
      <>
        {isActive && (
          <div className="absolute left-0 top-0 bottom-0 w-1 bg-vera-accent shadow-[0_0_10px_rgba(59,130,246,0.8)]" />
        )}
        <span className={ + 'mr-3  + '}>
          {icon}
        </span>
        <span className="tracking-wide text-sm">{label}</span>
      </>
    )}
  </NavLink>
);

export default MainLayout;
''')
