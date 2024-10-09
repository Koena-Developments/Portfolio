import React from 'react';
import './myComponents.css';
import { FaHome, FaSearch, FaPlusSquare, FaHeart, FaUser } from 'react-icons/fa';

function NavBar() {
  return (
    <div>

      <div className="search-bar">
        <input type="text" placeholder="Search" />
      </div>

      <nav className="navbar">
        <div className="navbar__menu">
          <a href="/home" className="navbar__link"><FaHome /></a>
          <a href="/search" className="navbar__link"><FaSearch /></a>
          <a href="/new" className="navbar__link"><FaPlusSquare /></a>
          <a href="/notifications" className="navbar__link"><FaHeart /></a>
          <a href="/profile" className="navbar__link"><FaUser /></a>
        </div>
      </nav>
    </div>
  );
}

export default NavBar;
