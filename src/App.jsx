import React, { useContext } from 'react';
import LeftPanel from './components/LeftPanel';
import RightPanel from './components/RightPanel';
import { TestCaseProvider } from './context/TestCaseContext';

function App() {
  return (
    <TestCaseProvider>
      <div className="flex flex-col h-screen bg-gray-100">
        <header className="bg-blue-700 text-white p-4 shadow-md">
          <h1 className="text-xl font-bold">UI Automation Testing Platform</h1>
        </header>
        <main className="flex flex-1 overflow-hidden">
          <LeftPanel />
          <RightPanel />
        </main>
      </div>
    </TestCaseProvider>
  );
}

export default App;