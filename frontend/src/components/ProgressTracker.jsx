/**
 * Progress Tracker Component
 *
 * Shows 7-step pipeline with current progress
 */
function ProgressTracker({ currentStep, steps, theme }) {
  const isDark = theme === 'dark';

  return (
    <div className="space-y-3">
      {steps.map((step) => (
        <div
          key={step.id}
          className={`
            flex items-center gap-4 transition-all duration-300
            ${step.id === currentStep ? 'opacity-100 scale-105' : ''}
            ${step.id < currentStep ? 'opacity-60' : ''}
            ${step.id > currentStep ? 'opacity-30' : ''}
          `}
        >
          <span className={`text-2xl ${step.id === currentStep ? 'animate-pulse' : ''}`}>
            {step.icon}
          </span>
          <span className="text-sm font-medium">{step.title}</span>
          {step.id < currentStep && (
            <span className="ml-auto text-verified">✓</span>
          )}
          {step.id === currentStep && (
            <span className="ml-auto">
              <div className={`w-2 h-2 rounded-full ${isDark ? 'bg-cyber-accent' : 'bg-clinical-accent'} animate-ping`} />
            </span>
          )}
        </div>
      ))}
    </div>
  );
}

export default ProgressTracker;
