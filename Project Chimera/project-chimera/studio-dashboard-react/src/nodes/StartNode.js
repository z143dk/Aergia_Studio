import React from 'react';
import { Handle, Position } from '@xyflow/react';

function StartNode({ data }) {
    return (
        <div style={{
            padding: '10px 20px',
            borderRadius: '50px',
            background: '#4CAF50',
            color: 'white',
            border: '2px solid #388E3C',
            boxShadow: '0 4px 6px rgba(0,0,0,0.1)',
            fontWeight: 'bold',
            textAlign: 'center',
            minWidth: '100px',
        }}>
            {data.label}

            {/* Source Handle at the bottom */}
            <Handle
                type="source"
                position={Position.Bottom}
                style={{
                    background: '#388E3C',
                    width: '12px',
                    height: '12px',
                    bottom: '-6px'
                }}
            />
        </div>
    );
}

export default StartNode;
