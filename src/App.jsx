import { useState } from 'react';
import { Navbar } from './components/Navbar';
import { DemoModal } from './components/DemoModal';
import { Lab } from './components/Lab';
import { Hero } from './sections/Hero';
import { Problem, Process, Confidence, Features } from './sections/ContentSections';
import { Finale } from './sections/Finale';

export default function App() {
    const [demoOpen, setDemoOpen] = useState(false);
    const [showLab, setShowLab] = useState(false);

    if (showLab) {
        return <Lab onBack={() => setShowLab(false)} />;
    }

    return (
        <>
            <div className="page-noise" />
            <Navbar onDemo={() => setDemoOpen(true)} onLab={() => setShowLab(true)} />
            <main>
                <Hero onDemo={() => setDemoOpen(true)} />
                <Problem />
                <Process />
                <Confidence />
                <Features />
                <Finale onDemo={() => setDemoOpen(true)} />
            </main>
            <DemoModal open={demoOpen} onClose={() => setDemoOpen(false)} />
        </>
    );
}
