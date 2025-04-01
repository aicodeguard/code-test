import React, { useState, useContext } from 'react';
import Button from './Button';
import { TestCaseContext } from '../context/TestCaseContext';

const TestCaseForm = () => {
  const [description, setDescription] = useState('');
  const [url, setUrl] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState(null);
  
  const { addTestCase } = useContext(TestCaseContext);
  
  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    
    if (!description.trim() || !url.trim()) {
      setError('Please fill in all fields');
      return;
    }
    
    if (!url.startsWith('http://') && !url.startsWith('https://')) {
      setError('URL must start with http:// or https://');
      return;
    }
    
    try {
      setIsSubmitting(true);
      await addTestCase(description, url);
      setDescription('');
      setUrl('');
    } catch (err) {
      setError(err.message || 'Failed to add test case');
    } finally {
      setIsSubmitting(false);
    }
  };
  
  return (
    <form onSubmit={handleSubmit} className="space-y-4 bg-gray-50 p-4 rounded-lg">
      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-2 rounded-md">
          {error}
        </div>
      )}
      
      <div>
        <label htmlFor="description" className="block text-sm font-medium text-gray-700 mb-1">
          Test Case Description
        </label>
        <input
          id="description"
          type="text"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          className="w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          placeholder="Enter test case description"
          disabled={isSubmitting}
        />
      </div>
      
      <div>
        <label htmlFor="url" className="block text-sm font-medium text-gray-700 mb-1">
          Test URL
        </label>
        <input
          id="url"
          type="text"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          className="w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          placeholder="https://example.com"
          disabled={isSubmitting}
        />
      </div>
      
      <Button
        type="submit"
        disabled={isSubmitting}
        className="w-full"
      >
        {isSubmitting ? 'Adding...' : 'Add Test Case'}
      </Button>
    </form>
  );
};

export default TestCaseForm;