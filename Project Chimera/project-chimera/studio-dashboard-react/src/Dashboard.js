import React, { useState, useCallback, useMemo } from 'react';
import {
  ReactFlow,
  addEdge,
  useNodesState,
  useEdgesState,
  Controls,
  Background,
} from '@xyflow/react';

import Sidebar from './Sidebar';
import AITaskNode from './nodes/AITaskNode';
import AvatarTaskNode from './nodes/AvatarTaskNode';
import StartNode from './nodes/StartNode';
import JobStatus from './JobStatus';

const initialNodes = [
  { id: '1', type: 'startNode', data: { label: 'Project Start' }, position: { x: 250, y: 50 } },
];

let id = 2;
const getId = () => `${id++}`;

const Dashboard = () => {
  const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);
  const [reactFlowInstance, setReactFlowInstance] = useState(null);

  const updateNodeData = useCallback((nodeId, newData) => {
    setNodes((nds) =>
      nds.map((node) => {
        if (node.id === nodeId) {
          return { ...node, data: { ...node.data, ...newData } };
        }
        return node;
      })
    );
  }, [setNodes]);

  const onDeleteNode = useCallback((nodeId) => {
    setNodes((nds) => nds.filter((node) => node.id !== nodeId));
  }, [setNodes]);

  const nodeTypes = useMemo(() => ({
    startNode: StartNode,
    aiTaskNode: (props) => <AITaskNode {...props} onDataChange={updateNodeData} onDelete={onDeleteNode} />,
    avatarTaskNode: (props) => <AvatarTaskNode {...props} onDataChange={updateNodeData} onDelete={onDeleteNode} />,
  }), [updateNodeData, onDeleteNode]);

  const handleSubmit = useCallback(async () => {
    // Support both new 'startNode' and legacy 'input' types to prevent errors during hot-reload
    const startNode = nodes.find(n => n.type === 'startNode' || n.type === 'input');
    if (!startNode) {
      alert("Error: Project Start node not found!");
      return;
    }

    const sceneOrder = [];
    let currentNode = startNode;
    // --- FIX: Replaced the 'for' loop with a 'while' loop for cleaner graph traversal ---
    while (currentNode) {
      const outgoingEdge = edges.find(e => e.source === currentNode.id);
      if (!outgoingEdge) break; // End of the chain

      const nextNode = nodes.find(n => n.id === outgoingEdge.target);
      if (!nextNode) break; // Should not happen in a valid graph

      if (nextNode.type === 'aiTaskNode' || nextNode.type === 'avatarTaskNode') {
        sceneOrder.push(nextNode);
      }
      currentNode = nextNode;
    }

    if (sceneOrder.length === 0) {
      alert("Please connect at least one filter node to the Project Start node.");
      return;
    }

    const formData = new FormData();

    sceneOrder.forEach((node, index) => {
      // Backend expects format: "Script Text | Image Prompt"
      // We use node.data.prompt for both if no separate image prompt exists.
      const scriptText = node.data.prompt || "Default script text";

      let imagePrompt = node.data.prompt || "A cinematic scene";
      if (node.type === 'avatarTaskNode' && node.data.useNewsCaster) {
        imagePrompt = "RESOURCE:newscaster_avatar.png";
      }

      // Construct the pipe-separated string
      const payload = `${scriptText}|${imagePrompt}`;

      formData.append(`scene_${index + 1}`, payload);

      if (node.type === 'avatarTaskNode' && node.data.avatarFile) {
        formData.append(`file_${index + 1}`, node.data.avatarFile);
      }
    });

    try {
      const response = await fetch('http://localhost:5001/api/add_storyboard_job', {
        method: 'POST',
        headers: {
          'X-API-KEY': 'local-dev-key',
        },
        body: formData,
      });
      const result = await response.json();
      if (result.status === 'success') {
        alert(`Successfully submitted job #${result.storyboard_id}!`);
      } else {
        throw new Error(result.message || 'Failed to submit job.');
      }
    } catch (error) {
      console.error("Error submitting job:", error);
      alert(`Error: ${error.message}`);
    }
  }, [nodes, edges]);

  const onConnect = useCallback((params) => setEdges((eds) => addEdge(params, eds)), [setEdges]);
  const onDragOver = useCallback((event) => { event.preventDefault(); event.dataTransfer.dropEffect = 'move'; }, []);
  const onDrop = useCallback(
    (event) => {
      event.preventDefault();
      const type = event.dataTransfer.getData('application/reactflow');
      const label = event.dataTransfer.getData('application/label');
      if (!type) return;

      const position = reactFlowInstance.screenToFlowPosition({ x: event.clientX, y: event.clientY });
      const newNode = {
        id: getId(), type, position,
        data: { label, taskType: label, prompt: '', avatarFile: null, avatarFileName: '' },
      };
      setNodes((nds) => nds.concat(newNode));
    },
    [reactFlowInstance, setNodes],
  );

  return (
    <div className="dashboard-wrapper">
      <Sidebar />
      <JobStatus />
      <div className="reactflow-wrapper">
        <ReactFlow
          nodes={nodes} edges={edges} onNodesChange={onNodesChange}
          onEdgesChange={onEdgesChange} onConnect={onConnect} onInit={setReactFlowInstance}
          onDrop={onDrop} onDragOver={onDragOver} nodeTypes={nodeTypes} fitView
        >
          <Controls />
          <Background />
        </ReactFlow>
        <button
          onClick={handleSubmit}
          style={{
            position: 'absolute', bottom: '20px', right: '20px', padding: '12px 24px',
            fontSize: '16px', fontWeight: 'bold', background: 'linear-gradient(45deg, #1a73e8, #4285f4)',
            color: 'white', border: 'none', borderRadius: '8px', cursor: 'pointer',
            boxShadow: '0 4px 12px rgba(0,0,0,0.2)', zIndex: 10,
          }}
        >
          Submit Job
        </button>
      </div>
    </div>
  );
};

export default Dashboard;
