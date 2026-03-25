import svgPaths from '../../imports/svg-hfhi0zz7rh';

interface WelcomeStateProps {
  onSelectAction: (action: string) => void;
}

export function WelcomeState({ onSelectAction }: WelcomeStateProps) {
  return (
    <div className="pt-20 pb-12 max-w-[620px]">
      <div className="flex flex-col gap-6">
        {/* Main Heading */}
        <div>
          <h2 className="font-bold text-[48px] leading-[48px] tracking-[-1.2px] text-[#181c21]">
            The architecture of <span className="text-[#005daa]">pure</span>
          </h2>
          <h2 className="font-bold text-[48px] leading-[48px] tracking-[-1.2px]">
            <span className="text-[#005daa]">thought</span>.
          </h2>
        </div>

        {/* Subtitle */}
        <p className="text-[18px] leading-[29.25px] text-[#414752]">
          How can I assist your creative or analytical process today? Our models
          are optimized for precision and clarity.
        </p>

        {/* Action Cards */}
        <div className="grid grid-cols-2 gap-4 pt-6">
          <button
            onClick={() => onSelectAction('strategic')}
            className="bg-white rounded-2xl p-6 border border-[rgba(193,199,212,0.1)] shadow-[0px_32px_64px_-12px_rgba(43,52,55,0.06)] hover:shadow-[0px_32px_64px_-12px_rgba(43,52,55,0.12)] transition-all text-left h-[158px] flex flex-col"
          >
            <svg className="w-[22px] h-[22px] mb-3.5" fill="none" viewBox="0 0 22 22">
              <path d={svgPaths.p11c2d500} fill="#005DAA" />
            </svg>
            <h3 className="font-bold text-[16px] leading-6 text-[#181c21] mb-2">
              Strategic Analysis
            </h3>
            <p className="text-[14px] leading-5 text-[#414752]">
              Review a business model and identify architectural weaknesses.
            </p>
          </button>

          <button
            onClick={() => onSelectAction('code')}
            className="bg-white rounded-2xl p-6 border border-[rgba(193,199,212,0.1)] shadow-[0px_32px_64px_-12px_rgba(43,52,55,0.06)] hover:shadow-[0px_32px_64px_-12px_rgba(43,52,55,0.12)] transition-all text-left h-[158px] flex flex-col"
          >
            <svg className="w-5 h-3 mb-4" fill="none" viewBox="0 0 20 12">
              <path d={svgPaths.p24c05900} fill="#005DAA" />
            </svg>
            <h3 className="font-bold text-[16px] leading-6 text-[#181c21] mb-2">
              Code Refactoring
            </h3>
            <p className="text-[14px] leading-5 text-[#414752]">
              Analyze existing repositories for performance and elegance.
            </p>
          </button>
        </div>
      </div>
    </div>
  );
}
