import { useState, useEffect } from 'react';
import { api } from '../services/api';

export const useTestCases = () => {
  const [testCases, setTestCases] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  // Fetch all test cases on mount
  useEffect(() => {
    fetchTestCases();
  }, []);
  
  // Fetch all test cases
  const fetchTestCases = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await api.getTestCases();
      setTestCases(data);
    } catch (err) {
      setError('Failed to fetch test cases');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };
  
  // Add a new test case
  const addTestCase = async (description, url) => {
    try {
      const newTestCase = await api.createTestCase(description, url);
      setTestCases(prev => [...prev, newTestCase]);
      return newTestCase;
    } catch (err) {
      throw new Error('Failed to add test case');
    }
  };
  
  // Run a test case
  const runTestCase = async (testCaseId) => {
    try {
      return await api.runTestCase(testCaseId);
    } catch (err) {
      throw new Error('Failed to run test case');
    }
  };
  
  return {
    testCases,
    loading,
    error,
    fetchTestCases,
    addTestCase,
    runTestCase
  };
};