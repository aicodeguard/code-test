// Mock data utility for UI automation testing platform
// This provides mock data for the application

// Generate mock test steps based on description and URL
export const getMockTestSteps = (description, url) => {
  const baseSteps = [
    {
      description: "Navigate to the specified URL",
      action: "navigate",
      selector: null,
      value: url
    },
    {
      description: "Wait for page to load",
      action: "wait",
      selector: "body",
      value: 2000
    }
  ];
  
  // Additional steps based on the description
  let additionalSteps = [];
  
  if (description.toLowerCase().includes('login')) {
    additionalSteps = [
      {
        description: "Enter username",
        action: "type",
        selector: "input[type='email'], input[name='username'], input[id='username']",
        value: "testuser@example.com"
      },
      {
        description: "Enter password",
        action: "type",
        selector: "input[type='password']",
        value: "securepassword"
      },
      {
        description: "Click login button",
        action: "click",
        selector: "button[type='submit'], input[type='submit'], .login-btn, .btn-login",
        value: null
      },
      {
        description: "Verify successful login",
        action: "assert",
        selector: ".dashboard, .account-info, .user-profile",
        value: "exists"
      }
    ];
  } else if (description.toLowerCase().includes('search')) {
    additionalSteps = [
      {
        description: "Enter search query",
        action: "type",
        selector: "input[type='search'], input[name='q'], .search-input",
        value: "test query"
      },
      {
        description: "Submit search query",
        action: "click",
        selector: "button[type='submit'], .search-button",
        value: null
      },
      {
        description: "Wait for search results",
        action: "wait",
        selector: ".search-results, .results-container",
        value: 3000
      },
      {
        description: "Verify search results are displayed",
        action: "assert",
        selector: ".search-result-item, .result-card",
        value: "exists"
      }
    ];
  } else if (description.toLowerCase().includes('form')) {
    additionalSteps = [
      {
        description: "Fill in form field 1",
        action: "type",
        selector: "input[name='field1']",
        value: "Sample text 1"
      },
      {
        description: "Fill in form field 2",
        action: "type",
        selector: "input[name='field2']",
        value: "Sample text 2"
      },
      {
        description: "Select dropdown option",
        action: "select",
        selector: "select",
        value: "Option 1"
      },
      {
        description: "Check checkbox",
        action: "click",
        selector: "input[type='checkbox']",
        value: null
      },
      {
        description: "Submit form",
        action: "click",
        selector: "button[type='submit']",
        value: null
      },
      {
        description: "Verify submission success message",
        action: "assert",
        selector: ".success-message, .alert-success",
        value: "exists"
      }
    ];
  } else {
    additionalSteps = [
      {
        description: "Capture screenshot",
        action: "screenshot",
        selector: null,
        value: "page"
      },
      {
        description: "Check main content exists",
        action: "assert",
        selector: "main, .content, #content",
        value: "exists"
      },
      {
        description: "Check page title",
        action: "assert",
        selector: "title",
        value: "contains:title"
      }
    ];
  }
  
  return [...baseSteps, ...additionalSteps];
};

// Generate mock test cases
export const getMockTestCases = () => {
  return [
    {
      id: "tc-1",
      description: "Login Test Case",
      url: "https://example.com/login",
      createdAt: "2023-03-20T10:30:00.000Z",
      yaml_path: "",
      result_url: "",
      status: "pass",
      steps: getMockTestSteps("Login Test Case", "https://example.com/login")
    },
    {
      id: "tc-2",
      description: "Search Functionality",
      url: "https://example.com/search",
      createdAt: "2023-03-21T14:45:00.000Z",
      steps: getMockTestSteps("Search Functionality", "https://example.com/search")
    },
    {
      id: "tc-3",
      description: "Contact Form Submission",
      url: "https://example.com/contact",
      createdAt: "2023-03-22T09:15:00.000Z",
      steps: getMockTestSteps("Contact Form Submission", "https://example.com/contact")
    }
  ];
};