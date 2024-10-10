import React, { useEffect, useState } from 'react';
import './App.css';
import NavigationBar from './components/Nav_bar';
import ProfilePage from './components/ProfilePage'; 

function App() {
  const [message, setMessage] = useState('');

  useEffect(() => {
    fetch('http://127.0.0.1:8000/api/')
      .then(response => response.json())
      .then(data => {
        setMessage(data.message); 
      })
      .catch(error => console.error('Error fetching data:', error));
  }, []);

  const handleLogin = (username, password) => {
    fetch('http://127.0.0.1:8000/api/login/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ username, password }),
    })
    .then(response => response.json())
    .then(data => {
      setMessage(data.message);
    })
    .catch(error => console.error('Error logging in:', error));
  };

  return (
    <div>
      <NavigationBar />
      <div style={{ paddingTop: '60px', paddingBottom: '60px' }}>
        <ProfilePage />  
      </div>
      <p>{message}</p>
    </div>
  );
}

export default App;
