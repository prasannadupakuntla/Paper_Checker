import { AnimatePresence, motion } from 'framer-motion';
import { X, Upload, BrainCircuit, FileBarChart, CheckCircle2, FileText, Sparkles } from 'lucide-react';
import { useRef, useState } from 'react';
import './demo-modal.css';
import './demo-enhancements.css';

const steps = [
  { label: 'Upload', icon: Upload },
  { label: 'Evaluate', icon: BrainCircuit },
  { label: 'Generate report', icon: FileBarChart }
];

export function DemoModal({ open, onClose }) {
  const inputRef = useRef(null);
  const [stage, setStage] = useState(0);
  const [fileName, setFileName] = useState('');
  const [evaluating, setEvaluating] = useState(false);

  const upload = () => inputRef.current?.click();
  const chooseFile = (event) => { const file = event.target.files?.[0]; if (file) { setFileName(file.name); setStage(1); } };
  const useSample = () => { setFileName('Sample biology answer sheet.jpg'); setStage(1); };
  const evaluate = () => { if (!fileName) return upload(); setEvaluating(true); window.setTimeout(() => { setEvaluating(false); setStage(2); }, 1050); };
  const report = () => { if (stage < 2) return evaluate(); setStage(3); };

  const actions = [upload, evaluate, report];
  return <AnimatePresence>{open && <motion.div className="demo-overlay" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} onMouseDown={onClose}>
    <motion.section className="demo-modal" initial={{ opacity: 0, y: 22, scale: .98 }} animate={{ opacity: 1, y: 0, scale: 1 }} exit={{ opacity: 0, y: 20, scale: .98 }} transition={{ type: 'spring', damping: 24, stiffness: 280 }} onMouseDown={(event) => event.stopPropagation()} role="dialog" aria-modal="true" aria-label="Paper Checker demo">
      <button className="demo-close" onClick={onClose} aria-label="Close demo"><X size={19}/></button>
      <div className="demo-heading"><span className="demo-kicker"><Sparkles size={12}/> LIVE PRODUCT DEMO</span><h2>See the confidence<br/><i>behind every mark.</i></h2><p>Upload one handwritten answer to preview the Paper Checker workflow.</p></div>
      <div className="demo-stepper">{steps.map(({ label, icon: Icon }, index) => <div className={stage >= index + 1 ? 'done' : stage === index ? 'current' : ''} key={label}><span>{stage >= index + 1 ? <CheckCircle2 size={16}/> : <Icon size={15}/>}</span><b>{label}</b>{index < 2 && <i/>}</div>)}</div>
      <div className="demo-workspace">
        {stage === 0 && <div className="upload-state"><div className="upload-icon"><Upload size={25}/></div><strong>Upload answer sheet</strong><p>PNG, JPG or PDF · Up to 10 MB</p><small>Your answer sheet is used only for this evaluation.</small></div>}
        {stage === 1 && <div className="ready-state"><div className="file-token"><FileText size={22}/><span>{fileName}</span><CheckCircle2 size={17}/></div><p>Image quality detected: <b>Excellent</b></p></div>}
        {stage === 2 && <div className="evaluate-state"><div className={evaluating ? 'eval-orb running' : 'eval-orb'}><BrainCircuit size={30}/></div><strong>{evaluating ? 'Evaluating your answer…' : 'Evaluation complete'}</strong><p>{evaluating ? 'Matching rubric, concepts and answer structure.' : 'Rubric matched · 8.5 / 10 marks suggested'}</p></div>}
        {stage === 3 && <div className="report-state"><div className="report-score"><span>OVERALL CONFIDENCE</span><strong>90<small>%</small></strong><b>High confidence</b></div><div className="report-feedback"><strong>8.5 <small>/ 10</small></strong><p><b>Missing concept:</b> Include the definition</p><p><b>Next step:</b> Add one example</p></div></div>}
      </div>
      <div className="demo-actions">{steps.map(({ label, icon: Icon }, index) => <button key={label} className={stage === index || (index === 0 && stage > 0) ? 'selected' : ''} onClick={actions[index]} disabled={evaluating}><Icon size={16}/>{index === 0 && fileName ? 'Change file' : label}</button>)}</div>
      {stage === 0 && <button className="sample-answer" onClick={useSample}><Sparkles size={14}/> Use sample answer instead</button>}
      <input ref={inputRef} className="file-input" type="file" accept="image/png,image/jpeg,application/pdf" onChange={chooseFile}/>
    </motion.section>
  </motion.div>}</AnimatePresence>;
}
