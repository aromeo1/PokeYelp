import React from 'react';
import { NavLink } from 'react-router-dom';
import { useSelector } from 'react-redux';
import OpenModalButton from '../OpenModalButton/OpenModalButton';
import LoginFormModal from '../LoginFormModal/LoginFormModal';
import SignupFormModal from '../SignupFormModal/SignupFormModal';
import ProfileButton from './ProfileButton';
import CreatePokemonModal from '../CreatePokemonModal/CreatePokemonModal';
import './Navigation.css';

function Navigation() {
  const user = useSelector(state => state.session.user);

  return (
    <header className="landing-header">
      <div className="logo-section">
        <h1 className="poke-logo">
          <NavLink to="/" style={{ textDecoration: 'none', color: 'inherit' }}>
            PokéYelp
          </NavLink>
        </h1>
      </div>
      <nav className="auth-nav">
        {user ? (
          <>
            <OpenModalButton
              buttonText="Create Pokemon"
              modalComponent={<CreatePokemonModal />}
              buttonClass="auth-btn create-pokemon-btn"
            />
            <ProfileButton />
          </>
        ) : (
          <>
            <OpenModalButton
              buttonText="Login"
              modalComponent={<LoginFormModal />}
              buttonClass="auth-btn login-btn"
            />
            <OpenModalButton
              buttonText="Sign Up"
              modalComponent={<SignupFormModal />}
              buttonClass="auth-btn signup-btn"
            />
          </>
        )}
      </nav>
    </header>
  );
}

export default Navigation;
