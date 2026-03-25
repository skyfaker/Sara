import { HelpCircle, Settings } from 'lucide-react';
import imgUserProfile from 'figma:asset/ba52c19535cd4d6f97f3ffd683a3bf037db144a2.png';

export function TopBar() {
  return (
    <div className="absolute top-0 left-0 right-0 h-[72px] flex items-center justify-between px-12 z-10">
      <h1 className="text-[#373cff] font-['Libre_Baskerville',serif] font-bold text-[24px]">
        Intelligent Monolith
      </h1>

      <div className="flex items-center gap-4">
        {/* System Active Status */}
        <div className="flex items-center gap-2">
          <div className="w-2 h-2 bg-[#005daa] rounded-full"></div>
          <span className="text-[12px] text-[#475569] font-medium uppercase tracking-wide">
            System Active
          </span>
        </div>

        {/* Help Icon */}
        <button className="w-10 h-10 flex items-center justify-center rounded-full hover:bg-gray-100 transition-colors">
          <HelpCircle className="w-5 h-5 text-[#475569]" />
        </button>

        {/* Settings Icon */}
        <button className="w-10 h-10 flex items-center justify-center rounded-full hover:bg-gray-100 transition-colors">
          <Settings className="w-5 h-5 text-[#475569]" />
        </button>

        {/* User Avatar */}
        <div className="w-10 h-10 rounded-full overflow-hidden bg-gray-200">
          <img src={imgUserProfile} alt="User" className="w-full h-full object-cover" />
        </div>
      </div>
    </div>
  );
}
