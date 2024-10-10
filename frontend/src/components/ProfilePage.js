import React, { useState } from 'react';
import './ProfilePage.css'; 

const ProfilePage = () => {
    const [isFollowing, setIsFollowing] = useState(false);

    const handleFollowClick = () => {
        setIsFollowing(!isFollowing); 
    };

    return (
        <div className="profile-container">
            <div className="profile-header">
                <img 
                    src="https://via.placeholder.com/150" 
                    alt="Profile"
                    className="profile-image"
                />
                <div className="profile-info">
                    <div className="profile-username">
                        <h2>Thabang Motswenyane</h2>
                        <button className="follow-button" onClick={handleFollowClick}>
                            {isFollowing ? 'Unfollow' : 'Follow'}
                        </button>
                    </div>
                    <div className="profile-stats">
                        <span><strong>23</strong> posts</span>
                        <span><strong>300</strong> followers</span>
                        <span><strong>180</strong> following</span>
                    </div>
                    <div className="profile-bio">
                        <p>Founder of stacky.Taxi | HER MAN  | NUMBER ONE</p>
                    </div>
                </div>
            </div>

            <div className="profile-posts">
                <div className="grid-posts">
                    <img src="https://via.placeholder.com/150" alt="Post 1" />
                    <img src="https://via.placeholder.com/150" alt="Post 2" />
                    <img src="https://via.placeholder.com/150" alt="Post 3" />
                    <img src="https://via.placeholder.com/150" alt="Post 4" />
                    <img src="https://via.placeholder.com/150" alt="Post 5" />
                    <img src="https://via.placeholder.com/150" alt="Post 6" />
                </div>
            </div>
        </div>
    );
};

export default ProfilePage;
