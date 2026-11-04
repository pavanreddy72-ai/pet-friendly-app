import { useEffect, useState } from "react";
import api from "../api";
import "../css/directory.css";

function Vets() {
  const [hospitals, setHospitals] = useState([]);
  const [search, setSearch] = useState("");
  const [area, setArea] = useState("");
  const [emergency, setEmergency] = useState(false);
  const [homeVisits, setHomeVisits] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const loadHospitals = async () => {
      setLoading(true);
      setError("");

      try {
        const params = {};
        if (search.trim()) params.search = search.trim();
        if (area) params.area = area;
        if (emergency) params.emergency = "1";
        if (homeVisits) params.home = "1";

        const response = await api.get("/vets/hospitals/", { params });
        setHospitals(response.data.results ?? response.data);
      } catch {
        setError("Could not load veterinary hospitals. Please try again.");
      } finally {
        setLoading(false);
      }
    };

    const timer = setTimeout(loadHospitals, 300);
    return () => clearTimeout(timer);
  }, [search, area, emergency, homeVisits]);

  const areas = [
    "Koramangala", "Indiranagar", "HSR Layout", "BTM Layout",
    "Jayanagar", "JP Nagar", "Banashankari", "Malleshwaram",
    "Rajajinagar", "Hebbal", "Yelahanka", "Whitefield",
    "Marathahalli", "Bellandur", "Sarjapur Road",
    "Electronic City", "KR Puram", "Kengeri", "Basavanagudi",
    "Bannerghatta Road",
  ];

  return (
    <section className="directory-page">
      <div className="directory-heading">
        <span className="eyebrow">VETERINARY CARE</span>
        <h1>Find a Vet 🏥</h1>
        <p>Find veterinary hospitals and services for your companions.</p>
      </div>

      <div className="directory-filters">
        <input
          type="search"
          placeholder="Search hospitals, services or areas..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />

        <select value={area} onChange={(e) => setArea(e.target.value)}>
          <option value="">All areas</option>
          {areas.map((item) => (
            <option key={item} value={item}>{item}</option>
          ))}
        </select>

        <label>
          <input
            type="checkbox"
            checked={emergency}
            onChange={(e) => setEmergency(e.target.checked)}
          />
          24/7 emergency
        </label>

        <label>
          <input
            type="checkbox"
            checked={homeVisits}
            onChange={(e) => setHomeVisits(e.target.checked)}
          />
          Home visits
        </label>
      </div>

      {loading && <p>Loading veterinary hospitals...</p>}
      {error && <p role="alert">{error}</p>}

      {!loading && !error && hospitals.length === 0 && (
        <p>No hospitals found. Try changing your filters.</p>
      )}

      <div className="directory-grid">
        {hospitals.map((hospital) => (
          <article className="directory-card" key={hospital.id}>
            <div className="directory-card-icon">🏥</div>
            <div className="directory-card-content">
              <h3>{hospital.name}</h3>
              <p>📍 {hospital.area}, {hospital.city}</p>
              {hospital.address && <p>{hospital.address}</p>}
              <p>🕒 {hospital.open_hours || "Contact for timings"}</p>
              {hospital.fee_label && <p>💰 {hospital.fee_label}</p>}
              <p>🐾 {hospital.pet_types}</p>

              {hospital.services_list?.length > 0 && (
                <div className="directory-tags">
                  {hospital.services_list.map((service) => (
                    <span key={service}>{service}</span>
                  ))}
                </div>
              )}

              <div className="directory-card-footer">
                {hospital.emergency_24x7 && <span>🚨 24/7 Emergency</span>}
                {hospital.home_visits && <span>🏠 Home visits</span>}
                {hospital.is_sample && <span>Demo listing</span>}
              </div>

              {hospital.phone && (
                <a className="button" href={`tel:${hospital.phone}`}>
                  Call hospital
                </a>
              )}
            </div>
          </article>
        ))}
      </div>
    </section>
  );
}

export default Vets;