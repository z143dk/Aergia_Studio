import React from 'react';

const Sidebar = () => {
  const onDragStart = (event, nodeType, label) => {
    event.dataTransfer.setData('application/reactflow', nodeType);
    event.dataTransfer.setData('application/label', label);
    event.dataTransfer.effectAllowed = 'move';
  };

  return (
    <aside className="sidebar">
      <h3>AI Filters</h3>
      <div
        className="sidebar-node"
        onDragStart={(event) => onDragStart(event, 'aiTaskNode', 'Gemini: Analyze Script')}
        draggable
      >
        Gemini: Analyze Script
      </div>
      <div
        className="sidebar-node"
        onDragStart={(event) => onDragStart(event, 'aiTaskNode', 'Veo: Generate Video')}
        draggable
      >
        Veo: Generate Video
      </div>
       <div
        className="sidebar-node"
        onDragStart={(event) => onDragStart(event, 'aiTaskNode', 'Genie: Create World')}
        draggable
      >
        Genie: Create World
      </div>
      {/* --- NEW: MultiTalk Avatar Node --- */}
      <div
        className="sidebar-node"
        onDragStart={(event) => onDragStart(event, 'avatarTaskNode', 'MultiTalk: Generate Avatar')}
        draggable
      >
        MultiTalk: Generate Avatar
      </div>
      <div
        className="sidebar-node"
        onDragStart={(event) => onDragStart(event, 'output', 'Final Output')}
        draggable
      >
        Final Output
      </div>
    </aside>
  );
};

export default Sidebar;
