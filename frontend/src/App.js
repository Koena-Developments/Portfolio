import React from 'react';
import './App.css';
import NavigationBar from './components/Nav_bar';
import ProfilePage from './components/ProfilePage'; 

function App() {                  
  return (
    <div className="App">
      <NavigationBar/>

      <div style={{ paddingTop: '60px', paddingBottom: '60px' }}>
        <ProfilePage />  
      </div>

    </div>
  );
}

export default App;
