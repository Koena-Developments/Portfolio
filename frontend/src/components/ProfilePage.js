import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { FaPlus } from "react-icons/fa";
import { Si365Datascience } from "react-icons/si";
import { MdEngineering } from "react-icons/md";
import { GiArtificialIntelligence } from "react-icons/gi";
import './ProfilePage.css';

const ProfilePage = () => {
    const [isFollowing, setIsFollowing] = useState(false);
    const [profileData, setProfileData] = useState(null);
    const [projects, setProjects] = useState([]);
    const [loadingProfile, setLoadingProfile] = useState(true);

    const anonymousId = localStorage.getItem('anonymousId') || 'Anonymous1';

    useEffect(() => {
        if (!localStorage.getItem('anonymousId')) {
            localStorage.setItem('anonymousId', anonymousId);
        }

        axios.get('http://127.0.0.1:8000/api/profile/thabangmotswenyane/')
            .then(response => {
                setProfileData(response.data);
                setIsFollowing(response.data.is_following);
                setLoadingProfile(false);
            })
            .catch(error => {
                console.error('Error fetching profile data:', error);
                setLoadingProfile(false);
            });

        axios.get('http://127.0.0.1:8000/api/projects/')
            .then(response => {
                setProjects(response.data);
            })
            .catch(error => {
                console.error('Error fetching projects:', error);
            });
    }, []); 

    const handleFollowClick = async () => {
        const followAction = isFollowing ? 'unfollow' : 'follow';
        try {
            const response = await axios.post(
                `http://127.0.0.1:8000/api/${followAction}/thabangmotswenyane/`, 
                {}, 
                {
                    headers: {
                        'Anonymous-Id': anonymousId,
                        Authorization: `Bearer ${localStorage.getItem('token')}`
                    }
                }
            );
    
            if (response.status === 200) {
                setIsFollowing(!isFollowing);  
                setProfileData(prevData => ({
                    ...prevData,
                    followers_count: prevData.followers_count + (isFollowing ? -1 : 1)
                }));
            } else {
                console.error(`Unexpected response status: ${response.status}`);
            }
        } catch (error) {
            console.error(`Error in ${followAction}:`, error.response?.data || error);
        }
    };
    

    const handleLikeClick = (projectId) => {
        axios.post(`http://127.0.0.1:8000/api/projects/${projectId}/like/`, {}, {
            headers: { 'Anonymous-Id': anonymousId }
        })
        .then(response => {
            const updatedProjects = projects.map(project =>
                project.id === projectId
                    ? { ...project, like_count: response.data.likes }
                    : project
            );
            setProjects(updatedProjects);
        })
        .catch(error => {
            console.error('Error liking/unliking project:', error.response?.data || error);
        });
    };
    
    
    const handleShareClick = () => {
        const shareData = {
            title: 'Check out this profile!',
            text: `Take a look at ${profileData.username}'s profile on our platform.`,
            url: window.location.href
        };

        if (navigator.share) {
            navigator.share(shareData).catch(err => console.error('Error sharing:', err));
        } else {
            navigator.clipboard.writeText(shareData.url)
                .then(() => alert('Profile URL copied to clipboard!'))
                .catch(err => console.error('Failed to copy:', err));
        }
    };

    if (loadingProfile) return <div>Loading profile data...</div>;
    if (!profileData) return <div>Profile data not available.</div>;

    return (
        <div className="profile-container">
            <div className="profile-header">
    <div className="profile-image-container">
        <img
            src={profileData.profile_picture || "https://via.placeholder.com/150"}
            alt="Profile"
            className="profile-image"
        />
        <div className="status-ring"></div> 
    </div>
    
    <div class = "username">
    <h2>{profileData.username}</h2>
    </div>

    <div className="profile-info">
        <div className="profile-username">
            <button className="follow-button" onClick={handleFollowClick}>
                {isFollowing ? 'Unfollow' : 'Follow'}
            </button>
            <button className="share-button" onClick={handleShareClick}>Share Profile</button>
        </div>

        <div className="profile-stats">
            <span className="stats"><strong >{projects.length}</strong></span>
            <span> projects</span>
            <span><strong className="stats">{profileData.followers_count}</strong> followers</span>
            <span><strong className="stats">{profileData.followers_count}</strong> certifications/Qualification</span>

        </div>
        
        <div className="profile-bio">
            <p>{profileData.bio}</p>
        </div>
    </div>
</div>
                
            <div className='upcoming-projects'>
                <div className='project'>
                <ul className='icons'>
                    <FaPlus size={15} />
                    </ul>
                </div>


                <div className='project'>
                    <ul className='icons'>
                    <FaPlus size={15} />
                    </ul>
                </div>


                <div className='project'>
                <ul className='icons'>
                    <FaPlus size={15} />
                    </ul>
                </div>

            </div>


                <div className='hori-line'>
                    <hr></hr>
                </div>

            <div className ="Job-title">
                <ul class="titles"> 
                <li>
                    <Si365Datascience size={35} />
                </li>
                <li>
                    <MdEngineering size={35} />
                </li>
                <li>
                    <GiArtificialIntelligence size={35} />
                </li>
                </ul>
            </div>

            <div className='hori-line'>
                <hr></hr>
            </div>
            <div className="profile-posts">
                <div className="grid-posts">
                    {projects.map(project => (
                        <div key={project.id} className="project-item">
                            <img src={project.image || "https://via.placeholder.com/150"} alt={project.title} />
                            <h3>{project.title}</h3>
                            <p>{project.description}</p>
                            <button onClick={() => handleLikeClick(project.id, project.is_liked)}>
                                {project.is_liked ? 'Unlike' : 'Like'} ({project.like_count})
                            </button>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
};

export default ProfilePage;
