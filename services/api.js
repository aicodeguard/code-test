// API service for UI automation testing platform

const API_BASE_URL = import.meta.env.REACT_APP_API_BASE_URL || 'http://localhost:10010/api';

const defaultHeaders = {
  'Content-Type': 'application/json'
};

export const api = {
  // Fetch all test cases
  async getTestCases() {
    const response = await fetch(`${API_BASE_URL}/test-cases`, {
      headers: defaultHeaders
    });
    if (!response.ok) {
      throw new Error('Failed to fetch test cases');
    }
    const { data: { test_cases } } = await response.json();
    return test_cases;
  },
  
  // Create a new test case
  async createTestCase(description, url) {
    const response = await fetch(`${API_BASE_URL}/test-cases/create`, {
      method: 'POST',
      headers: defaultHeaders,
      body: JSON.stringify({
        description,
        url,
        createdAt: new Date().toISOString(),
      }),
    });

    if (!response.ok) {
      throw new Error('Failed to create test case');
    }
    const { data } = await response.json();
    return data;
  },
  
  // Save test case steps
  async saveTestSteps(testCaseId, steps) {
    const response = await fetch(`${API_BASE_URL}/test-cases/${testCaseId}/steps`, {
      method: 'POST',
      headers: defaultHeaders,
      body: JSON.stringify({ steps }),
    });

    if (!response.ok) {
      throw new Error('Failed to save test steps');
    }
    return response.json();
  },
  
  // Generate test steps based on description and URL
  async generateTestSteps(description, url) {
    const response = await fetch(`${API_BASE_URL}/test-cases/generate-steps`, {
      method: 'POST',
      headers: defaultHeaders,
      body: JSON.stringify({ description, url }),
    });

    if (!response.ok) {
      throw new Error('Failed to generate test steps');
    }
    return response.json();
  },
  
  // Run a test case and get results
  async runTestCase(testCaseId) {
    const response = await fetch(`${API_BASE_URL}/test-cases/${testCaseId}/run`, {
      method: 'POST',
      headers: defaultHeaders,
    });

    if (!response.ok) {
      throw new Error('Failed to run test case');
    }
    return response.json();
  }
};