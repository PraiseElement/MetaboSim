import { useState, useCallback, useEffect } from 'react';
import { ThemeProvider } from './context/ThemeContext';
import Header from './components/Header';
import Dashboard from './components/Dashboard';
import SimulationPanel from './components/SimulationPanel';
import PathwayMap from './components/PathwayMap';
import MetricsPanel from './components/MetricsPanel';
import LearningPanel from './components/LearningPanel';
import QuizModule from './components/QuizModule';
import ClinicalModule from './components/ClinicalModule';
import GuideModule from './components/GuideModule';
import EnzymeModal from './components/EnzymeModal';
import { ErrorBoundary } from './components/ErrorBoundary';

// Backend root URL (same env var as api.js, but without /api suffix)
const BACKEND_ROOT = import.meta.env.VITE_API_URL || '';

export default function App() {
  const [activePage, setActivePage] = useState('dashboard');
  const [simulationResult, setSimulationResult] = useState(null);
  const [selectedPathway, setSelectedPathway] = useState('glycolysis');
  const [selectedEnzyme, setSelectedEnzyme] = useState(null);
  const [enzymeModal, setEnzymeModal] = useState(null); // enzyme clicked in PathwayMap
  const [isLoading, setIsLoading] = useState(false);

  // Silent wake-up ping — fires once on mount to warm the Render backend
  // after it has spun down due to inactivity. No UI impact; errors swallowed.
  useEffect(() => {
    fetch(`${BACKEND_ROOT}/`).catch(() => {});
  }, []);

  const handleSimulationResult = useCallback((result) => {
    setSimulationResult(result);
    setSelectedEnzyme(null);
  }, []);

  const handleEnzymeClick = useCallback((enzyme) => {
    setSelectedEnzyme(enzyme);
    setEnzymeModal(enzyme); // also open the detail modal
  }, []);

  return (
    <ThemeProvider>
      <div style={{ minHeight: '100vh', background: 'var(--bg-base)' }}>
        <Header activePage={activePage} onNavigate={setActivePage} />

        {activePage === 'dashboard' && (
          <Dashboard onNavigate={setActivePage} onSelectPathway={setSelectedPathway} />
        )}

        {activePage === 'simulate' && (
          <div className="main-layout">
            {/* Left: Simulation Controls */}
            <div className="scroll-col">
              <ErrorBoundary>
                <SimulationPanel
                  pathway={selectedPathway}
                  onPathwayChange={setSelectedPathway}
                  onResult={handleSimulationResult}
                  onLoading={setIsLoading}
                />
              </ErrorBoundary>
            </div>

            {/* Centre: Pathway Map */}
            <div style={{
              overflow: 'hidden',
              background: 'var(--bg-surface)',
              borderRadius: 'var(--radius-lg)',
              border: '1px solid var(--border)',
            }}>
              <ErrorBoundary>
                <PathwayMap
                  pathway={selectedPathway}
                  simulationResult={simulationResult}
                  isLoading={isLoading}
                  onEnzymeClick={handleEnzymeClick}
                />
              </ErrorBoundary>
            </div>

            {/* Right: Metrics + Learning */}
            <div className="scroll-col flex flex-col gap-4">
              <ErrorBoundary>
                <MetricsPanel
                  result={simulationResult}
                  pathway={selectedPathway}
                  isLoading={isLoading}
                />
              </ErrorBoundary>
              <ErrorBoundary>
                <LearningPanel enzyme={selectedEnzyme} result={simulationResult} />
              </ErrorBoundary>
            </div>
          </div>
        )}

        {activePage === 'clinical' && (
          <ClinicalModule onNavigate={setActivePage} />
        )}

        {activePage === 'quiz' && <QuizModule />}

        {activePage === 'guide' && <GuideModule />}

        {/* Enzyme detail modal — shown when an enzyme node is clicked */}
        <EnzymeModal
          enzymeState={enzymeModal}
          onClose={() => setEnzymeModal(null)}
        />
      </div>
    </ThemeProvider>
  );
}
