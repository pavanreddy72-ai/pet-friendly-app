import { useEffect, useMemo, useState } from "react";
import api from "../api";
import PetImage from "./PetImage";
import "../css/products.css";

const categories = [
  ["", "All products"],
  ["food", "Food"],
  ["treats", "Treats"],
  ["toys", "Toys"],
  ["bedding", "Bedding"],
  ["grooming", "Grooming"],
  ["health", "Health"],
  ["accessories", "Accessories"],
  ["travel", "Travel"],
  ["aquarium", "Aquarium"],
  ["cage", "Cages"],
  ["litter", "Litter"],
];

const petTypes = ["All", "Dog", "Cat", "Rabbit", "Bird", "Fish"];

function formatPrice(value) {
  const amount = Number(value);
  return Number.isFinite(amount)
    ? `₹${amount.toLocaleString("en-IN", { maximumFractionDigits: 2 })}`
    : "Price unavailable";
}

export default function Products() {
  const [products, setProducts] = useState([]);
  const [search, setSearch] = useState("");
  const [category, setCategory] = useState("");
  const [pet, setPet] = useState("All");
  const [selected, setSelected] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    let cancelled = false;

    async function loadProducts() {
      setLoading(true);
      setError("");

      try {
        const response = await api.get("/products/");
        const data = response.data;

        if (!cancelled) {
          setProducts(
            Array.isArray(data)
              ? data
              : Array.isArray(data.results)
                ? data.results
                : [],
          );
        }
      } catch (requestError) {
        if (!cancelled) {
          setError(
            requestError.response?.data?.detail ||
              "Could not load products. Please try again.",
          );
        }
      } finally {
        if (!cancelled) setLoading(false);
      }
    }

    loadProducts();

    return () => {
      cancelled = true;
    };
  }, []);

  useEffect(() => {
    function handleEscape(event) {
      if (event.key === "Escape") setSelected(null);
    }

    window.addEventListener("keydown", handleEscape);
    return () => window.removeEventListener("keydown", handleEscape);
  }, []);

  const filteredProducts = useMemo(() => {
    const term = search.trim().toLowerCase();

    return products.filter((product) => {
      const matchesSearch =
        !term ||
        [
          product.name,
          product.description,
          product.category_label,
          product.pet_type,
        ]
          .filter(Boolean)
          .join(" ")
          .toLowerCase()
          .includes(term);

      const matchesCategory =
        !category || product.category === category;

      const matchesPet =
        pet === "All" ||
        product.pet_type?.toLowerCase() === pet.toLowerCase() ||
        product.pet_type?.toLowerCase() === "all" ||
        product.pet_type?.toLowerCase() === "dog & cat";

      return matchesSearch && matchesCategory && matchesPet;
    });
  }, [products, search, category, pet]);

  return (
    <section className="products-page">
      <header className="products-hero">
        <span className="eyebrow">THE PET ESSENTIALS STORE</span>
        <h1>Little things for happier pets.</h1>
        <p>
          Discover food, toys, grooming supplies and everyday essentials
          for your animal companions.
        </p>
      </header>

      <div className="products-toolbar">
        <input
          type="search"
          value={search}
          onChange={(event) => setSearch(event.target.value)}
          placeholder="Search products..."
          aria-label="Search products"
        />

        <select
          value={pet}
          onChange={(event) => setPet(event.target.value)}
          aria-label="Filter by pet"
        >
          {petTypes.map((type) => (
            <option key={type} value={type}>{type} pets</option>
          ))}
        </select>
      </div>

      <div className="products-categories" aria-label="Product categories">
        {categories.map(([value, label]) => (
          <button
            type="button"
            key={value}
            className={category === value ? "active" : ""}
            aria-pressed={category === value}
            onClick={() => setCategory(value)}
          >
            {label}
          </button>
        ))}
      </div>

      <div className="products-results">
        <h2>Explore products</h2>
        <span>{filteredProducts.length} products</span>
      </div>

      {loading ? (
        <p className="products-state">Loading products...</p>
      ) : error ? (
        <p className="products-error" role="alert">{error}</p>
      ) : filteredProducts.length === 0 ? (
        <div className="products-empty">
          <span>🧸</span>
          <h3>No products found</h3>
          <p>Try changing your search or category.</p>
          <button
            type="button"
            onClick={() => {
              setSearch("");
              setCategory("");
              setPet("All");
            }}
          >
            Clear filters
          </button>
        </div>
      ) : (
        <div className="products-grid">
          {filteredProducts.map((product) => (
            <article
              className="product-card"
              key={product.id}
              tabIndex={0}
              role="button"
              aria-label={`View ${product.name}`}
              onClick={() => setSelected(product)}
              onKeyDown={(event) => {
                if (event.key === "Enter" || event.key === " ") {
                  event.preventDefault();
                  setSelected(product);
                }
              }}
            >
              <PetImage
                src={product.image_url}
                alt={product.name}
                className="product-image"
              />

              <div className="product-card-body">
                <span className="product-category">
                  {product.category_label || product.category}
                </span>

                <h3>{product.name}</h3>
                <p className="product-pet">{product.pet_type}</p>

                {product.pack && <p className="product-pack">{product.pack}</p>}

                <div className="product-card-bottom">
                  <strong>{formatPrice(product.price)}</strong>
                  <span className={product.in_stock ? "in-stock" : "out-stock"}>
                    {product.in_stock ? "In stock" : "Out of stock"}
                  </span>
                </div>

                <span className="product-view">View details →</span>
              </div>
            </article>
          ))}
        </div>
      )}

      {selected && (
        <div
          className="product-modal-backdrop"
          onClick={() => setSelected(null)}
        >
          <section
            className="product-modal"
            role="dialog"
            aria-modal="true"
            aria-labelledby="product-modal-title"
            onClick={(event) => event.stopPropagation()}
          >
            <button
              type="button"
              className="product-modal-close"
              onClick={() => setSelected(null)}
              aria-label="Close"
            >
              ×
            </button>

            <PetImage
              src={selected.image_url}
              alt={selected.name}
              className="product-modal-image"
            />

            <div className="product-modal-content">
              <span className="product-category">
                {selected.category_label || selected.category}
              </span>

              <h2 id="product-modal-title">{selected.name}</h2>
              <strong className="product-modal-price">
                {formatPrice(selected.price)}
              </strong>

              <p><strong>Suitable for:</strong> {selected.pet_type}</p>
              {selected.pack && <p><strong>Pack:</strong> {selected.pack}</p>}
              <p>
                <strong>Availability:</strong>{" "}
                {selected.in_stock ? "In stock" : "Out of stock"}
              </p>

              <h3>Product information</h3>
              <p>{selected.description || "No description available."}</p>

              <button
                type="button"
                className="button"
                onClick={() => setSelected(null)}
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
