import React, { useState } from 'react';
import { CheckCircle, Circle, ChevronRight } from 'lucide-react';
import './WizardLayout.css';

const steps = [
    { id: 1, title: 'System Check' },
    { id: 2, title: 'Configuration' },
    { id: 3, title: 'Summary' },
    { id: 4, title: 'Training' },
    { id: 5, title: 'Results' }
];

const WizardLayout = ({ children, currentStep, onStepChange }) => {
    return (
        <div className="wizard-container">
            <header className="wizard-header">
                <h1 className="app-title">LLM Finetuner Studio</h1>
                <div className="steps-indicator">
                    {steps.map((step, index) => (
                        <div key={step.id} className={`step-item ${currentStep >= step.id ? 'active' : ''}`}>
                            <div className="step-icon">
                                {currentStep > step.id ? <CheckCircle size={20} /> : <Circle size={20} />}
                            </div>
                            <span className="step-title">{step.title}</span>
                            {index < steps.length - 1 && <div className="step-line" />}
                        </div>
                    ))}
                </div>
            </header>
            <main className="wizard-content">
                {children}
            </main>
        </div>
    );
};

export default WizardLayout;
