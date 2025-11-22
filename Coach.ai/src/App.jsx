import React, { useState } from 'react';
import WizardLayout from './components/WizardLayout';
import SystemCheck from './components/SystemCheck';
import Configuration from './components/Configuration';
import Summary from './components/Summary';
import Training from './components/Training';
import Results from './components/Results';

function App() {
  const [currentStep, setCurrentStep] = useState(1);
  const [config, setConfig] = useState({
    model: 'Mistral 7B',
    dataset: null,
    batchSize: 1, // Safe default
    learningRate: 0.0001,
    epochs: 1,
    gradientAccumulation: 4,
    quantization: '4-bit', // Safe default
    maxSeqLength: 256
  });

  const nextStep = () => setCurrentStep(prev => Math.min(prev + 1, 5));
  const prevStep = () => setCurrentStep(prev => Math.max(prev - 1, 1));

  const handleSystemCheckComplete = (sysInfo) => {
    // Store presets if available
    if (sysInfo.presets) {
      const balanced = sysInfo.presets.balanced;
      setConfig(prev => ({
        ...prev,
        presets: sysInfo.presets, // Store all presets
        batchSize: balanced.batch_size,
        epochs: balanced.num_epochs,
        gradientAccumulation: balanced.gradient_accumulation,
        maxSeqLength: balanced.max_seq_length,
        learningRate: balanced.learning_rate,
        framework: sysInfo.framework,
        isOptimized: true,
        optimizationReason: sysInfo.reason
      }));
    } else {
      // Fallback logic (if backend doesn't send presets)
      // ... existing logic ...
    }

    nextStep();
  };

  const renderStep = () => {
    switch (currentStep) {
      case 1: return <SystemCheck onNext={handleSystemCheckComplete} />;
      case 2: return <Configuration config={config} setConfig={setConfig} onNext={nextStep} onPrev={prevStep} />;
      case 3: return <Summary config={config} onNext={nextStep} onPrev={prevStep} />;
      case 4: return <Training onNext={nextStep} />;
      case 5: return <Results onRestart={() => setCurrentStep(1)} />;
      default: return <SystemCheck onNext={handleSystemCheckComplete} />;
    }
  };

  return (
    <WizardLayout currentStep={currentStep}>
      {renderStep()}
    </WizardLayout>
  );
}

export default App;
