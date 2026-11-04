import "../css/catalogue.css";
import { useEffect, useMemo, useState } from "react";
import { Chips, PageHeader, SearchBox, Status, useFetch } from "./ui";

const SUITABLE = [
  "Guard dog", "Military & police work", "Search & rescue", "Service & therapy",
  "Family pet", "Apartment living", "First-time owners", "Hot-climate friendly",
  "Herding", "Hunting & retrieving", "Talks & mimics", "Community tank",
];
const PAGE_SIZE = 24;
const PAW = "\u{1F43E}";

function BreedImage({ breed, className }) {
  const [failed, setFailed] = useState(false);
  if (!breed.image_url || failed) {
    return <div className={`pf-img-fallback ${className || ""}`}>{breed.category_emoji || PAW}</div>;
  }
  return (
    <img className={className} src={breed.image_url} alt={breed.name} loading="lazy" onError={() => setFailed(true)} />
  );
}

function Fact({ label, value }) {
  if (!value) return null;
  return (
    <div className="pf-fact">
      <b>{label}</b>
      {value}
    </div>
  );
}

function Detail({ title, text }) {
  if (!text) return null;
  return (
    <>
      <h4>{title}</h4>
      <p>{text}</p>
    </>
  );
}

function BreedModal({ breed, onClose }) {
  useEffect(() => {
    const onKey = (e) => e.key === "Escape" && onClose();
    document.addEventListener("keydown", onKey);
    const previous = document.body.style.overflow;
    document.body.style.overflow = "hidden";
    return () => {
      document.removeEventListener("keydown", onKey);
      document.body.style.overflow = previous;
    };
  }, [onClose]);

  return (
    <div className="pf-overlay" onClick={onClose}>
      <div className="pf-modal" onClick={(e) => e.stopPropagation()} role="dialog" aria-modal="true">
        <button className="pf-close" onClick={onClose} aria-label="Close">&times;</button>
        <BreedImage breed={breed} className="pf-modal-img" />
        <div className="pf-modal-body">
          <span className="pf-badge">{breed.category_emoji} {breed.category_name}</span>
          <h2>{breed.name}</h2>
          <p>{breed.description}</p>

          {breed.legal_note && <div className="pf-notice" style={{ marginTop: 14 }}>&#9888;&#65039; {breed.legal_note}</div>}

          <div className="pf-facts">
            <Fact label="Size" value={breed.size} />
            <Fact label="Height" value={breed.height_range} />
            <Fact label="Weight" value={breed.weight_range} />
            <Fact label="Life span" value={breed.lifespan} />
            <Fact label="Fully grown at" value={breed.adult_age} />
            <Fact label="Origin" value={breed.origin} />
            <Fact label="Temperament" value={breed.temperament} />
            <Fact label="Activity level" value={breed.activity_level} />
            <Fact label="Experience needed" value={breed.experience_level} />
            <Fact label="With children" value={breed.child_compatibility} />
          </div>

          {breed.suitable_for_list?.length > 0 && (
            <>
              <h4>Suitable for</h4>
              <div className="pf-badges">
                {breed.suitable_for_list.map((t) => <span className="pf-badge" key={t}>{t}</span>)}
              </div>
            </>
          )}

          <Detail title="Diet" text={breed.diet} />
          <Detail title="Grooming" text={breed.grooming} />
          <Detail title="Exercise" text={breed.exercise_needs} />
          <Detail title="Housing" text={breed.housing_needs} />
          <Detail title="Social needs" text={breed.social_needs} />
          <Detail title="Care needs" text={breed.care_needs} />
          <Detail title="Health considerations" text={breed.health_considerations} />
          <Detail title="Enrichment" text={breed.enrichment} />

          <p style={{ marginTop: 20 }}>
            <a className="pf-link-btn" href="/services">See care services &amp; prices &rarr;</a>
          </p>
        </div>
      </div>
    </div>
  );
}

export default function CataloguePage() {
  const { data: breeds, loading, error } = useFetch("/catalogue/breeds/");
  const [q, setQ] = useState("");
  const [cat, setCat] = useState("");
  const [tag, setTag] = useState("");
  const filterKey = JSON.stringify([q, cat, tag]);
  const [pagination, setPagination] = useState({ filterKey, shown: PAGE_SIZE });
  const shown = pagination.filterKey === filterKey ? pagination.shown : PAGE_SIZE;
  const [selected, setSelected] = useState(null);

  const categories = useMemo(() => {
    const map = new Map();
    breeds.forEach((b) => {
      if (!map.has(b.category_slug)) {
        map.set(b.category_slug, { value: b.category_slug, label: b.category_name, icon: b.category_emoji });
      }
    });
    return [...map.values()].sort((a, b) => a.label.localeCompare(b.label));
  }, [breeds]);

  const filtered = useMemo(() => {
    const term = q.trim().toLowerCase();
    return breeds.filter(
      (b) =>
        (!cat || b.category_slug === cat) &&
        (!tag || (b.suitable_for_list || []).includes(tag)) &&
        (!term ||
          [b.name, b.category_name, b.suitable_for, b.temperament, b.origin].join(" ").toLowerCase().includes(term))
    );
  }, [breeds, q, cat, tag]);

  return (
    <div className="pf-page">
      <PageHeader
        eyebrow="Find your favourite"
        title="Explore the catalogue"
        subtitle="Breeds with photos, height, life span, who they suit, and care details."
      />
      <SearchBox value={q} onChange={setQ} placeholder="Try German Shepherd, rabbit, guard, apartment..." />
      <Chips options={categories} value={cat} onChange={setCat} allLabel="All animals" />
      <p className="pf-count">Suitable for:</p>
      <Chips options={SUITABLE.map((s) => ({ value: s, label: s }))} value={tag} onChange={setTag} allLabel="Any" />

      <Status loading={loading} error={error} empty={!loading && !error && filtered.length === 0} />
      {!loading && !error && <p className="pf-count">{filtered.length} results</p>}

      <div className="pf-grid">
        {filtered.slice(0, shown).map((b) => (
          <article className="pf-card" key={b.id}>
            <BreedImage breed={b} />
            <div className="pf-card-body">
              <span className="pf-badge" style={{ alignSelf: "flex-start" }}>{b.category_name}</span>
              <h3>{b.name}</h3>
              <p>{[b.size, b.height_range, b.lifespan].filter(Boolean).join(" \u00b7 ")}</p>
              <div className="pf-badges">
                {(b.suitable_for_list || []).slice(0, 3).map((t) => (
                  <span className="pf-badge" key={t}>{t}</span>
                ))}
              </div>
              <button className="pf-link-btn" onClick={() => setSelected(b)}>View details &rarr;</button>
            </div>
          </article>
        ))}
      </div>

      {shown < filtered.length && (
        <p style={{ textAlign: "center", marginTop: 24 }}>
          <button
            className="pf-btn"
            onClick={() => setPagination((current) => ({
              filterKey,
              shown: (current.filterKey === filterKey ? current.shown : PAGE_SIZE) + PAGE_SIZE,
            }))}
          >
            Show more ({filtered.length - shown} left)
          </button>
        </p>
      )}

      {selected && <BreedModal breed={selected} onClose={() => setSelected(null)} />}
    </div>
  );
}

