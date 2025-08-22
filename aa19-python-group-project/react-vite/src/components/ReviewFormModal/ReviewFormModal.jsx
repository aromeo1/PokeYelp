import { useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { useModal } from "../../context/Modal";
import { thunkAuthenticate } from "../../redux/session";
import "./ReviewFormModal.css";

function ReviewFormModal({ pokemonId, review = null }) {
  const dispatch = useDispatch();
  const { closeModal } = useModal();
  const sessionUser = useSelector(state => state.session.user);
  const [rating, setRating] = useState(review ? review.rating : 5);
  const [title, setTitle] = useState(review ? review.title : "");
  const [body, setBody] = useState(review ? review.body : "");
  const [errors, setErrors] = useState({});
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!sessionUser) {
      setErrors({ message: "Please log in to post a review" });
      setIsLoading(false);
      return;
    }

    setIsLoading(true);
    setErrors({});

    try {
      // Get CSRF token from cookies (Flask sets it automatically)
      const csrfToken = document.cookie
        .split('; ')
        .find(row => row.startsWith('csrf_token='))
        ?.split('=')[1];

      if (!csrfToken) {
        setErrors({ message: "Session expired. Please refresh the page." });
        setIsLoading(false);
        return;
      }

      const url = review 
        ? `/api/reviews/${review.id}`
        : `/api/reviews/pokemon/${pokemonId}/reviews`;
      
      const method = review ? "PATCH" : "POST";

      const response = await fetch(url, {
        method: method,
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrfToken
        },
        body: JSON.stringify({
          rating: rating,
          title: title,
          body: body
        }),
        credentials: 'include',
      });

      const contentType = response.headers.get("content-type");
      let data;
      
      try {
        if (contentType && contentType.includes("application/json")) {
          data = await response.json();
        } else {
          // If not JSON, try to read as text to see what the server returned
          const text = await response.text();
          console.error("Server returned non-JSON response:", text);
          throw new Error(`Server error: ${text.substring(0, 100)}`);
        }

        if (response.ok) {
          closeModal();
          window.location.reload(); // Refresh to show the updated review
        } else {
          setErrors(data.errors || { message: data.message || `Failed to ${review ? 'update' : 'post'} review` });
        }
      } catch (error) {
        console.error("Error parsing response:", error);
        setErrors({ message: "Server error. Please check the console for details." });
      }
    } catch (error) {
      console.error(`Error ${review ? 'updating' : 'posting'} review:`, error);
      if (error.message.includes("JSON")) {
        setErrors({ message: "Server error. Please try again later." });
      } else {
        setErrors({ message: error.message || `Failed to ${review ? 'update' : 'post'} review. Please try again.` });
      }
    } finally {
      setIsLoading(false);
    }
  };

  if (!sessionUser) {
    return (
      <div className="review-form-modal">
        <h2>{review ? 'Edit Review' : 'Post a Review'}</h2>
        <div className="error">Please log in to {review ? 'edit' : 'post'} a review</div>
        <div className="modal-buttons">
          <button type="button" onClick={closeModal}>
            Close
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="review-form-modal">
      <h2>{review ? 'Edit Review' : 'Post a Review'}</h2>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="rating">Rating (1-5 stars)</label>
          <select
            id="rating"
            value={rating}
            onChange={(e) => setRating(parseInt(e.target.value))}
            required
          >
            <option value={1}>1 Star</option>
            <option value={2}>2 Stars</option>
            <option value={3}>3 Stars</option>
            <option value={4}>4 Stars</option>
            <option value={5}>5 Stars</option>
          </select>
          {errors.rating && <div className="field-error">{errors.rating}</div>}
        </div>

        <div className="form-group">
          <label htmlFor="title">Title (optional)</label>
          <input
            type="text"
            id="title"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            placeholder="Add a title for your review"
            maxLength={255}
          />
          {errors.title && <div className="field-error">{errors.title}</div>}
        </div>

        <div className="form-group">
          <label htmlFor="body">Review (optional)</label>
          <textarea
            id="body"
            value={body}
            onChange={(e) => setBody(e.target.value)}
            placeholder="Share your thoughts about this Pokémon..."
            rows={4}
            maxLength={1000}
          />
          {errors.body && <div className="field-error">{errors.body}</div>}
        </div>

        {errors.message && <div className="error">{errors.message}</div>}

        <div className="modal-buttons">
          <button type="button" onClick={closeModal} disabled={isLoading}>
            Cancel
          </button>
          <button type="submit" disabled={isLoading}>
            {isLoading ? (review ? "Updating..." : "Posting...") : (review ? "Update Review" : "Post Review")}
          </button>
        </div>
      </form>
    </div>
  );
}

export default ReviewFormModal;
