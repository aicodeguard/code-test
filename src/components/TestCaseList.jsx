import React, { useContext } from 'react';
import TestCase from './TestCase';
import { TestCaseContext } from '../context/TestCaseContext';

const TestCaseList = () => {
  const { testCases, fetchingTestCases } = useContext(TestCaseContext);
  
  if (fetchingTestCases) {
    return (
      <div className="flex items-center justify-center p-8">
        <div className="animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-blue-500"></div>
      </div>
    );
  }
  
  if (testCases.length === 0) {
    return (
      <div className="text-center p-8 bg-gray-50 rounded-lg">
        <p className="text-gray-500">No test cases added yet</p>
      </div>
    );
  }
  
  return (
    <div className="space-y-4">
      {testCases.map((testCase) => (
        <TestCase key={testCase.id} testCase={testCase} />
      ))}
    </div>
  );
};

export default TestCaseList;