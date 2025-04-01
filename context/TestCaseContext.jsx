import React, { createContext, useState, useEffect } from 'react';
import { api } from '../services/api';

// Create context
export const TestCaseContext = createContext(null);

export const TestCaseProvider = ({ children }) => {
  const [testCases, setTestCases] = useState([]);
  const [fetchingTestCases, setFetchingTestCases] = useState(true);
  const [loading, setLoading] = useState(false);
  const [resultUrl, setResultUrl] = useState(null);
  const [error, setError] = useState(null);
  
  // Fetch test cases on mount
  useEffect(() => {
    fetchTestCases();
  }, []);
  
  const fetchTestCases = async () => {
    try {
      setFetchingTestCases(true);
      const data = await api.getTestCases();
      setTestCases(data);
    } catch (err) {
      console.error('Failed to fetch test cases:', err);
      setError('Failed to fetch test cases');
    } finally {
      setFetchingTestCases(false);
    }
  };
  
  const addTestCase = async (description, url) => {
    try {
      setLoading(true);
      const newTestCase = await api.createTestCase(description, url);
      setTestCases(prev => [...prev, newTestCase]);
      return newTestCase;
    } catch (err) {
      throw new Error('Failed to add test case');
    } finally {
      setLoading(false);
    }
  };
  
  const runTestCase = async (testCaseId) => {
    try {
      setLoading(true);
      setResultUrl(null);
      
      // Find the test case
      const testCase = testCases.find(tc => tc.id === testCaseId);
      if (!testCase) {
        throw new Error('Test case not found');
      }
      
      // Run the test case
      const result = await api.runTestCase(testCaseId);
      
      // Update the result URL to display in iframe
      setResultUrl(result.resultUrl);
      return result;
    } catch (err) {
      console.error('Failed to run test case:', err);
      setError('Failed to run test case');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const showResultPanel =  (resultUrl) => {
    try {
      setLoading(true);
      setResultUrl(resultUrl);
      return true;
    } catch (err) {
      console.error('Failed to run test case:', err);
      setError('Failed to run test case');
      throw err;
    } finally {
      setLoading(false);
    }
  };
  
  return (
    <TestCaseContext.Provider value={{
        testCases,
        fetchingTestCases,
        loading,
        resultUrl,
        error,
        fetchTestCases,
        addTestCase,
        runTestCase,
        showResultPanel,
      }}
    >
      {children}
    </TestCaseContext.Provider>
  );
};