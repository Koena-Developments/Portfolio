import React from 'react';
import { FaHome, FaSearch, FaPlusSquare, FaHeart, FaUserCircle } from 'react-icons/fa';
import './myComponents.css'; 
const NavigationBar = () => {
    return (
        <nav className="nav-bar">
            <ul className="nav-icons">
               
                <li>
                    <FaUserCircle size={24} />
                </li>
                <li>
                    <FaHome size={24} />
                </li>
                <li>
                    <FaHeart size={24} />
                </li>
                
            </ul>
        </nav>
    );
};

export default NavigationBar;
