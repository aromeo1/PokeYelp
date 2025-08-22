import { useState, useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { useModal } from "../../context/Modal";
import { thunkAuthenticate } from "../../redux/session";
import "./CreatePokemonModal.css";

function CreatePokemonModal({ pokemon = null }) {
  const dispatch = useDispatch();
  const { closeModal } = useModal();
  const sessionUser = useSelector(state => state.session.user);
  const [name, setName] = useState(pokemon ? pokemon.name : "");
  const [description, setDescription] = useState(pokemon ? pokemon.description : "");
  const [type, setType] = useState(pokemon ? pokemon.type : "");
  const [typeSecondary, setTypeSecondary] = useState(pokemon ? pokemon.type_secondary : "");
  const [region, setRegion] = useState(pokemon ? pokemon.region : "");
  const [category, setCategory] = useState(pokemon ? pokemon.category : "");
  const [imageUrl, setImageUrl] = useState(pokemon && pokemon.images && pokemon.images.length > 0 ? pokemon.images[0].url : "");
  const [errors, setErrors] = useState({});
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    dispatch(thunkAuthenticate());
  }, [dispatch]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!sessionUser) {
      setErrors({ message: "Please log in to create a Pokemon" });
      setIsLoading(false);
      return;
    }

    setIsLoading(true);
    setErrors({});

    try {
      // Get CSRF token from cookies
      const csrfToken = document.cookie
        .split('; ')
        .find(row => row.startsWith('csrf_token='))
        ?.split('=')[1];

      if (!csrfToken) {
        setErrors({ message: "Session expired. Please refresh the page." });
        setIsLoading(false);
        return;
      }

      const url = pokemon ? `/api/pokemon/${pokemon.id}` : "/api/pokemon/";
      const method = pokemon ? "PATCH" : "POST";

      const response = await fetch(url, {
        method: method,
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrfToken
        },
        body: JSON.stringify({
          name: name,
          type: type,
          type_secondary: typeSecondary || '',
          region: region,
          category: category,
          description: description,
          image_url: imageUrl
        }),
        credentials: 'include',
      });

      const contentType = response.headers.get("content-type");
      let data;
      
      try {
        if (contentType && contentType.includes("application/json")) {
          data = await response.json();
        } else {
          const text = await response.text();
          console.error("Server returned non-JSON response:", text);
          throw new Error(`Server error: ${text.substring(0, 100)}`);
        }

        if (response.ok) {
          closeModal();
          window.location.reload();
        } else {
          setErrors(data.errors || { message: data.message || `Failed to ${pokemon ? 'update' : 'create'} Pokemon` });
        }
      } catch (error) {
        console.error("Error parsing response:", error);
        setErrors({ message: "Server error. Please check the console for details." });
      }
    } catch (error) {
      console.error(`Error ${pokemon ? 'updating' : 'creating'} pokemon:`, error);
      if (error.message.includes("JSON")) {
        setErrors({ message: "Server error. Please try again later." });
      } else {
        setErrors({ message: error.message || `Failed to ${pokemon ? 'update' : 'create'} Pokemon. Please try again.` });
      }
    } finally {
      setIsLoading(false);
    }
  };

  if (!sessionUser) {
    return (
      <div className="create-pokemon-modal">
        <h2>{pokemon ? 'Edit Pokemon' : 'Create New Pokemon'}</h2>
        <div className="error">Please log in to {pokemon ? 'edit' : 'create'} a Pokemon</div>
        <div className="modal-buttons">
          <button type="button" onClick={closeModal}>
            Close
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="create-pokemon-modal">
      <h2>{pokemon ? 'Edit Pokemon' : 'Create New Pokemon'}</h2>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="name">Pokemon Name</label>
          <input
            type="text"
            id="name"
            value={name}
            onChange={(e) => setName(e.target.value)}
            required
          />
          {errors.name && <div className="field-error">{errors.name}</div>}
        </div>

        <div className="form-group">
          <label htmlFor="type">Type</label>
          <input
            type="text"
            id="type"
            value={type}
            onChange={(e) => setType(e.target.value)}
            required
          />
          {errors.type && <div className="field-error">{errors.type}</div>}
        </div>

        <div className="form-group">
          <label htmlFor="typeSecondary">Secondary Type (optional)</label>
          <input
            type="text"
            id="typeSecondary"
            value={typeSecondary}
            onChange={(e) => setTypeSecondary(e.target.value)}
          />
          {errors.type_secondary && <div className="field-error">{errors.type_secondary}</div>}
        </div>

        <div className="form-group">
          <label htmlFor="region">Region</label>
          <input
            type="text"
            id="region"
            value={region}
            onChange={(e) => setRegion(e.target.value)}
            required
          />
          {errors.region && <div className="field-error">{errors.region}</div>}
        </div>

        <div className="form-group">
          <label htmlFor="category">Category</label>
          <input
            type="text"
            id="category"
            value={category}
            onChange={(e) => setCategory(e.target.value)}
            required
          />
          {errors.category && <div className="field-error">{errors.category}</div>}
        </div>

        <div className="form-group">
          <label htmlFor="description">Description</label>
          <textarea
            id="description"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            required
          />
          {errors.description && <div className="field-error">{errors.description}</div>}
        </div>

        <div className="form-group">
          <label htmlFor="imageUrl">Image URL</label>
          <input
            type="url"
            id="imageUrl"
            value={imageUrl}
            onChange={(e) => setImageUrl(e.target.value)}
            placeholder="https://example.com/image.jpg"
          />
          {errors.image_url && <div className="field-error">{errors.image_url}</div>}
        </div>

        {errors.message && <div className="error">{errors.message}</div>}

        <div className="modal-buttons">
          <button type="button" onClick={closeModal} disabled={isLoading}>
            Cancel
          </button>
          <button type="submit" disabled={isLoading}>
            {isLoading ? (pokemon ? "Updating..." : "Creating...") : (pokemon ? "Update Pokemon" : "Create Pokemon")}
          </button>
        </div>
      </form>
    </div>
  );
}

export default CreatePokemonModal;
