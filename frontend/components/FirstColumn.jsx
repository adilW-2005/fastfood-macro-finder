import React, { useState } from 'react';
import styles from './FirstColumn.module.css';

const FirstColumn = ({ setData, setRestaurants, setUserLocation }) => {
  const [maxCalories, setMaxCalories] = useState(0);
  const [radiusSearch, setRadiusSearch] = useState(0);
  const [minProtein, setMinProtein] = useState(0);
  const [location, setLocation] = useState("");
  const [nlpQuery, setNlpQuery] = useState("");
  const [sortBy, setSortBy] = useState("");

  const fetchData = async () => {
    try {
      const requestData = {
        location: location,
        max_calories: Number(maxCalories),
        min_protein: Number(minProtein),
        radius_search: Number(radiusSearch),
        sort_by: sortBy,
        nlp_query: nlpQuery,
      };

      const response = await fetch("http://127.0.0.1:5000/recommendations", {
        method: "POST",
        mode: "cors",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(requestData),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }

      const result = await response.json();
      console.log("✅ API Response:", result);

      setData(result.restaurants || []);
      setRestaurants(result.brand_names || []);
      setUserLocation({
        lat: result.user_latitude,
        lng: result.user_longitude,
      });
    } catch (error) {
      console.error("❌ Fetch Error:", error);
    }
  };

  return (
    
    <aside className={styles.filters}>
      <h1>Fast Food Finder</h1>
      <h2>Search & Filters</h2>

      <input
        type="text"
        placeholder="Enter location"
        onChange={(e) => setLocation(e.target.value)}
      />

      <div className={styles.inputContainer}>
        <label>Max Calories</label>
        <input
          type="number"
          placeholder="e.g. 500"
          onChange={(e) => setMaxCalories(e.target.value)}
        />
      </div>

      <div className={styles.inputContainer}>
        <label>Min Protein</label>
        <input
          type="number"
          placeholder="e.g. 20"
          onChange={(e) => setMinProtein(e.target.value)}
        />
      </div>

      <div className={styles.rangeContainer}>
        <div className={styles.rangeHeader}>
          <span>Search Radius: {radiusSearch} meters</span>
        </div>
        <input
          type="range"
          min="0"
          max="5000"
          step="100"
          value={radiusSearch}
          onChange={(e) => setRadiusSearch(e.target.value)}
        />
      </div>

      <div className={styles.sortContainer}>
        <h3>Sort By</h3>
        <select onChange={(e) => setSortBy(e.target.value)}>
          <option value="">None</option>
          <option value="calories">Calories (Low to High)</option>
          <option value="protein">Protein (High to Low)</option>
        </select>
      </div>

      <h3>AI-powered Search</h3>
      <input
        type="text"
        placeholder="Enter an AI-powered NLP query"
        onChange={(e) => setNlpQuery(e.target.value)}
      />

      <button onClick={fetchData}>Search</button>
    </aside>
  );
};

export default FirstColumn;
