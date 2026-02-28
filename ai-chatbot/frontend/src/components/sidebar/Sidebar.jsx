import { useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  HiOutlinePlusCircle,
  HiOutlineChatBubbleLeftRight,
  HiOutlineTrash,
  HiOutlineXMark,
} from 'react-icons/hi2';
import { useChat } from '../../context/ChatContext';
import { formatRelative, truncate } from '../../utils/formatters';

export default function Sidebar({ onClose }) {
  const {
    conversations,
    currentConversation,
    loadConversations,
    selectConversation,
    createNewConversation,
    removeConversation,
  } = useChat();

  useEffect(() => {
    loadConversations();
  }, [loadConversations]);

  const handleNew = async () => {
    await createNewConversation();
    onClose?.();
  };

  const handleSelect = async (id) => {
    await selectConversation(id);
    onClose?.();
  };

  return (
    <div className="flex flex-col h-full bg-slate-900 text-white">
      <div className="flex items-center justify-between p-4 border-b border-slate-700/50">
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-lg flex items-center justify-center">
            <HiOutlineChatBubbleLeftRight className="w-4 h-4" />
          </div>
          <span className="font-semibold text-sm">NexusAI</span>
        </div>
        {onClose && (
          <button onClick={onClose} className="p-1 rounded-lg hover:bg-slate-800 transition-colors">
            <HiOutlineXMark className="w-5 h-5" />
          </button>
        )}
      </div>

      <div className="p-3">
        <motion.button
          whileHover={{ scale: 1.01 }}
          whileTap={{ scale: 0.99 }}
          onClick={handleNew}
          className="w-full flex items-center gap-2 px-3 py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-700 transition-colors text-sm font-medium"
        >
          <HiOutlinePlusCircle className="w-5 h-5" />
          New Chat
        </motion.button>
      </div>

      <div className="flex-1 overflow-y-auto px-3 pb-3 space-y-1">
        <AnimatePresence>
          {conversations.map((conv) => (
            <motion.div
              key={conv.id}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -20 }}
              className={`group flex items-center gap-2 px-3 py-2.5 rounded-xl cursor-pointer transition-colors ${
                currentConversation?.id === conv.id
                  ? 'bg-slate-700/80 text-white'
                  : 'text-slate-300 hover:bg-slate-800 hover:text-white'
              }`}
              onClick={() => handleSelect(conv.id)}
            >
              <HiOutlineChatBubbleLeftRight className="w-4 h-4 flex-shrink-0 opacity-50" />
              <div className="flex-1 min-w-0">
                <p className="text-sm truncate">{truncate(conv.title, 30)}</p>
                <p className="text-xs text-slate-500">{formatRelative(conv.updated_at)}</p>
              </div>
              <button
                onClick={(e) => {
                  e.stopPropagation();
                  removeConversation(conv.id);
                }}
                className="opacity-0 group-hover:opacity-100 p-1 rounded hover:bg-slate-600 transition-all"
              >
                <HiOutlineTrash className="w-3.5 h-3.5 text-slate-400" />
              </button>
            </motion.div>
          ))}
        </AnimatePresence>

        {conversations.length === 0 && (
          <div className="text-center py-8">
            <p className="text-sm text-slate-500">No conversations yet</p>
            <p className="text-xs text-slate-600 mt-1">Start a new chat to begin</p>
          </div>
        )}
      </div>
    </div>
  );
}
