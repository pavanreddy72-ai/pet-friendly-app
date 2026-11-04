
import { useCallback, useEffect, useState } from "react";
import api from "../api";
import Catalogue from "./Catalogue";
import Listings from "./Listings";
import HealthCare from "./HealthCare";
import Products from "./Products";
import Vets from "./Vets";
import Places from "./Places";
import "../css/dashboard.css";

const petCategories = [
  { name: "Dogs", emoji: "🐕", description: "Care, breeds and training" },
  { name: "Cats", emoji: "🐈", description: "Health, play and grooming" },
  { name: "Rabbits", emoji: "🐇", description: "Housing and daily care" },
  { name: "Birds", emoji: "🦜", description: "Enrichment and nutrition" },
  { name: "Fish", emoji: "🐠", description: "Aquariums and water care" },
  { name: "Small pets", emoji: "🐹", description: "Hamsters and guinea pigs" },
];

const quickLinks = [
  { title: "My Pets", emoji: "🐾", description: "Manage your pet profiles", section: "pets" },
  { title: "Explore Catalogue", emoji: "🔎", description: "Browse animal breeds and information", section: "catalogue" },
  { title: "Adoption & Sale", emoji: "🏡", description: "Find animals and publish listings", section: "listings" },
  { title: "Health & Care", emoji: "🩺", description: "Keep care records organised", section: "health" },
  { title: "Pet Products", emoji: "🧸", description: "Explore useful pet supplies", section: "products" },
  { title: "Find a Vet", emoji: "🏥", description: "Find veterinary services", section: "vets" },
  { title: "Pet-friendly Places", emoji: "📍", description: "Discover places to visit", section: "places" },
];

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

