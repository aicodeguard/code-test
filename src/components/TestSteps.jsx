import React, { useState } from 'react';

const TestSteps = ({ steps, onStepsChange }) => {
  const [editedSteps, setEditedSteps] = useState(steps);
  const [isEdited, setIsEdited] = useState(false);

  const handleDescriptionChange = (index, newDescription) => {
    const newSteps = editedSteps.map((step, i) => 
      i === index ? { ...step, description: newDescription } : step
    );
    setEditedSteps(newSteps);
    setIsEdited(true);
    onStepsChange?.(newSteps, true);
  };
  const handleAddStep = () => {
    const newStep = { description: '', action: '' };
    const newSteps = [...editedSteps, newStep];
    setEditedSteps(newSteps);
    setIsEdited(true);
    onStepsChange?.(newSteps, true);
  };

  if (!steps || steps.length === 0) {
    return (
      <div className="text-center">
        <p className="text-sm text-gray-500 mb-2">No steps available</p>
        <button
          onClick={handleAddStep}
          className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 transition-colors"
        >
          Add Step
        </button>
      </div>
    );
  }
  
  return (
    <div>
      <ol className="space-y-2 text-sm list-none mb-4">
        {editedSteps.map((step, index) => (
          <li key={index} className="p-2 bg-white rounded border border-gray-200 relative">
            <div className="flex items-center gap-2">
              <input
                type="text"
                className="text-gray-700 flex-1 bg-transparent border-none focus:ring-2 focus:ring-blue-500 rounded px-1 min-h-[2.5rem]"
                value={step.description}
                onChange={(e) => handleDescriptionChange(index, e.target.value)}
              />
              {step.action && (
                <span className="text-xs text-green-600 bg-green-50 px-2 py-0.5 rounded inline-flex items-center whitespace-nowrap">
                  Action: {step.action}
                </span>
              )}
            </div>
          </li>
        ))}
      </ol>
      <div className="text-center">
        <button
          onClick={handleAddStep}
          className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 transition-colors"
        >
          Add Step
        </button>
      </div>
    </div>
  );
};

export default TestSteps;