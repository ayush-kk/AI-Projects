import { useRef, useEffect } from 'react';
import { motion } from 'framer-motion';
import { HiOutlineSparkles, HiOutlineDocumentText, HiOutlinePhoto, HiOutlineCode, HiOutlineGlobeAlt, HiOutlineChatBubbleBottomCenter } from 'react-icons/hi2';
import MessageBubble from './MessageBubble';
import StreamingMessage from './StreamingMessage';
import ChatInput from './ChatInput';
import { useChat } from '../../context/ChatContext';

const STARTERS = [
  { icon: HiOutlineDocumentText, label: 'Summarize a document', prompt: 'Help me summarize a document I will upload' },
  { icon: HiOutlinePhoto, label: 'Generate an image', prompt: 'Generate an image of ' },
  { icon: HiOutlineCode, label: 'Write some code', prompt: 'Write a code snippet that ' },
  { icon: HiOutlineGlobeAlt, label: 'Search the web', prompt: 'Search the web for ' },
  { icon: HiOutlineChatBubbleBottomCenter, label: 'General chat', prompt: 'Hello! I would like to ' },
  { icon: HiOutlineDocumentText, label: 'Create a report', prompt: 'Generate a professional report about ' },
];

export default function ChatWindow({ onSendMessage }) {
  const { messages, isStreaming, streamingMessage } = useChat();
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, streamingMessage]);

  const isEmpty = messages.length === 0 && !isStreaming;

  return (
    <div className="flex flex-col h-full">
      <div className="flex-1 overflow-y-auto">
        {isEmpty ? (
          <div className="flex flex-col items-center justify-center h-full px-4">
            <motion.div
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 0.5 }}
              className="text-center mb-10"
            >
              <div className="w-16 h-16 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-2xl flex items-center justify-center mx-auto mb-4 shadow-lg shadow-indigo-200">
                <HiOutlineSparkles className="w-8 h-8 text-white" />
              </div>
              <h2 className="text-xl font-bold text-slate-800">How can I help you today?</h2>
              <p className="text-sm text-slate-500 mt-1">Choose a prompt or type your own message</p>
            </motion.div>

            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3 max-w-2xl w-full">
              {STARTERS.map((starter, idx) => (
                <motion.button
                  key={idx}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.1 * idx }}
                  whileHover={{ scale: 1.02, y: -2 }}
                  whileTap={{ scale: 0.98 }}
                  onClick={() => onSendMessage(starter.prompt)}
                  className="flex items-center gap-3 p-4 bg-white rounded-xl border border-slate-200 hover:border-indigo-200 hover:shadow-md hover:shadow-indigo-50 transition-all text-left"
                >
                  <starter.icon className="w-5 h-5 text-indigo-500 flex-shrink-0" />
                  <span className="text-sm text-slate-700">{starter.label}</span>
                </motion.button>
              ))}
            </div>
          </div>
        ) : (
          <div className="max-w-3xl mx-auto py-4">
            {messages.map((msg, idx) => (
              <MessageBubble key={msg.id || idx} message={msg} isLast={idx === messages.length - 1} />
            ))}
            {isStreaming && <StreamingMessage content={streamingMessage} />}
            {isStreaming && !streamingMessage && (
              <div className="flex gap-3 px-4 py-3">
                <div className="w-8 h-8 rounded-xl bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center">
                  <HiOutlineSparkles className="w-4 h-4 text-white" />
                </div>
                <div className="flex items-center gap-1 px-4 py-3 bg-white rounded-2xl border border-slate-100 shadow-sm">
                  {[0, 1, 2].map((i) => (
                    <motion.div
                      key={i}
                      className="w-1.5 h-1.5 bg-indigo-400 rounded-full"
                      animate={{ y: [0, -6, 0] }}
                      transition={{ duration: 0.6, repeat: Infinity, delay: i * 0.15 }}
                    />
                  ))}
                </div>
              </div>
            )}
            <div ref={bottomRef} />
          </div>
        )}
      </div>

      <ChatInput onSend={onSendMessage} />
    </div>
  );
}
