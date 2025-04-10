import React, { useContext } from 'react';
import { TestCaseContext } from '../context/TestCaseContext';

const RightPanel = () => {
  const { resultUrl, loading } = useContext(TestCaseContext);

  return (
    <div className="w-2/3 flex flex-col h-full">
      {loading && (
        <div className="flex items-center justify-center flex-1">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500 mx-auto mb-4"></div>
            <p className="text-gray-600">Processing test case...</p>
          </div>
        </div>
      )}
      
      {!loading && !resultUrl && (
        <div className="flex items-center justify-center flex-1 bg-gray-50 text-gray-500">
          <div className="text-center p-8">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-12 w-12 mx-auto mb-4 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
            <h3 className="text-lg font-medium mb-2">No Test Results</h3>
            <p>Run a test case to see results here</p>
          </div>
        </div>
      )}
      
      {!loading && resultUrl && (
        <iframe
          src={resultUrl}
          className="w-full h-full bg-white"
          title="Test Results"
          sandbox="allow-same-origin allow-scripts"
        ></iframe>
      )}
    </div>
  );
};

export default RightPanel;