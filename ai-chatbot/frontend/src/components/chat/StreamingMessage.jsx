import { motion } from 'framer-motion';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import CodeBlock from './CodeBlock';
import { HiOutlineSparkles } from 'react-icons/hi2';

export default function StreamingMessage({ content }) {
  if (!content) return null;

  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      className="flex gap-3 px-4 py-3 justify-start"
    >
      <div className="flex-shrink-0 w-8 h-8 rounded-xl bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center mt-1">
        <HiOutlineSparkles className="w-4 h-4 text-white" />
      </div>

      <div className="max-w-[80%] md:max-w-[70%] rounded-2xl px-4 py-3 bg-white border border-slate-100 text-slate-800 shadow-sm">
        <div className="prose prose-sm prose-slate max-w-none prose-pre:p-0 prose-pre:bg-transparent">
          <ReactMarkdown
            remarkPlugins={[remarkGfm]}
            components={{
              code({ node, inline, className, children, ...props }) {
                const match = /language-(\w+)/.exec(className || '');
                if (!inline && match) {
                  return (
                    <CodeBlock language={match[1]}>
                      {String(children).replace(/\n$/, '')}
                    </CodeBlock>
                  );
                }
                return (
                  <code className="px-1.5 py-0.5 rounded-md bg-slate-100 text-indigo-600 text-xs font-mono" {...props}>
                    {children}
                  </code>
                );
              },
            }}
          >
            {content}
          </ReactMarkdown>
        </div>
        <motion.span
          className="inline-block w-1.5 h-4 bg-indigo-500 rounded-full ml-0.5 align-middle"
          animate={{ opacity: [1, 0] }}
          transition={{ duration: 0.5, repeat: Infinity }}
        />
      </div>
    </motion.div>
  );
}
