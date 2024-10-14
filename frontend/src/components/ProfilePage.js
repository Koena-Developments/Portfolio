import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './ProfilePage.css';

const ProfilePage = () => {
    const [isFollowing, setIsFollowing] = useState(false);
    const [profileData, setProfileData] = useState(null); // Initialize as null to indicate no data yet
    const [projects, setProjects] = useState([]);
    const [loadingProfile, setLoadingProfile] = useState(true); // Track loading state

    const getToken = () => localStorage.getItem('token');

    useEffect(() => {
        const token = getToken();

        // Fetch profile data
        axios.get('http://127.0.0.1:8000/api/profile', {
            headers: {
                Authorization: `Bearer ${token}`,  
            },
        })
        .then(response => {
            console.log('Profile Data:', response.data); // Log profile data for debugging
            setProfileData(response.data); // Set profile data once fetched
            setLoadingProfile(false);  // Set loading to false after receiving data
        })
        .catch(error => {
            console.error('Error fetching profile data:', error);
            setLoadingProfile(false);  // Set loading to false even if there's an error
        });

        // Fetch projects data
        axios.get('http://127.0.0.1:8000/api/projects/', {
            headers: {
                Authorization: `Bearer ${token}`,  // Add the token in the Authorization header
            },
        })
        .then(response => {
            console.log('Projects Data:', response.data); // Log projects data for debugging
            setProjects(response.data); // Set projects data once fetched
        })
        .catch(error => {
            console.error('Error fetching projects:', error);
        });
    }, []);

    // Handle follow/unfollow click
    const handleFollowClick = () => {
        const token = getToken();
        setIsFollowing(!isFollowing);

        axios.post('http://127.0.0.1:8000/api/follow/', 
        { isFollowing: !isFollowing }, 
        {
            headers: {
                Authorization: `Bearer ${token}`,  // Add the token in the Authorization header
            },
        })
        .then(response => {
            console.log('Follow/Unfollow success:', response.data);
        })
        .catch(error => {
            console.error('Error in follow/unfollow:', error);
        });
    };

    // if (loadingProfile) return <div>Loading profile data...</div>;

    // if (!profileData) return <div>Profile data not available.</div>;

    return (
        <div className="profile-container">
            <div className="profile-header">
                {/* Ensure profileData is not null before accessing its properties */}
                {profileData && (
                    <>
                        <img 
                            src={profileData.profile_picture || "https://via.placeholder.com/150"} 
                            alt="Profile"
                            className="profile-image"
                        />
                        <div className="profile-info">
                            <div className="profile-username">
                                <h2>{profileData.username}</h2>
                                <button className="follow-button" onClick={handleFollowClick}>
                                    {isFollowing ? 'Unfollow' : 'Follow'}
                                </button>
                            </div>
                            <div className="profile-stats">
                                <span><strong>{projects.length}</strong> projects</span>
                                <span><strong>{profileData.followers_count}</strong> followers</span>
                            </div>
                            <div className="profile-bio">
                                <p>{profileData.bio}</p>
                            </div>
                        </div>
                    </>
                )}
            </div>
    
            <div className="profile-posts">
                <div className="grid-posts">
                    {projects.map(project => (
                        <div key={project.id} className="project-item">
                            <img src="https://via.placeholder.com/150" alt={project.title} />
                            <h3>{project.title}</h3>
                            <p>{project.description}</p>
                            <button>{project.like_count} Likes</button>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
};

export default ProfilePage;
