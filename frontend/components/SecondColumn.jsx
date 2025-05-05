import React, { useState } from 'react';
import styles from './SecondColumn.module.css';

const SecondColumn = ({ data, nutritionData, refreshNutrition , restaurants }) => {
  const [activeTab, setActiveTab] = useState("results");
  const [searchQuery, setSearchQuery] = useState("");

  const isLogged = (item) => {
    return nutritionData.logs?.some((log) => log.food_id === item.food_id);
  };

  const getPieChartStyle = (carbs, protein, fat) => {
    const totalCalories = (carbs * 4) + (protein * 4) + (fat * 9);
    const carbsPercentage = (carbs * 4) / totalCalories * 100;
    const proteinPercentage = (protein * 4) / totalCalories * 100;
    return {
      background: `conic-gradient(
        #3498DB 0% ${carbsPercentage}%,
        #F1C40F ${carbsPercentage}% ${carbsPercentage + proteinPercentage}%,
        #2ECC71 ${carbsPercentage + proteinPercentage}% 100%
      )`
    };
  };



  const logItem = async (item) => {
    const requestData = {
      food_id: item.food_id,
      food_name: item.food_name,
      brand_name: item.brand_name,
      calories: item.calories,
      protein: item.protein,
      fat: item.fat,
      carbs: item.carbs
    };

    try {
      const response = await fetch("http://127.0.0.1:5000/log_item", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(requestData),
      });

      if (!response.ok) throw new Error("Failed to log item");

      console.log("Item logged:", await response.json());
      await refreshNutrition();
    } catch (error) {
      console.error("Log error:", error);
    }
  };

  const unlogItem = async (item) => {
    try {
      const response = await fetch(`http://127.0.0.1:5000/unlog_item/${item.food_id}`, {
        method: "DELETE",
        headers: { "Content-Type": "application/json" },
      });

      if (!response.ok) throw new Error("Failed to unlog item");

      console.log("Item unlogged");
      await refreshNutrition();
    } catch (error) {
      console.error("Unlog error:", error);
    }
  };

  const renderResults = () => {
    const filteredData = (data || []).filter((item) =>
      item.food_name?.toLowerCase().includes(searchQuery.toLowerCase()) ||
      item.brand_name?.toLowerCase().includes(searchQuery.toLowerCase())
    );
  
    console.log("All Restaurants:", restaurants);
  
    if (filteredData.length === 0) {
      return <p>No matching results found.</p>;
    }
  
    return filteredData.map((item) => {
      const matchedRestaurant = restaurants?.find(
        (r) => r.name.toLowerCase() === item.brand_name.toLowerCase()
      );
      const address = matchedRestaurant?.address;
  
      return (
        <div key={item.food_id} className={styles.foodItem}>
          <div className={styles.foodInfo}>
            <h3>{item.food_name}</h3>
            <h2>{item.brand_name}</h2>
            <p>
              {item.calories} cal | {item.protein}g protein | {item.carbs}g carbs | {item.fat}g fat
            </p>
            {address && <p className={styles.foodAddress}>📍 {address}</p>}
          </div>
          <div className={styles.foodActions}>
            <div className={styles.chartContainer}>
              <div
                className={styles.pieChartSmall}
                style={getPieChartStyle(item.carbs, item.protein, item.fat)}
              ></div>
              <div className={styles.innerCircle}>{item.calories} kcal</div>
            </div>
            <button
              className={`${styles.logItem} ${isLogged(item) ? styles.unlog : ""}`}
              onClick={() => isLogged(item) ? unlogItem(item) : logItem(item)}
            >
              {isLogged(item) ? "Unlog Item" : "Log Item"}
            </button>
          </div>
        </div>
      );
    });
  };
  

  const renderLoggedItems = () => {

   

    
    const items = nutritionData.logs || [];
    return items.length > 0 ? (
      items.map((item, index) => (

        
        <div key={item.food_id || index} className={styles.foodItem}>
          <div className={styles.foodInfo}>
            <h3>{item.food_name}</h3>
            <h2>{item.brand_name}</h2>
            <p>
              {item.calories} cal | {item.protein}g protein | {item.carbs}g carbs | {item.fat}g fat
            </p>
          </div>
          <div className={styles.foodActions}>
            <div className={styles.chartContainer}>
              <div
                className={styles.pieChartSmall}
                style={getPieChartStyle(item.carbs, item.protein, item.fat)}
              ></div>
              <div className={styles.innerCircle}>{item.calories} kcal</div>
            </div>
            <button className={`${styles.logItem} ${styles.unlog}`} onClick={() => unlogItem(item)}>
              Unlog Item
            </button>
          </div>
        </div>
      ))
    ) : (
      <p>No logged items found.</p>
    );
  };

  return (
    <div className={styles.results}>
      <div className={styles.tabs}>
        <button
          className={`${styles.tabBtn} ${activeTab === "results" ? styles.activeTab : ""}`}
          onClick={() => setActiveTab("results")}
        >
          Recommendations
        </button>
        <button
          className={`${styles.tabBtn} ${activeTab === "logged" ? styles.activeTab : ""}`}
          onClick={() => setActiveTab("logged")}
        >
          Logged Items
        </button>
      </div>

      {activeTab === "results" && (
        <div className={styles.searchBar}>
          <input
            type="text"
            placeholder="Search food or brand..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className={styles.searchInput}
          />
        </div>
      )}

      <div className={styles.tabContent}>
        {activeTab === "results" ? renderResults() : renderLoggedItems()}
      </div>
    </div>
  );
};

export default SecondColumn;