import React, { useState, useEffect } from 'react';

const JobStatus = () => {
    const [jobs, setJobs] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [isOpen, setIsOpen] = useState(true);

    const fetchJobs = async () => {
        setLoading(true);
        setError(null);
        try {
            const response = await fetch('http://localhost:5001/api/storyboards', {
                headers: {
                    'X-API-KEY': 'local-dev-key'
                }
            });
            const data = await response.json();
            if (data.status === 'success') {
                setJobs(data.jobs);
            } else {
                setError(data.message || 'Failed to fetch jobs');
            }
        } catch (err) {
            setError('Error connecting to server');
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchJobs();
        const interval = setInterval(fetchJobs, 10000); // Poll every 10 seconds
        return () => clearInterval(interval);
    }, []);

    if (!isOpen) {
        return (
            <button
                onClick={() => setIsOpen(true)}
                style={{
                    position: 'absolute',
                    top: '20px',
                    right: '20px',
                    padding: '10px 16px',
                    backgroundColor: 'white',
                    border: '1px solid #ddd',
                    borderRadius: '8px',
                    boxShadow: '0 2px 5px rgba(0,0,0,0.1)',
                    cursor: 'pointer',
                    zIndex: 100,
                    fontWeight: 'bold',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '8px'
                }}
            >
                📋 Job History
            </button>
        );
    }

    return (
        <div style={{
            position: 'absolute',
            top: '20px',
            right: '20px',
            width: '300px',
            backgroundColor: 'white',
            borderRadius: '8px',
            boxShadow: '0 2px 10px rgba(0,0,0,0.1)',
            padding: '16px',
            zIndex: 100,
            maxHeight: '80vh',
            overflowY: 'auto'
        }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '12px' }}>
                <h3 style={{ margin: 0, fontSize: '16px' }}>Job History</h3>
                <div style={{ display: 'flex', gap: '8px' }}>
                    <button
                        onClick={fetchJobs}
                        disabled={loading}
                        style={{
                            padding: '4px 8px',
                            fontSize: '12px',
                            cursor: 'pointer',
                            background: '#f0f0f0',
                            border: '1px solid #ddd',
                            borderRadius: '4px'
                        }}
                    >
                        {loading ? '...' : 'Refresh'}
                    </button>
                    <button
                        onClick={() => setIsOpen(false)}
                        style={{
                            padding: '4px 8px',
                            fontSize: '12px',
                            cursor: 'pointer',
                            background: 'transparent',
                            border: 'none',
                            fontWeight: 'bold',
                            color: '#666'
                        }}
                    >
                        ✕
                    </button>
                </div>
            </div>

            {error && (
                <div style={{ color: 'red', fontSize: '12px', marginBottom: '8px' }}>
                    {error}
                </div>
            )}

            <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
                {jobs.length === 0 && !loading && (
                    <div style={{ textAlign: 'center', color: '#666', fontSize: '13px' }}>
                        No jobs found.
                    </div>
                )}

                {jobs.map(job => (
                    <div key={job.id} style={{
                        border: '1px solid #eee',
                        borderRadius: '6px',
                        padding: '8px',
                        fontSize: '13px',
                        position: 'relative' // For absolute positioning if needed, or flex
                    }}>
                        <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '4px', alignItems: 'center' }}>
                            <span style={{ fontWeight: 'bold' }}>Job #{job.id}</span>
                            <div style={{ display: 'flex', gap: '6px', alignItems: 'center' }}>
                                <span style={{
                                    padding: '2px 6px',
                                    borderRadius: '10px',
                                    fontSize: '11px',
                                    backgroundColor:
                                        job.status === 'completed' ? '#e6fffa' :
                                            job.status === 'error' ? '#fff5f5' : '#ebf8ff',
                                    color:
                                        job.status === 'completed' ? '#2c7a7b' :
                                            job.status === 'error' ? '#c53030' : '#2b6cb0',
                                }}>
                                    {job.status.toUpperCase()}
                                </span>
                                <button
                                    onClick={async () => {
                                        if (window.confirm(`Are you sure you want to delete Job #${job.id}?`)) {
                                            try {
                                                const response = await fetch(`http://localhost:5001/api/storyboard/${job.id}`, {
                                                    method: 'DELETE',
                                                    headers: {
                                                        'X-API-KEY': 'local-dev-key'
                                                    }
                                                });
                                                if (response.ok) {
                                                    fetchJobs(); // Refresh list
                                                } else {
                                                    alert('Failed to delete job');
                                                }
                                            } catch (e) {
                                                console.error(e);
                                                alert('Error deleting job');
                                            }
                                        }
                                    }}
                                    style={{
                                        background: 'none',
                                        border: 'none',
                                        cursor: 'pointer',
                                        fontSize: '14px',
                                        padding: '0 4px',
                                        color: '#e53e3e' // Red color for delete
                                    }}
                                    title="Delete Job"
                                >
                                    🗑️
                                </button>
                            </div>
                        </div>

                        {job.video_url && (
                            <a href={`http://localhost:5001${job.video_url}`} target="_blank" rel="noopener noreferrer" style={{ display: 'block', color: '#3182ce', textDecoration: 'none', marginTop: '4px' }}>
                                View Video
                            </a>
                        )}

                        {job.error_message && (
                            <div style={{ color: '#e53e3e', fontSize: '11px', marginTop: '4px' }}>
                                Error: {job.error_message}
                            </div>
                        )}
                    </div>
                ))}
            </div>
        </div>
    );
};

export default JobStatus;
