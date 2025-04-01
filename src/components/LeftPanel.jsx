import React from 'react';
import TestCaseForm from './TestCaseForm';
import TestCaseList from './TestCaseList';

const LeftPanel = () => {
  return (
    <div className="w-1/3 bg-white p-4 shadow-md overflow-y-auto flex flex-col h-full border-r border-gray-200">
      <div className="mb-4">
        <h2 className="text-lg font-semibold mb-2">Add Test Case</h2>
        <TestCaseForm />
      </div>
      <div className="flex-1 overflow-y-auto">
        <h2 className="text-lg font-semibold mb-2">Test Cases</h2>
        <TestCaseList />
      </div>
    </div>
  );
};

export default LeftPanel;