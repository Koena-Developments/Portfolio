import React from "react";
import { FaHome, FaSearch, FaRegHeart, FaUser, FaPlusSquare } from "react-icons/fa";
import "./Sidebar.css";

const Sidebar = () => {
  return (
    <div className="sidebar">
      <div className="sidebar__logo">
        <h1>Plutogram</h1>
      </div>
      <nav className="sidebar__nav">
        <ul>
          <li>
            <FaHome />
            <span>Home</span>
          </li>
          <li>
            <FaSearch />
            <span>Search</span>
          </li>
          <li>
            <FaPlusSquare />
            <span>Create</span>
          </li>
          <li>
            <FaRegHeart />
            <span>Notifications</span>
          </li>
          <li>
            <FaUser />
            <span>Profile</span>
          </li>
        </ul>
      </nav>
    </div>
  );
};

export default Sidebar;
