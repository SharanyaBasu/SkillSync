import React, { useState, useEffect } from 'react';
import './mainpage.css';

function MainPage() {
  // Initialize state with data from local storage, or default to empty arrays
  const [skills, setSkills] = useState(() => {
    const savedSkills = localStorage.getItem('skills');
    return savedSkills ? JSON.parse(savedSkills) : [''];
  });
  const [experiences, setExperiences] = useState(() => {
    const savedExperiences = localStorage.getItem('experiences');
    return savedExperiences ? JSON.parse(savedExperiences) : [''];
  });
  const [location, setLocation] = useState('');
  const [jobs, setJobs] = useState([]);

  useEffect(() => {
    // Save skills and experiences to local storage whenever they change
    localStorage.setItem('skills', JSON.stringify(skills));
    localStorage.setItem('experiences', JSON.stringify(experiences));
  }, [skills, experiences]);

  const addField = (type) => {
    if (type === 'skill') {
      if (skills[skills.length - 1].trim() !== '') {
        setSkills([...skills, '']);
      }
    } else if (type === 'experience') {
      setExperiences([...experiences, '']);
    }
  };

  const handleChange = (index, value, type) => {
    if (type === 'skill') {
      const newSkills = [...skills];
      newSkills[index] = value;
      setSkills(newSkills);
    } else if (type === 'experience') {
      const newExperiences = [...experiences];
      newExperiences[index] = value;
      setExperiences(newExperiences);
    }
  };

  const removeSkill = (index) => {
    if (skills.length > 1) {
      const newSkills = skills.filter((_, i) => i !== index);
      setSkills(newSkills);
    }
  };

  const removeExperience = (index) => {
    if (experiences.length > 1) {
      const newExperiences = experiences.filter((_, i) => i !== index);
      setExperiences(newExperiences);
    }
  };

  const handleSubmit = async () => {
    try {
      const location = document.getElementById('location-input').value;
      const userSkills = skills.join(', ');
      const userExperiences = experiences.join(', ');

      const url = new URL('http://127.0.0.1:8000/api/match_jobs');
      url.searchParams.append('location', location);

      const response = await fetch(url.toString(), {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          user_skills: userSkills,
          user_experiences: userExperiences
        }),
      });

      if (response.ok) {
        const data = await response.json();
        setJobs(data.jobs || []);
      } else {
        console.error('Error fetching jobs:', response.statusText);
      }
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <div className="main-container">
      <h1>Enter Your Skills</h1>
      <div className="bubble-container">
        {skills.map((skill, index) => (
          <div key={index} className="bubble">
            <input
              type="text"
              value={skill}
              onChange={(e) => handleChange(index, e.target.value, 'skill')}
              placeholder="Enter skill"
            />
            <button
              onClick={() => removeSkill(index)}
              className="remove-button"
              aria-label="Remove skill"
            >
              &times;
            </button>
            {index === skills.length - 1 && (
              <button onClick={() => addField('skill')} className="add-button">
                +
              </button>
            )}
          </div>
        ))}
      </div>
      <h1>Enter Your Experiences</h1>
      <div className="experience-container">
        {experiences.map((experience, index) => (
          <div key={index} className="experience-box">
            <textarea
              value={experience}
              onChange={(e) => handleChange(index, e.target.value, 'experience')}
              placeholder="Enter experience"
            />
            <button
              onClick={() => removeExperience(index)}
              className="remove-button"
              aria-label="Remove experience"
            >
              &times;
            </button>
            {index === experiences.length - 1 && (
              <button onClick={() => addField('experience')} className="add-button">
                +
              </button>
            )}
          </div>
        ))}
      </div>
      <div className="field-container">
        <label htmlFor="location"><b>Location:</b></label>
        <input
          type="text"
          id="location-input"
          value={location}
          onChange={(e) => setLocation(e.target.value)}
          placeholder="Enter location"
          className="input-field"
        />
      </div>
      <button onClick={handleSubmit} className="submit-button">
        Match Me
      </button>
      <div>
        <h2>Job Results:</h2>
        {jobs.map((job, index) => (
          <div key={index} className="job-result">
            <h3>{job.title}</h3>
            <p><b>Company: </b>{job.company}</p>
            <p><b>Location: </b>{job.location}</p>
            <p><b>Description: </b>{job.description}</p>
            <p><b>Matching Score: </b>{job.matching_score}</p>
            <a href={job.url} target="_blank" rel="noopener noreferrer"><b>View Job</b></a>
          </div>
        ))}
      </div>
    </div>
  );
}

export default MainPage;
