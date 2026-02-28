import { motion } from 'framer-motion';
import { HiOutlineGlobeAlt } from 'react-icons/hi2';

export default function SearchToggle({ enabled, onToggle }) {
  return (
    <button
      onClick={onToggle}
      className={`flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg text-xs font-medium transition-all ${
        enabled
          ? 'bg-emerald-50 text-emerald-700 border border-emerald-200'
          : 'bg-slate-50 text-slate-400 border border-slate-200 hover:text-slate-500'
      }`}
      title={enabled ? 'Web search enabled' : 'Web search disabled'}
    >
      <HiOutlineGlobeAlt className="w-3.5 h-3.5" />
      <span className="hidden sm:inline">Web</span>
      <motion.div
        className={`w-6 h-3.5 rounded-full relative ${enabled ? 'bg-emerald-500' : 'bg-slate-300'}`}
      >
        <motion.div
          className="w-2.5 h-2.5 bg-white rounded-full absolute top-0.5"
          animate={{ left: enabled ? 12 : 2 }}
          transition={{ type: 'spring', stiffness: 500, damping: 30 }}
        />
      </motion.div>
    </button>
  );
}
