import React, { useState, useContext } from 'react';
import TestSteps from './TestSteps';
import Button from './Button';
import { TestCaseContext } from '../context/TestCaseContext';
import { api } from '../services/api';
const TestCase = ({ testCase }) => {
  const [expanded, setExpanded] = useState(false);
  const {runTestCase, showResultPanel} = useContext(TestCaseContext);
  const [isRunning, setIsRunning] = useState(false);
  const [isEdited, setIsEdited] = useState(false);
  const [editedSteps, setEditedSteps] = useState(testCase.steps);
  
  const handleSave = async () => {
    try {
      await api.saveTestSteps(testCase.id, editedSteps);
      testCase.steps = editedSteps;
      setIsEdited(false);
    } catch (error) {
      console.error('Failed to save test steps:', error);
      // TODO: Add proper error handling UI feedback
    }
  };

  const handleStepsChange = (newSteps, edited) => {
    setEditedSteps(newSteps);
    setIsEdited(edited);
  };

  const handleRun = async () => {
    try {
      setIsRunning(true);
      await runTestCase(testCase.id);
    } finally {
      setIsRunning(false);
    }
  };

  const handleExpand = () => {
    setExpanded(!expanded);
    showResultPanel(testCase.result_url);
  }
  
  return (
    <div className="border border-gray-200 rounded-lg overflow-hidden bg-white">
      <div className="p-4 flex items-center justify-between bg-white">
        <div className="flex-1">
          <h3 className="font-medium text-blue-700 truncate">{testCase.description}</h3>
          <p className="text-sm text-gray-500 truncate">{testCase.url}</p>
        </div>
        <div className="flex space-x-2 ml-4">
          <Button
            onClick={handleSave}
            className="bg-blue-600 hover:bg-blue-700"
            disabled={!isEdited}
          >
            Save
          </Button>
          <Button
            onClick={handleRun}
            className="bg-green-600 hover:bg-green-700"
            disabled={isRunning}
          >
            {isRunning ? 'Running...' : 'Run'}
          </Button>
          <Button
            onClick={handleExpand}
            className="bg-gray-200 hover:bg-gray-300 text-gray-800"
          >
            {expanded ? 'Hide Steps' : 'Show Steps'}
          </Button>
        </div>
      </div>
      
      {expanded && (
        <div className="border-t border-gray-200 p-4 bg-gray-50">
          <h4 className="text-sm font-medium mb-2">Test Steps</h4>
          <TestSteps steps={editedSteps} onStepsChange={handleStepsChange} />
        </div>
      )}
    </div>
  );
};

export default TestCase;