import { Plus, Clock, Bookmark, Archive, Settings, LogOut } from 'lucide-react';
import svgPaths from '../../imports/svg-hfhi0zz7rh';

interface SidebarProps {
  onNewChat: () => void;
  onSelectView: (view: string) => void;
  activeView: string;
}

export function Sidebar({ onNewChat, onSelectView, activeView }: SidebarProps) {
  return (
    <div className="w-64 h-full bg-[#f8f9fa] flex flex-col p-4 gap-2">
      {/* Logo */}
      <div className="flex items-center gap-3 px-2 py-6 pb-4">
        <div className="w-10 h-10 bg-[#005daa] rounded-full flex items-center justify-center relative shadow-[0px_32px_64px_-12px_rgba(43,52,55,0.06)]">
          <svg className="w-[17.7px] h-4" fill="none" viewBox="0 0 17.7 16">
            <path d={svgPaths.p19386c00} fill="white" />
          </svg>
        </div>
        <div className="flex flex-col">
          <div className="font-['Libre_Baskerville',serif] font-bold text-[18px] text-[#373cff] leading-[28px] tracking-[-0.45px]">
            Intelligence
          </div>
          <div className="font-bold text-[10px] text-[#94a3b8] uppercase tracking-[1px] leading-[15px]">
            Monolith V1
          </div>
        </div>
      </div>

      {/* Navigation */}
      <div className="flex-1 flex flex-col gap-1">
        <button
          onClick={onNewChat}
          className="flex items-center gap-3 px-4 py-3 rounded-full bg-white shadow-[0px_1px_2px_0px_rgba(0,0,0,0.05)] hover:bg-gray-50 transition-colors"
        >
          <svg className="w-3.5 h-3.5" fill="none" viewBox="0 0 14 14">
            <path d={svgPaths.p2bb32400} fill="#373CFF" />
          </svg>
          <span className="font-medium text-[14px] text-[#373cff] leading-5">New Chat</span>
        </button>

        <button
          onClick={() => onSelectView('recent')}
          className={`flex items-center gap-3 px-4 py-3 rounded-full transition-colors ${
            activeView === 'recent' ? 'bg-white shadow-sm' : 'hover:bg-white/50'
          }`}
        >
          <svg className="w-[18px] h-[18px]" fill="none" viewBox="0 0 18 18">
            <path d={svgPaths.p22876fc0} fill="#475569" />
          </svg>
          <span className="font-medium text-[14px] text-[#475569] leading-5">Recent Sessions</span>
        </button>

        <button
          onClick={() => onSelectView('saved')}
          className={`flex items-center gap-3 px-4 py-3 rounded-full transition-colors ${
            activeView === 'saved' ? 'bg-white shadow-sm' : 'hover:bg-white/50'
          }`}
        >
          <svg className="w-3.5 h-[18px]" fill="none" viewBox="0 0 14 18">
            <path d={svgPaths.p1db08b60} fill="#475569" />
          </svg>
          <span className="font-medium text-[14px] text-[#475569] leading-5">Saved Prompts</span>
        </button>

        <button
          onClick={() => onSelectView('archive')}
          className={`flex items-center gap-3 px-4 py-3 rounded-full transition-colors ${
            activeView === 'archive' ? 'bg-white shadow-sm' : 'hover:bg-white/50'
          }`}
        >
          <svg className="w-[18px] h-[18px]" fill="none" viewBox="0 0 18 18">
            <path d={svgPaths.pf86ae00} fill="#475569" />
          </svg>
          <span className="font-medium text-[14px] text-[#475569] leading-5">Archive</span>
        </button>
      </div>

      {/* Bottom Section */}
      <div className="flex flex-col gap-4 pt-4 border-t border-[#e2e8f0]">
        {/* Settings & Logout */}
        <button className="flex items-center gap-3 px-4 py-3 hover:bg-white/50 rounded-full transition-colors">
          <svg className="w-5 h-5" fill="none" viewBox="0 0 20.1 20">
            <path d={svgPaths.p3cdadd00} fill="#475569" />
          </svg>
          <span className="font-medium text-[14px] text-[#475569] leading-5">Settings</span>
        </button>

        <button className="flex items-center gap-3 px-4 pb-3 hover:bg-white/50 rounded-full transition-colors">
          <svg className="w-[18px] h-[18px]" fill="none" viewBox="0 0 18 18">
            <path d={svgPaths.p3e9df400} fill="#475569" />
          </svg>
          <span className="font-medium text-[14px] text-[#475569] leading-5">Logout</span>
        </button>
      </div>
    </div>
  );
}
