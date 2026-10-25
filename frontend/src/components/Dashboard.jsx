
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
  { title: "Adoption", emoji: "🏡", description: "Explore adoption opportunities", section: "adoption" },
  { title: "Health & Care", emoji: "🩺", description: "Keep care records organised", section: "health" },
  { title: "Pet Products", emoji: "🧸", description: "Explore useful pet supplies", section: "products" },
  { title: "Find a Vet", emoji: "🏥", description: "Find veterinary services", section: "vets" },
  { title: "Pet-friendly Places", emoji: "📍", description: "Discover places to visit", section: "places" },
];

function Dashboard({ email, onLogout }) {
  return (
    <main className="pet-app dashboard">
      <header className="topbar dashboard-topbar">
        <a className="brand" href="#dashboard" aria-label="PetFriendly dashboard">
          <span className="brand-icon" aria-hidden="true">🐾</span>
          <span>pet<span className="brand-accent">friendly</span></span>
        </a>
        <div className="dashboard-account">
          <span className="account-email">{email}</span>
          <button className="button button-outline logout-button" onClick={onLogout}>
            Log out
          </button>
        </div>
      </header>

      <section className="dashboard-content" id="dashboard">
        <div className="dashboard-welcome">
          <div>
            <span className="eyebrow">YOUR PET-FRIENDLY SPACE</span>
            <h1>A little more love, every day.</h1>
            <p>Discover care, companionship and helpful services for every kind of pet.</p>
          </div>
          <div className="dashboard-mascots" aria-hidden="true">🐕 🐈 🐇</div>
        </div>

        <section className="dashboard-section" aria-labelledby="quick-links-title">
          <div className="section-heading">
            <div>
              <span className="eyebrow">GET STARTED</span>
              <h2 id="quick-links-title">Your pet toolkit</h2>
            </div>
          </div>
          <div className="quick-link-grid">
            {quickLinks.map((item) => (
              <article className="quick-link-card" key={item.section}>
                <span className="quick-link-icon" aria-hidden="true">{item.emoji}</span>
                <h3>{item.title}</h3>
                <p>{item.description}</p>
                <span className="coming-soon">Coming next</span>
              </article>
            ))}
          </div>
        </section>

        <section className="dashboard-section" aria-labelledby="categories-title">
          <div className="section-heading">
            <div>
              <span className="eyebrow">PETS OF ALL KINDS</span>
              <h2 id="categories-title">Explore pet categories</h2>
            </div>
          </div>
          <div className="category-grid">
            {petCategories.map((pet) => (
              <article className="category-card" key={pet.name}>
                <span className="category-emoji" aria-hidden="true">{pet.emoji}</span>
                <div>
                  <h3>{pet.name}</h3>
                  <p>{pet.description}</p>
                </div>
              </article>
            ))}
          </div>
        </section>

        <section className="dashboard-note">
          <span aria-hidden="true">🌱</span>
          <div>
            <h2>Every pet deserves thoughtful care.</h2>
            <p>We’re building tools to help you organise pet information and find trustworthy care resources.</p>
          </div>
        </section>
      </section>

      <footer className="site-footer">
        Made for every paw, wing, fin, and little friend. <span aria-hidden="true">♥</span>
      </footer>
    </main>
  );
}

export default Dashboard;   
