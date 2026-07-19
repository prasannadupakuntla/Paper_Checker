import { Menu, X, ScanLine, FlaskConical } from 'lucide-react';
import { useState } from 'react';
import { useActiveSection } from '../hooks/useActiveSection';
const links = [['problem', 'Problem'], ['process', 'How it works'], ['confidence', 'Confidence']];
export function Navbar({ onDemo, onLab }) {
    const [open, setOpen] = useState(false);
    const active = useActiveSection(['hero', ...links.map(x => x[0])]);
    return (
        <header className="nav-wrap">
            <nav className="nav">
                <a className="brand" href="#hero"><span className="brand-mark"><ScanLine size={15} /></span>Paper <i>Checker</i></a>
                <div className={'nav-links ' + (open ? 'show' : '')}>
                    {links.map(([id, label]) => (
                        <a key={id} className={active === id ? 'active' : ''} href={'#' + id} onClick={() => setOpen(false)}>{label}</a>
                    ))}
                    <button className="nav-lab" onClick={onLab}><FlaskConical size={14} /> Lab</button>
                    <button className="nav-cta" onClick={onDemo}>Try the demo <span>↗</span></button>
                </div>
                <button className="menu" onClick={() => setOpen(!open)} aria-label="Toggle menu">{open ? <X /> : <Menu />}</button>
            </nav>
        </header>
    );
}
