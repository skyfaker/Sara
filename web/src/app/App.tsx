import { useState, useRef, useEffect } from 'react';
import { Sidebar } from './components/Sidebar';
import { TopBar } from './components/TopBar';
import { WelcomeState } from './components/WelcomeState';
import { ChatMessage, Message } from './components/ChatMessage';
import { ChatInput } from './components/ChatInput';

export default function App() {
  const [activeView, setActiveView] = useState('chat');
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      role: 'user',
      content: `Can you explain the concept of "Intelligent Monoliths" in software architecture and how it contrasts with microservices in terms of maintainability?`,
      timestamp: 'You • 10:24 AM',
    },
    {
      id: '2',
      role: 'assistant',
      content: '',
      timestamp: '',
      hasImage: true,
      model: 'deepseek-chat',
    },
  ]);
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

  const handleSendMessage = (content: string) => {
    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content,
      timestamp: `You • ${new Date().toLocaleTimeString('en-US', { hour: 'numeric', minute: '2-digit' })}`,
    };

    setMessages((prev) => [...prev, userMessage]);
    setIsLoading(true);

    // Simulate AI response
    setTimeout(() => {
      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: '',
        timestamp: '',
        hasImage: Math.random() > 0.5,
        model: 'deepseek-chat',
      };
      setMessages((prev) => [...prev, assistantMessage]);
      setIsLoading(false);
    }, 2000);
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
