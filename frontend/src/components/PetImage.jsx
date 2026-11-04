
import { useState } from "react";

function PetImage({ src, alt = "Pet photo", className = "" }) {
  const [hasError, setHasError] = useState(false);

  const imageSrc = src?.trim() && !hasError
    ? src
    : "/animal-placeholder.svg";

  return (
    <img
      src={imageSrc}
      alt={alt}
      className={className}
      loading="lazy"
      onError={() => setHasError(true)}
    />
  );
}

export default PetImage;
