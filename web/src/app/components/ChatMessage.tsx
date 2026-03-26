import svgPaths from '../../imports/svg-hfhi0zz7rh';

export interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: string;
  hasImage?: boolean;
  model?: string;
}

interface ChatMessageProps {
  message: Message;
}

export function ChatMessage({ message }: ChatMessageProps) {
  if (message.role === 'user') {
    return (
      <div className="flex flex-col items-end w-full">
        <div className="bg-white max-w-[603px] rounded-tl-3xl rounded-bl-3xl rounded-br-3xl p-5 border border-[rgba(193,199,212,0.05)] shadow-[0px_32px_64px_-12px_rgba(43,52,55,0.06)]">
          <p className="text-[16px] leading-[26px] text-[#181c21] whitespace-pre-wrap">
            {message.content}
          </p>
        </div>
        <div className="pt-2 px-2">
          <p className="text-[10px] leading-[15px] text-[#94a3b8] uppercase tracking-[-0.5px] font-bold">
            {message.timestamp}
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="flex flex-col gap-6 w-full">
      <div className="flex gap-4 items-start w-full">
        {/* Avatar */}
        <div className="w-8 h-8 bg-[#005daa] rounded-full flex items-center justify-center flex-shrink-0">
          <span className="text-white font-bold text-[10px] leading-[15px]">IM</span>
        </div>

        {/* Message Content */}
        <div className="bg-[#f2f3fb] max-w-[696px] rounded-tr-3xl rounded-bl-3xl rounded-br-3xl p-8 border border-[rgba(255,255,255,0.4)] shadow-[0px_32px_64px_-12px_rgba(43,52,55,0.06)] flex-1">
          <div className="text-[16px] leading-[26px] text-[#181c21] whitespace-pre-wrap">
            {message.content}
          </div>
        </div>
      </div>

      {/* Action Buttons */}
      <div className="flex items-center gap-4 pl-12">
        <button className="group flex items-center gap-2 text-[#94a3b8] hover:text-[#005daa] transition-colors">
          <svg className="w-3 h-3" fill="none" viewBox="0 0 11.6667 11.6667">
            <path d={svgPaths.p1fd12b00} className="fill-current" />
          </svg>
        </button>
        <button className="group flex items-center gap-2 text-[#94a3b8] hover:text-[#005daa] transition-colors">
          <svg className="w-[10.5px] h-3" fill="none" viewBox="0 0 10.5 11.6667">
            <path d={svgPaths.p29eb9000} className="fill-current" />
          </svg>
        </button>
        <div className="text-[10px] text-[#94a3b8] tracking-wide">
          {message.model ? message.model : ''}
        </div>
      </div>
    </div>
  );
}
