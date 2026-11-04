
import { useCallback, useEffect, useState } from "react";
import api from "../api";
import PetImage from "./PetImage";
import "../css/listings.css";

const initialForm = {
  pet_name: "",
  species: "dog",
  breed: "",
  age_description: "",
  description: "",
  location: "",
  image_url: "",
  adoption_fee: "0",
  price: "",
};

const speciesOptions = [
  ["dog", "Dog"],
  ["cat", "Cat"],
  ["rabbit", "Rabbit"],
  ["guinea_pig", "Guinea pig"],
  ["hamster", "Hamster"],
  ["bird", "Bird"],
  ["fish", "Fish"],
  ["tortoise", "Tortoise"],
  ["rat", "Pet rat"],
  ["chinchilla", "Chinchilla"],
  ["other", "Other"],
];

function Listings() {
  const [type, setType] = useState("adoptions");
  const [items, setItems] = useState([]);
  const [search, setSearch] = useState("");
  const [showForm, setShowForm] = useState(false);
  const [selectedListing, setSelectedListing] = useState(null);
  const [form, setForm] = useState(initialForm);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");
  const [notice, setNotice] = useState("");

  const loadListings = useCallback(async () => {
    try {
      setError("");
      const response = await api.get(`/listings/${type}/`);
      const data = response.data;
      setItems(Array.isArray(data) ? data : data.results || []);
    } catch (err) {
      setError(
        err.response?.data?.detail ||
          "Could not load listings. Please check the backend and try again.",
      );
    } finally {
      setLoading(false);
    }
  }, [type]);

 useEffect(() => {
  const timer = setTimeout(() => {
    loadListings();
  }, 0);

  return () => clearTimeout(timer);
}, [loadListings]);

  useEffect(() => {
    function handleEscape(event) {
      if (event.key === "Escape") {
        setSelectedListing(null);
      }
    }

    window.addEventListener("keydown", handleEscape);
    return () => window.removeEventListener("keydown", handleEscape);
  }, []);

  function changeType(nextType) {
    setType(nextType);
    setLoading(true);
    setSearch("");
    setShowForm(false);
    setSelectedListing(null);
    setError("");
    setNotice("");
    setForm(initialForm);
  }

  function handleChange(event) {
    const { name, value } = event.target;
    setForm((previous) => ({ ...previous, [name]: value }));
    setError("");
    setNotice("");
  }

  async function handleSubmit(event) {
    event.preventDefault();
    setSaving(true);
    setError("");
    setNotice("");

    const payload = {
      pet_name: form.pet_name.trim(),
      species: form.species,
      breed: form.breed.trim(),
      age_description: form.age_description.trim(),
      description: form.description.trim(),
      location: form.location.trim(),
      image_url: form.image_url.trim(),
    };

    if (type === "adoptions") {
      payload.adoption_fee = form.adoption_fee || "0";
    } else {
      payload.price = form.price;
    }

    try {
      await api.post(`/listings/${type}/`, payload);
      setForm(initialForm);
      setShowForm(false);
      setNotice("Your listing was created successfully.");
      await loadListings();
    } catch (err) {
      const data = err.response?.data;
      setError(
        data && typeof data === "object"
          ? Object.entries(data)
              .map(([key, value]) =>
                `${key.replaceAll("_", " ")}: ${
                  Array.isArray(value) ? value.join(" ") : String(value)
                }`,
              )
              .join(" ")
          : "Could not submit your listing. Please log in and try again.",
      );
    } finally {
      setSaving(false);
    }
  }

  const filteredItems = items.filter((item) => {
    const term = search.trim().toLowerCase();
    if (!term) return true;

    return [
      item.pet_name,
      item.species,
      item.breed,
      item.location,
      item.description,
    ].some((value) => value?.toLowerCase().includes(term));
  });

  function formatPrice(value) {
    const amount = Number(value);
    return Number.isFinite(amount)
      ? `₹${amount.toLocaleString("en-IN", {
          maximumFractionDigits: 2,
        })}`
      : "Not specified";
  }

  return (
    <section className="listings-page">
      <div className="listings-hero">
        <span className="eyebrow">A NEW BEGINNING</span>
        <h1>Find a friend who needs you.</h1>
        <p>
          Explore individual animals looking for a home or listed for sale.
          Every animal deserves responsible care.
        </p>
      </div>

      <div className="listings-toolbar">
        <div
          className="listing-tabs"
          role="tablist"
          aria-label="Listing type"
        >
          <button
            type="button"
            role="tab"
            aria-selected={type === "adoptions"}
            className={type === "adoptions" ? "active" : ""}
            onClick={() => changeType("adoptions")}
          >
            🏡 Adoption
          </button>
          <button
            type="button"
            role="tab"
            aria-selected={type === "sales"}
            className={type === "sales" ? "active" : ""}
            onClick={() => changeType("sales")}
          >
            🐾 For sale
          </button>
        </div>

        <button
          type="button"
          className="button listings-create-button"
          onClick={() => {
            setShowForm((previous) => !previous);
            setError("");
            setNotice("");
          }}
        >
          {showForm ? "Cancel" : "+ Create listing"}
        </button>
      </div>

      {notice && (
        <p className="listings-notice" role="status">
          {notice}
        </p>
      )}
      {error && (
        <p className="listings-error" role="alert">
          {error}
        </p>
      )}

      {showForm && (
        <form className="listing-form" onSubmit={handleSubmit}>
          <h2>Create {type === "adoptions" ? "adoption" : "sale"} listing</h2>
          <p className="listing-form-note">
            Fill in the animal's details to create your listing.
          </p>

          <div className="listing-form-grid">
            <label>
              Animal name *
              <input
                name="pet_name"
                value={form.pet_name}
                onChange={handleChange}
                maxLength={100}
                required
              />
            </label>

            <label>
              Species *
              <select
                name="species"
                value={form.species}
                onChange={handleChange}
              >
                {speciesOptions.map(([value, label]) => (
                  <option key={value} value={value}>
                    {label}
                  </option>
                ))}
              </select>
            </label>

            <label>
              Breed
              <input
                name="breed"
                value={form.breed}
                onChange={handleChange}
                maxLength={100}
              />
            </label>

            <label>
              Age
              <input
                name="age_description"
                value={form.age_description}
                onChange={handleChange}
                maxLength={100}
                placeholder="e.g. 6 months"
              />
            </label>

            <label>
              Location *
              <input
                name="location"
                value={form.location}
                onChange={handleChange}
                maxLength={200}
                placeholder="City or area"
                required
              />
            </label>

            <label>
              Image URL
              <input
                type="url"
                name="image_url"
                value={form.image_url}
                onChange={handleChange}
                maxLength={500}
                placeholder="https://..."
              />
            </label>

            {type === "adoptions" ? (
              <label>
                Adoption fee (₹)
                <input
                  type="number"
                  name="adoption_fee"
                  min="0"
                  step="0.01"
                  value={form.adoption_fee}
                  onChange={handleChange}
                  required
                />
              </label>
            ) : (
              <label>
                Sale price (₹) *
                <input
                  type="number"
                  name="price"
                  min="0.01"
                  step="0.01"
                  value={form.price}
                  onChange={handleChange}
                  required
                />
              </label>
            )}
          </div>

          <label>
            Description *
            <textarea
              name="description"
              value={form.description}
              onChange={handleChange}
              rows={4}
              required
            />
          </label>

          <button className="button" type="submit" disabled={saving}>
            {saving ? "Submitting..." : "Create listing"}
          </button>
        </form>
      )}

      <div className="listings-search">
        <input
          type="search"
          value={search}
          onChange={(event) => setSearch(event.target.value)}
          placeholder="Search by animal, breed or location..."
          aria-label="Search listings"
        />
        <span>{filteredItems.length} listings</span>
      </div>

      {loading ? (
        <p className="listings-state">Loading listings...</p>
      ) : error && items.length === 0 ? (
        <p className="listings-state">
          Listings couldn't be loaded. Check the error above.
        </p>
      ) : filteredItems.length === 0 ? (
        <div className="listings-empty">
          <span aria-hidden="true">🐾</span>
          <h2>No listings found yet</h2>
          <p>
            {search
              ? "Try another search."
              : "Listings will appear here when available."}
          </p>
        </div>
      ) : (
        <div className="listings-grid">
          {filteredItems.map((item) => (
            <article
              className="listing-card"
              key={item.id}
              role="button"
              tabIndex={0}
              aria-label={`View details for ${item.pet_name}`}
              onClick={() => setSelectedListing(item)}
              onKeyDown={(event) => {
                if (event.key === "Enter" || event.key === " ") {
                  event.preventDefault();
                  setSelectedListing(item);
                }
              }}
            >
              <PetImage
                src={item.image_url}
                alt={item.pet_name}
                className="listing-image"
              />

              <div className="listing-card-content">
                <div className="listing-card-heading">
                  <h2>{item.pet_name}</h2>
                  <span className="listing-status">{item.species}</span>
                </div>

                <p className="listing-breed">
                  {[item.breed, item.age_description]
                    .filter(Boolean)
                    .join(" · ") || "Breed and age not specified"}
                </p>

                <p className="listing-description">{item.description}</p>
                <p className="listing-location">📍 {item.location}</p>

                <div className="listing-price">
                  {type === "adoptions"
                    ? Number(item.adoption_fee) > 0
                      ? `Adoption fee: ${formatPrice(item.adoption_fee)}`
                      : "Adoption fee: No fee"
                    : `Price: ${formatPrice(item.price)}`}
                </div>

                <span className="listing-view-hint">View details →</span>
              </div>
            </article>
          ))}
        </div>
      )}

      {selectedListing && (
        <div
          className="listing-modal-backdrop"
          onClick={() => setSelectedListing(null)}
        >
          <section
            className="listing-modal"
            role="dialog"
            aria-modal="true"
            aria-labelledby="listing-modal-title"
            onClick={(event) => event.stopPropagation()}
          >
            <button
              type="button"
              className="listing-modal-close"
              aria-label="Close listing details"
              onClick={() => setSelectedListing(null)}
            >
              ×
            </button>

            <PetImage
              src={selectedListing.image_url}
              alt={selectedListing.pet_name}
              className="listing-modal-image"
            />

            <div className="listing-modal-content">
              <span className="listing-status">
                {selectedListing.species}
              </span>
              <h2 id="listing-modal-title">{selectedListing.pet_name}</h2>

              <div className="listing-modal-facts">
                <p>
                  <strong>Breed:</strong>{" "}
                  {selectedListing.breed || "Not specified"}
                </p>
                <p>
                  <strong>Age:</strong>{" "}
                  {selectedListing.age_description || "Not specified"}
                </p>
                <p>
                  <strong>Location:</strong>{" "}
                  {selectedListing.location || "Not specified"}
                </p>
                <p>
                  <strong>
                    {type === "adoptions" ? "Adoption fee" : "Sale price"}:
                  </strong>{" "}
                  {type === "adoptions"
                    ? formatPrice(selectedListing.adoption_fee ?? 0)
                    : formatPrice(selectedListing.price)}
                </p>
              </div>

              <h3>About this animal</h3>
              <p className="listing-modal-description">
                {selectedListing.description || "No description provided."}
              </p>

              <button
                type="button"
                className="button listing-modal-done"
                onClick={() => setSelectedListing(null)}
              >
                Close details
              </button>
            </div>
          </section>
        </div>
      )}
    </section>
  );
}

export default Listings;
