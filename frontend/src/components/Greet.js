import React from 'react';
import './myComponents.css'; // Make sure to import your CSS file
import { FaHome, FaSearch, FaPlusSquare, FaHeart, FaUser } from 'react-icons/fa';

function NavBar() {
  return (
    <nav className="navbar">
      <div className="navbar__logo">
        <img 
          // src="https://upload.wikimedia.org/wikipedia/commons/a/a5/Instagram_icon.png" 
          alt="Logo" 
        />
      </div>
      <div className="navbar__search">
        <input type="text" placeholder="Search" />
      </div>
      <div className="navbar__menu">
        <a href="#"><FaHome /></a>
        <a href="#"><FaSearch /></a>
        <a href="#"><FaPlusSquare /></a>
        <a href="#"><FaHeart /></a>
        <a href="#"><FaUser /></a>
      </div>
    </nav>
  );
}

export default NavBar;
