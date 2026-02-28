import { useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { motion, AnimatePresence } from 'framer-motion';
import { HiOutlinePaperClip, HiOutlineXMark } from 'react-icons/hi2';

export default function FileUpload({ files, onUpload, onRemove, uploading }) {
  const onDrop = useCallback(
    (acceptedFiles) => {
      onUpload(acceptedFiles);
    },
    [onUpload]
  );

  const { getRootProps, getInputProps, isDragActive, open } = useDropzone({
    onDrop,
    noClick: true,
    noKeyboard: true,
  });

  return (
    <div {...getRootProps()} className="relative">
      <input {...getInputProps()} />

      {isDragActive && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          className="absolute inset-0 -top-32 bg-indigo-50/90 border-2 border-dashed border-indigo-300 rounded-xl flex items-center justify-center z-10"
        >
          <p className="text-indigo-600 font-medium text-sm">Drop files here</p>
        </motion.div>
      )}

      <button
        type="button"
        onClick={open}
        disabled={uploading}
        className="p-2 rounded-xl bg-slate-100 text-slate-500 hover:bg-slate-200 hover:text-slate-700 transition-all disabled:opacity-50"
        title="Attach file"
      >
        <HiOutlinePaperClip className="w-5 h-5" />
      </button>

      {files.length > 0 && (
        <div className="absolute bottom-full mb-2 left-0 right-0 space-y-1">
          <AnimatePresence>
            {files.map((file, idx) => (
              <motion.div
                key={idx}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: 10 }}
                className="flex items-center gap-2 px-2.5 py-1.5 bg-indigo-50 rounded-lg text-xs text-indigo-700"
              >
                <span className="truncate flex-1">{file.filename}</span>
                {onRemove && (
                  <button onClick={() => onRemove(idx)} className="hover:text-red-500 transition-colors">
                    <HiOutlineXMark className="w-3.5 h-3.5" />
                  </button>
                )}
              </motion.div>
            ))}
          </AnimatePresence>
        </div>
      )}
    </div>
  );
}
