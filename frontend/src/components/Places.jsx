import { useEffect, useState } from "react";
import api from "../api";
import "../css/directory.css";


const categories = [
  ["", "All places"],
  ["hotel", "Hotels"],
  ["resort", "Resorts & getaways"],
  ["restaurant", "Restaurants"],
  ["cafe", "Cafes"],
  ["park", "Parks"],
];

function Places() {
  const [places, setPlaces] = useState([]);
  const [search, setSearch] = useState("");
  const [category, setCategory] = useState("");
  const [location, setLocation] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const loadPlaces = async () => {
      setLoading(true);
      setError("");

      try {
        const params = {};
        if (search.trim()) params.search = search.trim();
        if (category) params.category = category;
        if (location.trim()) params.location = location.trim();

        const response = await api.get("/places/", { params });
        setPlaces(response.data.results ?? response.data);
      } catch {
        setError("Could not load pet-friendly places. Please try again.");
      } finally {
        setLoading(false);
      }
    };

    const timer = setTimeout(loadPlaces, 300);
    return () => clearTimeout(timer);
  }, [search, category, location]);

  return (
    <section className="directory-page">
      <div className="directory-heading">
        <span className="eyebrow">EXPLORE TOGETHER</span>
        <h1>Pet-Friendly Places 📍</h1>
        <p>Discover places where you and your companion can spend time together.</p>
      </div>

      <div className="directory-filters">
        <input
          type="search"
          placeholder="Search places, areas or amenities..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />

        <select
          value={category}
          onChange={(e) => setCategory(e.target.value)}
        >
          {categories.map(([value, label]) => (
            <option key={value} value={value}>{label}</option>
          ))}
        </select>

        <input
          type="text"
          placeholder="Filter by area or city..."
          value={location}
          onChange={(e) => setLocation(e.target.value)}
        />
      </div>

      {loading && <p>Loading pet-friendly places...</p>}
      {error && <p role="alert">{error}</p>}

      {!loading && !error && places.length === 0 && (
        <p>No places found. Try changing your filters.</p>
      )}

      <div className="directory-grid">
        {places.map((place) => (
          <article className="directory-card" key={place.id}>
            <div className="directory-card-icon">
              {place.category === "hotel" ? "🏨" :
                place.category === "resort" ? "🌴" :
                place.category === "restaurant" ? "🍽️" :
                place.category === "cafe" ? "☕" : "🌳"}
            </div>

            <div className="directory-card-content">
              <span className="directory-category">{place.category_label}</span>
              <h3>{place.name}</h3>
              <p>📍 {place.location}, {place.city}</p>

              {place.address && <p>{place.address}</p>}
              {place.price_label && <p>💰 {place.price_label}</p>}
              {place.pet_fee > 0 && <p>🐾 Additional pet fee: ₹{place.pet_fee}</p>}

              {place.pet_policy && (
                <p className="directory-policy">{place.pet_policy}</p>
              )}

              {place.amenities_list?.length > 0 && (
                <div className="directory-tags">
                  {place.amenities_list.map((amenity) => (
                    <span key={amenity}>{amenity}</span>
                  ))}
                </div>
              )}

              <div className="directory-card-footer">
                {place.is_sample && <span>Demo listing</span>}
              </div>

              {place.phone && (
                <a className="button" href={`tel:${place.phone}`}>
                  Contact place
                </a>
              )}
            </div>
          </article>
        ))}
      </div>
    </section>
  );
}

export default Places;