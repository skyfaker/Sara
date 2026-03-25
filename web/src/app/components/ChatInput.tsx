import { useState } from 'react';
import { Paperclip, Send } from 'lucide-react';

interface ChatInputProps {
  onSend: (message: string) => void;
  isLoading?: boolean;
}

export function ChatInput({ onSend, isLoading }: ChatInputProps) {
  const [input, setInput] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (input.trim() && !isLoading) {
      onSend(input.trim());
      setInput('');
    }
  };

  return (
    <div className="absolute bottom-0 left-0 right-0 pb-8 px-12">
      <form onSubmit={handleSubmit} className="relative max-w-7xl mx-auto">
        {isLoading && (
          <div className="absolute -top-8 left-0 flex items-center gap-2">
            <div className="w-2 h-2 bg-[#005daa] rounded-full"></div>
            <span className="text-[12px] text-[#94a3b8] uppercase tracking-wide font-medium">
              Awaiting Command
            </span>
          </div>
        )}
        
        <div className="bg-white rounded-2xl shadow-[0px_32px_64px_-12px_rgba(43,52,55,0.06)] border border-[rgba(193,199,212,0.1)] px-6 py-4 flex items-center gap-4">
          <button
            type="button"
            className="text-[#94a3b8] hover:text-[#005daa] transition-colors"
          >
            <Paperclip className="w-5 h-5" />
          </button>
          
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Describe your inquiry..."
            disabled={isLoading}
            className="flex-1 bg-transparent outline-none text-[16px] text-[#181c21] placeholder:text-[#94a3b8] disabled:opacity-50"
          />
          
          <button
            type="submit"
            disabled={!input.trim() || isLoading}
            className="bg-[#005daa] hover:bg-[#004d8a] disabled:opacity-50 disabled:cursor-not-allowed text-white rounded-full w-12 h-12 flex items-center justify-center transition-colors"
          >
            <Send className="w-5 h-5" />
          </button>
        </div>

        <div className="pt-2 text-center text-[10px] text-[#94a3b8]">
          Model: Monolith-v1-Turbo • Context: 128k Tokens
        </div>
      </form>
    </div>
  );
}
