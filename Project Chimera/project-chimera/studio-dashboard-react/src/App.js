import React from 'react';
import { ReactFlowProvider } from '@xyflow/react';
import Dashboard from './Dashboard';

// Import necessary styles
import './index.css'; 
import '@xyflow/react/dist/style.css'; // Required for React Flow to display correctly

function App() {
  return (
    // The ReactFlowProvider is necessary for the node-based UI to function.
    <ReactFlowProvider>
      <div className="App">
        {/* This renders your main dashboard component. */}
        <Dashboard />
      </div>
    </ReactFlowProvider>
  );
}

export default App;