function Dashboard({ email, onLogout }) {
  const [activeView, setActiveView] = useState("dashboard");
  const [pets, setPets] = useState([]);
  const [loadingPets, setLoadingPets] = useState(true);
  const [petError, setPetError] = useState("");
  const [savingPet, setSavingPet] = useState(false);
  const [petName, setPetName] = useState("");
  const [species, setSpecies] = useState("dog");

  const loadPets = useCallback(async () => {
    try {
      const response = await api.get("/pets/");
      setPets(response.data);
      setPetError("");
    } catch (error) {
      setPetError(
        error.response?.status === 401
          ? "Your session may have expired. Please log out and log in again."
          : "Could not load your pets. Please try again."
      );
    } finally {
      setLoadingPets(false);
    }
  }, []);

  useEffect(() => {
    const timer = setTimeout(() => {
      loadPets();
    }, 0);

    return () => clearTimeout(timer);
  }, [loadPets]);

  async function handleAddPet(event) {
    event.preventDefault();

    if (!petName.trim()) {
      setPetError("Please enter your pet's name.");
      return;
    }

    setSavingPet(true);
    setPetError("");

    try {
      await api.post("/pets/", {
        name: petName.trim(),
        species,
      });

      setPetName("");
      setSpecies("dog");
      await loadPets();
    } catch (error) {
      const data = error.response?.data;

      setPetError(
        data?.name?.[0] ||
          data?.species?.[0] ||
          data?.detail ||
          "Could not save your pet. Please try again."
      );
    } finally {
      setSavingPet(false);
    }
  }

  function renderHeader() {
    return (
      <header className="topbar dashboard-topbar">
        <a
          className="brand"
          href="#dashboard"
          aria-label="PetFriendly dashboard"
          onClick={(event) => {
            event.preventDefault();
            setActiveView("dashboard");
          }}
        >
          <span className="brand-icon" aria-hidden="true">🐾</span>
          <span>
            pet<span className="brand-accent">friendly</span>
          </span>
        </a>

        <div className="dashboard-account">
          <span className="account-email">{email}</span>

          {activeView !== "dashboard" && (
            <button
              type="button"
              className="button button-outline"
              onClick={() => setActiveView("dashboard")}
            >
              Back to dashboard
            </button>
          )}

          <button
            type="button"
            className="button button-outline logout-button"
            onClick={onLogout}
          >
            Log out
          </button>
        </div>
      </header>
    );
  }

  // Application section navigation
  if (
    ["catalogue", "listings", "health", "products", "vets", "places"].includes(
      activeView
    )
  ) {
    return (
      <main className="pet-app dashboard">
        {renderHeader()}

        <section className="dashboard-content">
          {activeView === "catalogue" ? (
            <Catalogue />
          ) : activeView === "listings" ? (
            <Listings />
          ) : activeView === "health" ? (
            <HealthCare />
          ) : activeView === "products" ? (
            <Products />
          ) : activeView === "vets" ? (
            <Vets />
          ) : (
            <Places />
          )}
        </section>

        <footer className="site-footer">
          Made for every paw, wing, fin, and little friend.{" "}
          <span aria-hidden="true">♥</span>
        </footer>
      </main>
    );
  }

  return (
    <main className="pet-app dashboard">
      {renderHeader()}

      <section className="dashboard-content" id="dashboard">

        {/* Welcome */}
        <div className="dashboard-welcome">
          <div>
            <span className="eyebrow">YOUR PET-FRIENDLY SPACE</span>
            <h1>A little more love, every day.</h1>
            <p>
              Discover care, companionship and helpful services for every kind
              of pet.
            </p>
          </div>

          <div className="dashboard-mascots" aria-hidden="true">
            🐕 🐈 🐇
          </div>
        </div>

        {/* My Pets */}
        <section
          className="dashboard-section"
          id="pets"
          aria-labelledby="my-pets-title"
        >
          <div className="section-heading">
            <div>
              <span className="eyebrow">YOUR COMPANIONS</span>
              <h2 id="my-pets-title">My Pets</h2>
            </div>
          </div>

          <form className="pet-form" onSubmit={handleAddPet}>
            <label htmlFor="pet-name">Pet name</label>

            <input
              id="pet-name"
              type="text"
              value={petName}
              onChange={(event) => setPetName(event.target.value)}
              placeholder="Enter your pet's name"
              maxLength={100}
              required
            />

            <label htmlFor="pet-species">Species</label>

            <select
              id="pet-species"
              value={species}
              onChange={(event) => setSpecies(event.target.value)}
            >
              {speciesOptions.map(([value, label]) => (
                <option key={value} value={value}>
                  {label}
                </option>
              ))}
            </select>

            <button
              className="button"
              type="submit"
              disabled={savingPet}
            >
              {savingPet ? "Saving..." : "Add pet"}
            </button>
          </form>

          {petError && <p role="alert">{petError}</p>}

          {loadingPets ? (
            <p>Loading your pets...</p>
          ) : pets.length === 0 ? (
            <p>You haven't added any pets yet. Add your first pet above!</p>
          ) : (
            <div className="category-grid">
              {pets.map((pet) => {
                const speciesLabel =
                  speciesOptions.find(([value]) => value === pet.species)?.[1] ||
                  pet.species;

                const emojiBySpecies = {
                  dog: "🐕",
                  cat: "🐈",
                  rabbit: "🐇",
                  guinea_pig: "🐹",
                  hamster: "🐹",
                  bird: "🦜",
                  fish: "🐠",
                  tortoise: "🐢",
                  rat: "🐀",
                  chinchilla: "🐭",
                  other: "🐾",
                };

                return (
                  <article className="category-card" key={pet.id}>
                    <span className="category-emoji" aria-hidden="true">
                      {emojiBySpecies[pet.species] || "🐾"}
                    </span>

                    <div>
                      <h3>{pet.name}</h3>
                      <p>{speciesLabel}</p>
                      {pet.breed && <p>{pet.breed}</p>}
                    </div>
                  </article>
                );
              })}
            </div>
          )}
        </section>

        {/* Quick Links */}
        <section
          className="dashboard-section"
          aria-labelledby="quick-links-title"
        >
          <div className="section-heading">
            <div>
              <span className="eyebrow">GET STARTED</span>
              <h2 id="quick-links-title">Your pet toolkit</h2>
            </div>
          </div>

          <div className="quick-link-grid">
            {quickLinks.map((item) => (
              <article className="quick-link-card" key={item.section}>
                <span className="quick-link-icon" aria-hidden="true">
                  {item.emoji}
                </span>

                <h3>{item.title}</h3>
                <p>{item.description}</p>

                {item.section === "pets" ? (
                  <a className="coming-soon" href="#pets">
                    Manage my pets
                  </a>
                ) : (
                  <button
                    type="button"
                    className="coming-soon"
                    onClick={() => setActiveView(item.section)}
                  >
                    {item.section === "catalogue"
                      ? "Browse catalogue"
                      : item.section === "listings"
                      ? "Browse adoption & sale"
                      : item.section === "health"
                      ? "Open Health & Care"
                      : item.section === "products"
                      ? "Explore products"
                      : item.section === "vets"
                      ? "Find veterinary care"
                      : "Explore places"}
                  </button>
                )}
              </article>
            ))}
          </div>
        </section>

        {/* Clickable Pet Categories */}
        <section
          className="dashboard-section"
          aria-labelledby="categories-title"
        >
          <div className="section-heading">
            <div>
              <span className="eyebrow">PETS OF ALL KINDS</span>
              <h2 id="categories-title">Explore pet categories</h2>
            </div>
          </div>

          <div className="category-grid">
            {petCategories.map((pet) => (
              <button
                type="button"
                className="category-card category-card-clickable"
                key={pet.name}
                onClick={() => setActiveView("catalogue")}
                aria-label={`Explore ${pet.name} in the catalogue`}
              >
                <span className="category-emoji" aria-hidden="true">
                  {pet.emoji}
                </span>

                <div>
                  <h3>{pet.name}</h3>
                  <p>{pet.description}</p>
                  <span className="category-explore-link">
                    Explore breeds →
                  </span>
                </div>
              </button>
            ))}
          </div>
        </section>

        {/* Dashboard Note */}
        <section className="dashboard-note">
          <span aria-hidden="true">🌱</span>

          <div>
            <h2>Every pet deserves thoughtful care.</h2>
            <p>
              We're building tools to help you organise pet information and
              find trustworthy care resources.
            </p>
          </div>
        </section>
      </section>

      <footer className="site-footer">
        Made for every paw, wing, fin, and little friend.{" "}
        <span aria-hidden="true">♥</span>
      </footer>
    </main>
  );
}

export default Dashboard;
