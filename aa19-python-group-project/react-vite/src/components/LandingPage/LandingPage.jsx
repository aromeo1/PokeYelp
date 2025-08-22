import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useSelector } from 'react-redux';
import './LandingPage.css';

const LandingPage = () => {
  const navigate = useNavigate();
  const user = useSelector(state => state.session.user);
  const [pokemonData, setPokemonData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchPokemonData();
  }, []);

  const fetchPokemonData = async () => {
    try {
      const response = await fetch('/api/pokemon/');
      if (!response.ok) {
        throw new Error('Failed to fetch Pokémon data');
      }
      const data = await response.json();
      const pokemonList = data.pokemon || [];
      
      const pokemonWithReviews = pokemonList.map(pokemon => ({
        ...pokemon,
        reviews: pokemon.reviews || []
      }));
      
      setPokemonData(pokemonWithReviews);
      setLoading(false);
    } catch (err) {
      console.error('Error fetching Pokémon:', err);
      setError(err.message);
      setLoading(false);
    }
  };

  const handlePokemonClick = (pokemonId) => {
    navigate(`/pokemon/${pokemonId}`);
  };

  const calculateAverageRating = (reviews) => {
    if (!reviews || reviews.length === 0) return 0;
    const totalRating = reviews.reduce((sum, review) => sum + review.rating, 0);
    return Math.round((totalRating / reviews.length) * 10) / 10;
  };

  const getReviewCount = (reviews) => {
    return reviews ? reviews.length : 0;
  };

  const renderStars = (rating) => {
    const fullStars = Math.floor(rating);
    const hasHalfStar = rating % 1 >= 0.5;
    const emptyStars = 5 - fullStars - (hasHalfStar ? 1 : 0);
    
    return (
      <>
        {'⭐'.repeat(fullStars)}
        {hasHalfStar && '⭐'}
        {'☆'.repeat(emptyStars)}
      </>
    );
  };

  const handleCardClick = (pokemonId) => {
    navigate(`/pokemon/${pokemonId}`);
  };

  if (loading) {
    return (
      <div className="landing-page">
        <main className="landing-main">
          <div className="loading-container">
            <h2>Loading Pokémon...</h2>
          </div>
        </main>
      </div>
    );
  }

  if (error) {
    return (
      <div className="landing-page">
        <main className="landing-main">
          <div className="error-container">
            <h2>Error Loading Pokémon</h2>
            <p>{error}</p>
            <button onClick={fetchPokemonData} className="retry-button">
              Try Again
            </button>
          </div>
        </main>
      </div>
    );
  }

  return (
    <div className="landing-page">
      <main className="landing-main">
        <section className="pokemon-grid">
          <div className="pokemon-cards">
            {pokemonData.map(pokemon => {
              const averageRating = calculateAverageRating(pokemon.reviews);
              const reviewCount = getReviewCount(pokemon.reviews);
              
              return (
                <div 
                  key={pokemon.id} 
                  className="pokemon-card"
                  onClick={() => handleCardClick(pokemon.id)}
                  style={{ cursor: 'pointer' }}
                >
                  <img 
                    src={pokemon.images && pokemon.images.length > 0 ? pokemon.images[0].url : 'https://example.com/image.jpg'} 
                    alt={pokemon.name} 
                    className="pokemon-image"
                  />
                  <div className="pokemon-details">
                    <h3 className="pokemon-name">{pokemon.name}</h3>
                    <p className="pokemon-type">
                      {pokemon.type}
                      {pokemon.type_secondary && ` / ${pokemon.type_secondary}`}
                    </p>
                    <p className="pokemon-region">{pokemon.region || 'Unknown'}</p>
                    <div className="pokemon-rating">
                      <span className="stars">{renderStars(averageRating)}</span>
                      <span className="reviews">({reviewCount} reviews)</span>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        </section>
      </main>
    </div>
  );
};

export default LandingPage;
