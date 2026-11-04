
import { useEffect, useState, } from "react";
import api from "../api";

// eslint-disable-next-line react-refresh/only-export-components
export function useFetch(url) {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    let cancelled = false;

    async function fetchData() {
      setLoading(true);
      setError("");

      try {
        const response = await api.get(url);
        const result = response.data;

        if (!cancelled) {
          setData(
            Array.isArray(result)
              ? result
              : Array.isArray(result.results)
                ? result.results
                : [],
          );
        }
      } catch (requestError) {
        if (!cancelled) {
          setError(
            requestError.response?.data?.detail ||
              "Could not load information. Please try again.",
          );
        }
      } finally {
        if (!cancelled) {
          setLoading(false);
        }
      }
    }

    fetchData();

    return () => {
      cancelled = true;
    };
  }, [url]);

  return { data, loading, error };
}

export function PageHeader({ eyebrow, title, subtitle }) {
  return (
    <header className="pf-page-header">
      {eyebrow && <span className="eyebrow">{eyebrow}</span>}
      <h1>{title}</h1>
      {subtitle && <p>{subtitle}</p>}
    </header>
  );
}

export function SearchBox({ value, onChange, placeholder = "Search..." }) {
  return (
    <div className="pf-search">
      <span aria-hidden="true">⌕</span>
      <input
        type="search"
        value={value}
        onChange={(event) => onChange(event.target.value)}
        placeholder={placeholder}
        aria-label="Search"
      />
      {value && (
        <button type="button" onClick={() => onChange("")} aria-label="Clear search">
          ×
        </button>
      )}
    </div>
  );
}

export function Chips({
  options,
  value,
  onChange,
  allLabel = "All",
}) {
  return (
    <div className="pf-chips" role="group">
      <button
        type="button"
        className={!value ? "active" : ""}
        aria-pressed={!value}
        onClick={() => onChange("")}
      >
        {allLabel}
      </button>

      {options.map((option) => (
        <button
          type="button"
          key={option.value}
          className={value === option.value ? "active" : ""}
          aria-pressed={value === option.value}
          onClick={() => onChange(option.value)}
        >
          {option.icon && <span>{option.icon} </span>}
          {option.label}
        </button>
      ))}
    </div>
  );
}

export function Status({ loading, error, empty }) {
  if (loading) {
    return <p className="pf-status">Loading, please wait...</p>;
  }

  if (error) {
    return <p className="pf-status pf-status-error" role="alert">{error}</p>;
  }

  if (empty) {
    return (
      <div className="pf-status pf-status-empty">
        <span aria-hidden="true">🐾</span>
        <p>No results found. Try changing your search or filters.</p>
      </div>
    );
  }

  return null;
}

