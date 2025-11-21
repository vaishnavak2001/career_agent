import React from 'react';
import Header from './components/Header';
import JobFeed from './components/JobFeed';
import Dashboard from './components/Dashboard';

function App() {
  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      <main>
        <Dashboard />
        <div className="flex max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 gap-6">
          <div className="flex-1">
            <JobFeed />
          </div>
          <div className="hidden lg:block w-80 py-8">
            {/* Sidebar for filters or extra info */}
            <div className="bg-white shadow rounded-lg p-4 sticky top-24">
              <h3 className="font-bold text-gray-900 mb-4">Filters</h3>
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700">Location</label>
                  <input type="text" className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary focus:ring-primary sm:text-sm border p-2" placeholder="City, state, zip" />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700">Job Type</label>
                  <select className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary focus:ring-primary sm:text-sm border p-2">
                    <option>Full-time</option>
                    <option>Contract</option>
                    <option>Part-time</option>
                  </select>
                </div>
                <div>
                  <label className="flex items-center">
                    <input type="checkbox" className="rounded border-gray-300 text-primary focus:ring-primary" />
                    <span className="ml-2 text-sm text-gray-600">Remote Only</span>
                  </label>
                </div>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;
