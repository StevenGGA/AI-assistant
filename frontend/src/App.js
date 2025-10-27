import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [user, setUser] = useState(null);
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Check if user is logged in
  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      fetchUserInfo(token);
    }
  }, []);

  const fetchUserInfo = async (token) => {
    try {
      const response = await fetch('http://localhost:8000/api/auth/me', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      if (response.ok) {
        const userData = await response.json();
        setUser(userData);
        fetchProjects(token);
      } else {
        localStorage.removeItem('token');
      }
    } catch (err) {
      console.error('Error fetching user info:', err);
    }
  };

  const fetchProjects = async (token) => {
    try {
      const response = await fetch('http://localhost:8000/api/projects/', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      if (response.ok) {
        const projectData = await response.json();
        setProjects(projectData);
      }
    } catch (err) {
      console.error('Error fetching projects:', err);
    }
  };

  const handleLogin = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    const formData = new FormData(e.target);
    
    try {
      const response = await fetch('http://localhost:8000/api/auth/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          username: formData.get('username'),
          password: formData.get('password'),
        }),
      });

      const data = await response.json();
      
      if (response.ok) {
        localStorage.setItem('token', data.access_token);
        fetchUserInfo(data.access_token);
      } else {
        setError(data.detail || 'Login failed');
      }
    } catch (err) {
      setError('Network error. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    setUser(null);
    setProjects([]);
  };

  const handleCreateProject = async (e) => {
    e.preventDefault();
    const token = localStorage.getItem('token');
    const formData = new FormData(e.target);
    
    try {
      const response = await fetch('http://localhost:8000/api/projects/', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          name: formData.get('name'),
          description: formData.get('description'),
        }),
      });

      if (response.ok) {
        fetchProjects(token);
        e.target.reset();
      }
    } catch (err) {
      console.error('Error creating project:', err);
    }
  };

  if (!user) {
    return (
      <div className="App">
        <div className="login-container">
          <h1>AI Workflow Assistant</h1>
          <h2>Login</h2>
          <form onSubmit={handleLogin}>
            <div className="form-group">
              <input
                type="text"
                name="username"
                placeholder="Username or Email"
                required
              />
            </div>
            <div className="form-group">
              <input
                type="password"
                name="password"
                placeholder="Password"
                required
              />
            </div>
            {error && <div className="error">{error}</div>}
            <button type="submit" disabled={loading}>
              {loading ? 'Logging in...' : 'Login'}
            </button>
          </form>
          <p className="hint">Default: admin / admin123</p>
        </div>
      </div>
    );
  }

  return (
    <div className="App">
      <header className="App-header">
        <h1>AI Workflow Assistant</h1>
        <div className="user-info">
          <span>Welcome, {user.full_name || user.username}!</span>
          <button onClick={handleLogout}>Logout</button>
        </div>
      </header>
      
      <main>
        <section className="integrations">
          <h2>Integrations</h2>
          <div className="integration-status">
            <div className={`integration ${user.has_google ? 'connected' : ''}`}>
              Google Drive: {user.has_google ? '✓ Connected' : '✗ Not connected'}
            </div>
            <div className={`integration ${user.has_slack ? 'connected' : ''}`}>
              Slack: {user.has_slack ? '✓ Connected' : '✗ Not connected'}
            </div>
            <div className={`integration ${user.has_canvas ? 'connected' : ''}`}>
              Canvas: {user.has_canvas ? '✓ Connected' : '✗ Not connected'}
            </div>
          </div>
        </section>

        <section className="projects">
          <h2>Projects</h2>
          
          <div className="create-project">
            <h3>Create New Project</h3>
            <form onSubmit={handleCreateProject}>
              <input
                type="text"
                name="name"
                placeholder="Project Name"
                required
              />
              <textarea
                name="description"
                placeholder="Project Description"
                rows="3"
              />
              <button type="submit">Create Project</button>
            </form>
          </div>

          <div className="project-list">
            <h3>Your Projects</h3>
            {projects.length === 0 ? (
              <p>No projects yet. Create your first project above!</p>
            ) : (
              <ul>
                {projects.map(project => (
                  <li key={project.id} className="project-card">
                    <h4>{project.name}</h4>
                    <p>{project.description}</p>
                    <div className="project-meta">
                      <span>Status: {project.status}</span>
                      <span>Members: {project.member_count || 1}</span>
                      <span>Tasks: {project.task_count || 0}</span>
                    </div>
                  </li>
                ))}
              </ul>
            )}
          </div>
        </section>
      </main>
    </div>
  );
}

export default App;