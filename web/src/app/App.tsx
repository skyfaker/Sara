import { useState, useRef, useEffect } from 'react';
import { Sidebar } from './components/Sidebar';
import { TopBar } from './components/TopBar';
import { WelcomeState } from './components/WelcomeState';
import { ChatMessage, Message } from './components/ChatMessage';
import { ChatInput } from './components/ChatInput';

export default function App() {
  const [activeView, setActiveView] = useState('chat');
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [showWelcome, setShowWelcome] = useState(false);
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages]);

  const handleNewChat = () => {
    setMessages([]);
    setShowWelcome(true);
  };

  const handleSelectAction = (action: string) => {
    setShowWelcome(false);
    let message = '';
    if (action === 'strategic') {
      message = 'I need help with strategic analysis of a business model. Can you guide me through identifying architectural weaknesses?';
    } else {
      message = 'I have a codebase that needs refactoring. Can you help me analyze it for performance improvements?';
    }
    handleSendMessage(message);
  };

  const handleSendMessage = async (content: string) => {
    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content,
      timestamp: `You • ${new Date().toLocaleTimeString('en-US', { hour: 'numeric', minute: '2-digit' })}`,
    };

    setMessages((prev) => [...prev, userMessage]);
    setIsLoading(true);

    try {
      const allMessages = [...messages, userMessage];
      const res = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          messages: allMessages.map((m) => ({ role: m.role, content: m.content })),
          stream: true,
        }),
      });

      if (!res.ok) {
        const errData = await res.json().catch(() => null);
        throw new Error(errData?.message || `Request failed (${res.status})`);
      }

      const assistantId = (Date.now() + 1).toString();
      const assistantMessage: Message = {
        id: assistantId,
        role: 'assistant',
        content: '',
        timestamp: `Assistant • ${new Date().toLocaleTimeString('en-US', { hour: 'numeric', minute: '2-digit' })}`,
        model: '',
      };
      setMessages((prev) => [...prev, assistantMessage]);

      const reader = res.body!.getReader();
      const decoder = new TextDecoder();
      let buffer = '';

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split('\n');
        buffer = lines.pop() || '';

        for (const line of lines) {
          const trimmed = line.trim();
          if (!trimmed.startsWith('data: ')) continue;
          try {
            const payload = JSON.parse(trimmed.slice(6));
            if (payload.done) break;
            if (payload.content) {
              setMessages((prev) =>
                prev.map((m) =>
                  m.id === assistantId ? { ...m, content: m.content + payload.content } : m,
                ),
              );
            }
          } catch {
            // skip malformed SSE lines
          }
        }
      }
    } catch (err) {
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: `Error: ${err instanceof Error ? err.message : 'Something went wrong'}`,
        timestamp: `System • ${new Date().toLocaleTimeString('en-US', { hour: 'numeric', minute: '2-digit' })}`,
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="size-full flex bg-[#f8f9fa] font-['Inter',sans-serif]">
      {/* Sidebar */}
      <Sidebar
        onNewChat={handleNewChat}
        onSelectView={setActiveView}
        activeView={activeView}
      />

      {/* Main Content */}
      <div className="flex-1 bg-[#f9f9ff] relative overflow-hidden">
        {/* Top Bar */}
        <TopBar />

        {/* Chat Canvas */}
        <div
          ref={scrollRef}
          className="absolute inset-0 overflow-y-auto pt-[72px] pb-32"
        >
          <div className="max-w-7xl mx-auto px-12 py-8">
            {showWelcome || messages.length === 0 ? (
              <WelcomeState onSelectAction={handleSelectAction} />
            ) : (
              <div className="flex flex-col gap-12 pb-32">
                {messages.map((message) => (
                  <ChatMessage key={message.id} message={message} />
                ))}
              </div>
            )}
          </div>
        </div>

        {/* Chat Input */}
        <ChatInput onSend={handleSendMessage} isLoading={isLoading} />
      </div>
    </div>
  );
}
