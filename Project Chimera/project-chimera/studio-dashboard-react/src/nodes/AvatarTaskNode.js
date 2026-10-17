import React, { useCallback } from 'react';
import { Handle, Position } from '@xyflow/react';

function AvatarTaskNode({ id, data, onDataChange, onDelete }) {

  const onPromptChange = useCallback((evt) => {
    if (onDataChange) {
      onDataChange(id, { prompt: evt.target.value });
    }
  }, [id, onDataChange]);

  // --- NEW: This now passes the actual file object to the state ---
  const onFileChange = useCallback((evt) => {
    if (evt.target.files && evt.target.files[0]) {
      const file = evt.target.files[0];
      if (onDataChange) {
        // Store the file object itself and the name for display
        onDataChange(id, { avatarFile: file, avatarFileName: file.name });
      }
    }
  }, [id, onDataChange]);

  return (
    <div style={{
      border: '1px solid #1a73e8', padding: '15px', borderRadius: '8px',
      background: '#e8f0fe', minWidth: '250px', textAlign: 'left',
      boxShadow: '0 2px 5px rgba(0,0,0,0.1)', position: 'relative',
    }}>
      <button
        onClick={() => onDelete(id)}
        style={{
          position: 'absolute', top: '5px', right: '5px', width: '20px',
          height: '20px', border: '1px solid #ccc', borderRadius: '50%',
          background: '#fff', color: '#555', cursor: 'pointer', display: 'flex',
          alignItems: 'center', justifyContent: 'center', lineHeight: '1', fontSize: '14px',
        }}
        title="Delete Node"
      >×</button>

      <Handle type="target" position={Position.Top} />

      <div><strong>{data.label}</strong></div>
      <hr style={{ margin: '10px 0', borderColor: '#d2e3fc' }} />

      <label style={{ display: 'block', marginBottom: '5px', color: '#333', fontSize: '12px' }}>
        Voiceover Script:
      </label>
      <textarea
        onChange={onPromptChange} rows={3}
        style={{ width: '100%', boxSizing: 'border-box', padding: '8px', borderRadius: '4px', border: '1px solid #ccc', fontSize: '14px' }}
        value={data.prompt}
        placeholder="Enter the script for the avatar..."
      />

      <label style={{ display: 'block', marginTop: '10px', marginBottom: '5px', color: '#333', fontSize: '12px' }}>
        <input
          type="checkbox"
          checked={data.useNewsCaster || false}
          onChange={(e) => onDataChange(id, { useNewsCaster: e.target.checked })}
        /> Use News Caster Avatar
      </label>

      {!data.useNewsCaster && (
        <>
          <label style={{ display: 'block', marginTop: '5px', marginBottom: '5px', color: '#333', fontSize: '12px' }}>
            Avatar Image:
          </label>
          <input
            type="file"
            onChange={onFileChange}
            accept="image/png, image/jpeg"
            style={{ width: '100%' }}
          />
          {/* Display the filename from the state */}
          {data.avatarFileName && <p style={{ fontSize: '12px', color: '#555', margin: '5px 0 0 0' }}>File: {data.avatarFileName}</p>}
        </>
      )}

      <Handle type="source" position={Position.Bottom} />
    </div>
  );
}

export default AvatarTaskNode;
