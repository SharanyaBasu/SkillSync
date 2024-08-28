import React from 'react';
import { Link } from 'react-router-dom';
import './welcomepage.css';

function WelcomePage() {
  return (
    <div className="welcome-container">
      <h1>Welcome to SkillSync</h1>
      <Link to="/main" className="get-started-button">
        Get Started
      </Link>
    </div>
  );
}

export default WelcomePage;
