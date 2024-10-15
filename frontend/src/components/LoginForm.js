// import React, { useState } from 'react';
// import axios from 'axios'; 
// import { useNavigate } from 'react-router-dom'; // Import useNavigate

// const LoginForm = () => {
//     const [username, setUsername] = useState('');
//     const [password, setPassword] = useState('');
//     const [error, setError] = useState('');
//     const navigate = useNavigate(); // Initialize navigate

//     const handleSubmit = async (e) => {
//         e.preventDefault();
//         try {
//             const response = await axios.post('http://127.0.0.1:8000/api/login/', {
//                 username,
//                 password,
//             });
//             console.log('Login successful:', response.data.message);
//             localStorage.setItem('token', response.data.token); // Store token on successful login

//             // Redirect to the ProfilePage after successful login
//             navigate('/'); // Change this to the path of your ProfilePage
//         } catch (error) {
//             setError(error.response?.data?.error || 'Login failed');
//             console.error('Error logging in:', error);
//         }
//     };

//     return (
//         <form onSubmit={handleSubmit}>
//             <input
//                 type="text"
//                 value={username}
//                 onChange={(e) => setUsername(e.target.value)}
//                 placeholder="Username"
//                 required
//             />
//             <input
//                 type="password"
//                 value={password}
//                 onChange={(e) => setPassword(e.target.value)}
//                 placeholder="Password"
//                 required
//             />
//             <button type="submit">Login</button>
//             {error && <p>{error}</p>}
//         </form>
//     );
// };

// export default LoginForm;
