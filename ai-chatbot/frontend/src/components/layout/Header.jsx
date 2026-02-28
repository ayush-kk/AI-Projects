import { motion } from 'framer-motion';
import { HiOutlineBars3, HiOutlineArrowRightOnRectangle } from 'react-icons/hi2';
import { useAuth } from '../../context/AuthContext';
import { useChat } from '../../context/ChatContext';
import ModelSelector from '../controls/ModelSelector';
import SearchToggle from '../controls/SearchToggle';

export default function Header({ onMenuClick }) {
  const { user, logout } = useAuth();
  const { searchEnabled, toggleSearch } = useChat();

  return (
    <header className="h-14 flex items-center justify-between px-4 border-b border-slate-200 bg-white/80 backdrop-blur-lg flex-shrink-0">
      <div className="flex items-center gap-3">
        <button
          onClick={onMenuClick}
          className="p-1.5 rounded-lg hover:bg-slate-100 transition-colors md:hidden"
        >
          <HiOutlineBars3 className="w-5 h-5 text-slate-600" />
        </button>
        <span className="text-sm font-semibold text-slate-800 hidden sm:block">NexusAI</span>
      </div>

      <div className="flex items-center gap-3">
        <div className="hidden sm:block">
          <ModelSelector />
        </div>
        <SearchToggle enabled={searchEnabled} onToggle={toggleSearch} />
        <div className="flex items-center gap-2 pl-3 border-l border-slate-200">
          <div className="w-7 h-7 rounded-full bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center">
            <span className="text-xs font-medium text-white">
              {user?.username?.[0]?.toUpperCase() || 'U'}
            </span>
          </div>
          <span className="text-sm text-slate-600 hidden lg:block">{user?.username}</span>
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={logout}
            className="p-1.5 rounded-lg hover:bg-red-50 text-slate-400 hover:text-red-500 transition-colors"
            title="Logout"
          >
            <HiOutlineArrowRightOnRectangle className="w-4 h-4" />
          </motion.button>
        </div>
      </div>
    </header>
  );
}
