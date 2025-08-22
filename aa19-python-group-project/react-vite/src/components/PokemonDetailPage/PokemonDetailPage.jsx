import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useSelector } from 'react-redux';
import OpenModalButton from '../OpenModalButton/OpenModalButton';
import ReviewFormModal from '../ReviewFormModal';
import CreatePokemonModal from '../CreatePokemonModal/CreatePokemonModal';
import './PokemonDetailPage.css';

const PokemonDetailPage = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const sessionUser = useSelector(state => state.session.user);
  const [pokemon, setPokemon] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchPokemonDetails();
  }, [id]);

  const fetchPokemonDetails = async () => {
    try {
      const response = await fetch(`/api/pokemon/${id}`);
      if (!response.ok) {
        throw new Error('Failed to fetch Pokémon details');
      }
      const data = await response.json();
      setPokemon(data);
      setLoading(false);
    } catch (err) {
      console.error('Error fetching Pokémon details:', err);
      setError(err.message);
      setLoading(false);
    }
  };

  const calculateAverageRating = (reviews) => {
    if (!reviews || reviews.length === 0) return 0;
    const totalRating = reviews.reduce((sum, review) => sum + review.rating, 0);
    return Math.round((totalRating / reviews.length) * 10) / 10;
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

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString();
  };

  const handleDeleteReview = async (reviewId) => {
    if (!window.confirm('Are you sure you want to delete this review?')) {
      return;
    }

    try {
      const response = await fetch(`/api/reviews/${reviewId}`, {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Failed to delete review');
      }

      // Remove the deleted review from the pokemon state
      setPokemon(prevPokemon => ({
        ...prevPokemon,
        reviews: prevPokemon.reviews.filter(review => review.id !== reviewId)
      }));

    } catch (err) {
      console.error('Error deleting review:', err);
      alert(`Failed to delete review: ${err.message}`);
    }
  };

  const handleDeletePokemon = async () => {
    if (!window.confirm('Are you sure you want to delete this Pokémon? This action cannot be undone.')) {
      return;
    }

    try {
      const response = await fetch(`/api/pokemon/${pokemon.id}`, {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Failed to delete Pokémon');
      }

      navigate('/');
      
    } catch (err) {
      console.error('Error deleting Pokémon:', err);
      alert(`Failed to delete Pokémon: ${err.message}`);
    }
  };

  if (loading) {
    return (
      <div className="pokemon-detail-page">
        <div className="loading-container">
          <h2>Loading Pokémon details...</h2>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="pokemon-detail-page">
        <div className="error-container">
          <h2>Error Loading Pokémon</h2>
          <p>{error}</p>
        </div>
      </div>
    );
  }

  if (!pokemon) {
    return (
      <div className="pokemon-detail-page">
        <div className="error-container">
          <h2>Pokémon not found</h2>
        </div>
      </div>
    );
  }

  const averageRating = calculateAverageRating(pokemon.reviews);
  const reviewCount = pokemon.reviews ? pokemon.reviews.length : 0;

  return (
    <div className="pokemon-detail-page">
      <div className="detail-container">
        <div className="pokemon-header">
          <div className="pokemon-image-section">
            <img 
              src={pokemon.images && pokemon.images.length > 0 
                ? pokemon.images[0].url 
                : 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/0.png'} 
              alt={pokemon.name} 
              className="detail-pokemon-image"
            />
          </div>

        <div className="pokemon-info-section">
          <div className="pokemon-header-title">
            <h1 className="detail-pokemon-name">{pokemon.name}</h1>
            {sessionUser && sessionUser.id === pokemon.user_id && (
              <div className="pokemon-actions">
                <OpenModalButton
                  modalComponent={<CreatePokemonModal pokemon={pokemon} />}
                  buttonText="Edit"
                  buttonClass="edit-pokemon-button"
                />
                <button
                  className="delete-pokemon-button"
                  onClick={handleDeletePokemon}
                  title="Delete this Pokémon"
                >
                  Delete
                </button>
              </div>
            )}
          </div>
          
          <p className="pokemon-type">
            Type: {pokemon.type}
            {pokemon.type_secondary && ` / ${pokemon.type_secondary}`}
          </p>

          <div className="pokemon-meta">
            <div className="meta-item">
              <strong>Region:</strong> {pokemon.region || 'Unknown'}
            </div>
            <div className="meta-item">
              <strong>Category:</strong> {pokemon.category || 'Unknown'}
            </div>
            <div className="meta-item">
              <strong>Added:</strong> {formatDate(pokemon.created_at)}
            </div>
          </div>

          <div className="pokemon-rating">
            <span className="stars">{renderStars(averageRating)}</span>
            <span className="rating-text">
              {averageRating}/5 ({reviewCount} reviews)
            </span>
          </div>
        </div>
        </div>

        <div className="pokemon-description">
          <h3>Description</h3>
          <p>{pokemon.description || 'No description available.'}</p>
        </div>

        <div className="reviews-section">
          <div className="reviews-header">
            <h3>Reviews ({reviewCount})</h3>
            {sessionUser && sessionUser.id !== pokemon.user_id && (
              <OpenModalButton
                modalComponent={<ReviewFormModal pokemonId={pokemon.id} />}
                buttonText="Post a Review"
                buttonClass="post-review-button"
              />
            )}
          </div>
          
          {pokemon.reviews && pokemon.reviews.length > 0 ? (
            pokemon.reviews.map(review => (
              <div key={review.id} className="review-card">
                <div className="review-header">
                  <div className="review-meta">
                    <p>
                      <strong>Rating:</strong> {renderStars(review.rating)} 
                      <span style={{marginLeft: '10px', color: '#888', fontSize: '12px'}}>
                        {formatDate(review.created_at)}
                      </span>
                    </p>
                  </div>
                  {sessionUser && sessionUser.id === review.user_id && (
                    <div className="review-actions">
                      <OpenModalButton
                        modalComponent={<ReviewFormModal pokemonId={pokemon.id} review={review} />}
                        buttonText="Edit"
                        buttonClass="edit-review-button"
                      />
                      <button
                        className="delete-review-button"
                        onClick={() => handleDeleteReview(review.id)}
                        title="Delete this review"
                      >
                        Delete
                      </button>
                    </div>
                  )}
                </div>
                {review.title && (
                  <h4 className="review-title">{review.title}</h4>
                )}
                {review.body && (
                  <p>{review.body}</p>
                )}
              </div>
            ))
          ) : (
            <p className="no-reviews">No reviews yet. Be the first to review this Pokémon!</p>
          )}
        </div>
      </div>
    </div>
  );
};

export default PokemonDetailPage;
