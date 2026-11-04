
import { useCallback, useEffect, useState } from "react";
import api from "../api";
import "../css/health-care.css";

const initialForm = {
  pet: "",
  record_type: "vaccination",
  title: "",
  date: "",
  next_due_date: "",
  veterinarian: "",
  notes: "",
};

const recordTypes = [
  ["vaccination", "Vaccination"],
  ["vet_visit", "Vet visit"],
  ["medication", "Medication"],
  ["treatment", "Treatment"],
  ["checkup", "Routine checkup"],
  ["other", "Other"],
];

function HealthCare() {
  const [pets, setPets] = useState([]);
  const [records, setRecords] = useState([]);
  const [form, setForm] = useState(initialForm);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [showForm, setShowForm] = useState(false);
  const [error, setError] = useState("");
  const [notice, setNotice] = useState("");

  const loadData = useCallback(async () => {
    setLoading(true);
    setError("");

    try {
      const [petResponse, recordResponse] = await Promise.all([
        api.get("/pets/"),
        api.get("/health/"),
      ]);

      const petData = Array.isArray(petResponse.data)
        ? petResponse.data
        : petResponse.data.results || [];

      const recordData = Array.isArray(recordResponse.data)
        ? recordResponse.data
        : recordResponse.data.results || [];

      setPets(petData);
      setRecords(recordData);
    } catch (requestError) {
      setError(
        requestError.response?.status === 401
          ? "Your session has expired. Please log in again."
          : "Could not load health records. Check that the backend is running.",
      );
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    const timer = setTimeout(() => {
      loadData();
    }, 0);

    return () => clearTimeout(timer);
  }, [loadData]);

  function handleChange(event) {
    const { name, value } = event.target;
    setForm((previous) => ({ ...previous, [name]: value }));
    setError("");
    setNotice("");
  }

  async function handleSubmit(event) {
    event.preventDefault();
    setError("");
    setNotice("");

    if (!form.pet) {
      setError("Please select a pet first.");
      return;
    }

    setSaving(true);

    try {
      await api.post("/health/", {
        ...form,
        pet: Number(form.pet),
        next_due_date: form.next_due_date || null,
      });

      setForm(initialForm);
      setShowForm(false);
      setNotice("Health record saved successfully.");
      await loadData();
    } catch (requestError) {
      const data = requestError.response?.data;

      setError(
        data && typeof data === "object"
          ? Object.entries(data)
              .map(([field, messages]) =>
                `${field.replaceAll("_", " ")}: ${
                  Array.isArray(messages)
                    ? messages.join(" ")
                    : String(messages)
                }`,
              )
              .join(" ")
          : "Could not save the health record.",
      );
    } finally {
      setSaving(false);
    }
  }

  function formatDate(value) {
    if (!value) return "Not set";

    return new Date(`${value}T00:00:00`).toLocaleDateString("en-IN", {
      day: "numeric",
      month: "short",
      year: "numeric",
    });
  }

  return (
    <section className="health-page">
      <header className="health-hero">
        <span className="eyebrow">HEALTH & WELLBEING</span>
        <h1>Every little detail matters.</h1>
        <p>
          Keep your pets’ vaccinations, vet visits, treatments and care dates
          organised in one place.
        </p>
        <button
          type="button"
          className="button"
          onClick={() => {
            setShowForm((previous) => !previous);
            setError("");
            setNotice("");
          }}
        >
          {showForm ? "Cancel" : "+ Add health record"}
        </button>
      </header>

      {notice && <p className="health-notice" role="status">{notice}</p>}
      {error && <p className="health-error" role="alert">{error}</p>}

      {showForm && (
        <form className="health-form" onSubmit={handleSubmit}>
          <h2>Add a health record</h2>

          {pets.length === 0 ? (
            <p>Add a pet to your My Pets section before creating a health record.</p>
          ) : (
            <>
              <div className="health-form-grid">
                <label>
                  Pet *
                  <select name="pet" value={form.pet} onChange={handleChange} required>
                    <option value="">Select your pet</option>
                    {pets.map((pet) => (
                      <option key={pet.id} value={pet.id}>{pet.name}</option>
                    ))}
                  </select>
                </label>

                <label>
                  Record type *
                  <select
                    name="record_type"
                    value={form.record_type}
                    onChange={handleChange}
                    required
                  >
                    {recordTypes.map(([value, label]) => (
                      <option key={value} value={value}>{label}</option>
                    ))}
                  </select>
                </label>

                <label>
                  Title *
                  <input
                    name="title"
                    value={form.title}
                    onChange={handleChange}
                    maxLength={150}
                    placeholder="e.g. Rabies vaccination"
                    required
                  />
                </label>

                <label>
                  Date *
                  <input
                    type="date"
                    name="date"
                    value={form.date}
                    onChange={handleChange}
                    required
                  />
                </label>

                <label>
                  Next due date
                  <input
                    type="date"
                    name="next_due_date"
                    value={form.next_due_date}
                    onChange={handleChange}
                    min={form.date || undefined}
                  />
                </label>

                <label>
                  Veterinarian or clinic
                  <input
                    name="veterinarian"
                    value={form.veterinarian}
                    onChange={handleChange}
                    maxLength={150}
                    placeholder="Optional"
                  />
                </label>
              </div>

              <label>
                Notes
                <textarea
                  name="notes"
                  value={form.notes}
                  onChange={handleChange}
                  rows={4}
                  placeholder="Treatment details, observations or instructions"
                />
              </label>

              <button className="button" type="submit" disabled={saving}>
                {saving ? "Saving..." : "Save health record"}
              </button>
            </>
          )}
        </form>
      )}

      <section className="health-records">
        <div className="health-section-heading">
          <h2>Health history</h2>
          <span>{records.length} records</span>
        </div>

        {loading ? (
          <p className="health-state">Loading your records...</p>
        ) : records.length === 0 ? (
          <div className="health-empty">
            <span aria-hidden="true">🩺</span>
            <h3>No health records yet</h3>
            <p>Your saved vaccinations and vet visits will appear here.</p>
          </div>
        ) : (
          <div className="health-record-grid">
            {records.map((record) => (
              <article className="health-record-card" key={record.id}>
                <span className="health-record-icon" aria-hidden="true">
                  {record.record_type === "vaccination" ? "💉" : "🩺"}
                </span>
                <div className="health-record-content">
                  <span className="health-record-type">
                    {recordTypes.find(([value]) => value === record.record_type)?.[1] ||
                      record.record_type}
                  </span>
                  <h3>{record.title}</h3>
                  <p className="health-pet-name">🐾 {record.pet_name}</p>
                  <p>Date: {formatDate(record.date)}</p>
                  {record.next_due_date && (
                    <p>Next due: {formatDate(record.next_due_date)}</p>
                  )}
                  {record.veterinarian && <p>Vet: {record.veterinarian}</p>}
                  {record.notes && <p className="health-notes">{record.notes}</p>}
                </div>
              </article>
            ))}
          </div>
        )}
      </section>
    </section>
  );
}

export default HealthCare;
