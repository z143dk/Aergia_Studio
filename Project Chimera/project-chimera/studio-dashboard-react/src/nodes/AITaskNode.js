import React, { useCallback } from 'react';
import { Handle, Position } from '@xyflow/react';

// The component now receives an `onDelete` callback function from the dashboard
function AITaskNode({ id, data, onDataChange, onDelete }) {

  const onPromptChange = useCallback((evt) => {
    if (onDataChange) {
        onDataChange(id, { prompt: evt.target.value });
    }
  }, [id, onDataChange]);

  return (
    <div style={{
      border: '1px solid #777',
      padding: '15px',
      borderRadius: '8px',
      background: '#fff',
      minWidth: '200px',
      textAlign: 'left',
      boxShadow: '0 2px 5px rgba(0,0,0,0.1)',
      position: 'relative', // This is required to position the delete button
    }}>
      {/* --- NEW: Delete Button --- */}
      <button 
        onClick={() => onDelete(id)}
        style={{
            position: 'absolute',
            top: '5px',
            right: '5px',
            width: '20px',
            height: '20px',
            border: '1px solid #ccc',
            borderRadius: '50%',
            background: '#f0f0f0',
            color: '#555',
            cursor: 'pointer',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            lineHeight: '1',
            fontSize: '14px',
        }}
        title="Delete Node"
      >
        ×
      </button>

      {/* Input handle on the top of the node */}
      <Handle type="target" position={Position.Top} />
      
      <div>
        <strong>{data.label}</strong>
      </div>
      
      <hr style={{ margin: '10px 0', borderColor: '#eee' }} />

      <label htmlFor="text" style={{ display: 'block', marginBottom: '5px', color: '#555', fontSize: '12px' }}>
        Prompt:
      </label>
      <textarea 
        id="text" 
        name="text" 
        onChange={onPromptChange} 
        rows={4}
        style={{ 
          width: '100%', 
          boxSizing: 'border-box', 
          padding: '8px', 
          borderRadius: '4px', 
          border: '1px solid #ccc',
          fontSize: '14px'
        }}
        value={data.prompt}
        placeholder="Enter instructions..."
      />

      {/* Output handle on the bottom of the node */}
      <Handle type="source" position={Position.Bottom} id="a" />
    </div>
  );
}

export default AITaskNode;
