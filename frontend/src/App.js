import React, { useEffect, useState } from 'react';
import './App.css';
import NavigationBar from './components/Nav_bar';
import ProfilePage from './components/ProfilePage';
// import LoginForm from './components/LoginForm'; 
import SignupForm from './components/SignupForm';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';

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

    return (
        <Router>
            <NavigationBar />
            <div style={{ paddingTop: '60px', paddingBottom: '60px' }}>
                <Routes>
                    <Route path="/" element={<ProfilePage />} /> 
                    {/* <Route path="/login" element={<LoginForm />} />  */}
                    <Route path= "/signup" element={<SignupForm />} />
                </Routes>
            </div>
            <p>{message}</p>
        </Router>
    );
}

export default App;
