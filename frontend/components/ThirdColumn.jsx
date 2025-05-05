import React, { useEffect, useState } from 'react';
import MapComponent from './MapComponent';
import { Link, useNavigate } from 'react-router-dom';
import styles from './ThirdColumn.module.css';

const ThirdColumn = ({ nutritionData, restaurants, userLocation }) => {
  const navigate = useNavigate();
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [userData, setUserData] = useState(null);
  const [pieChartStyle, setPieChartStyle] = useState({ background: "#ccc" });

  const fetchUserSession = async () => {
    try {
      const response = await fetch("http://127.0.0.1:5000/auth/check_session", {
        method: "GET",
        credentials: "include",
      });

      const result = await response.json();
      if (response.ok) {
        setIsLoggedIn(true);
        setUserData({ user_id: result.user_id });
      } else {
        setIsLoggedIn(false);
        setUserData(null);
      }
    } catch (error) {
      console.error("Session error:", error);
      setIsLoggedIn(false);
    }
  };

  const handleLogout = async () => {
    try {
      await fetch("http://127.0.0.1:5000/auth/logout", {
        method: "POST",
        credentials: "include",
      });
      localStorage.removeItem("user");
      setIsLoggedIn(false);
      navigate("/");
    } catch (error) {
      console.error("Logout failed:", error);
    }
  };

  useEffect(() => {
    fetchUserSession();
  }, []);

  const {
    totalCarbs = 0,
    totalProtein = 0,
    totalFat = 0,
    totalCalories = 0,
  } = nutritionData || {};

  useEffect(() => {
    const total = totalCarbs * 4 + totalProtein * 4 + totalFat * 9;
    if (total === 0) {
      setPieChartStyle({ background: "#ccc" });
      return;
    }
    const carbsPct = (totalCarbs * 4) / total * 100;
    const proteinPct = (totalProtein * 4) / total * 100;
    const fatPct = (totalFat * 9) / total * 100;
    setPieChartStyle({
      background: `conic-gradient(
        #3498DB 0% ${carbsPct}%,
        #F1C40F ${carbsPct}% ${carbsPct + proteinPct}%,
        #2ECC71 ${carbsPct + proteinPct}% 100%
      )`
    });
  }, [totalCarbs, totalProtein, totalFat]);

  return (
    <aside className={styles.dashboard}>
      {isLoggedIn ? (
        <button className={styles.signIn} onClick={handleLogout}>Logout</button>
      ) : (
        <Link to="/login">
          <button className={styles.signIn}>New User / Sign In</button>
        </Link>
      )}
      <h2>Nutrition Dashboard</h2>
      <div className={styles.pieChart} key={JSON.stringify(pieChartStyle)} style={pieChartStyle}>
        <div className={styles.chartDashboard}>
          <div className={styles.innerCircleDashboard}>{totalCalories} kcal</div>
        </div>
      </div>

      <div className={styles.legend}>
        <div className={styles.legendItem}><span className={`${styles.legendColor} ${styles.carbs}`}></span> Carbs: <strong>{totalCarbs} g</strong></div>
        <div className={styles.legendItem}><span className={`${styles.legendColor} ${styles.protein}`}></span> Protein: <strong>{totalProtein} g</strong></div>
        <div className={styles.legendItem}><span className={`${styles.legendColor} ${styles.fat}`}></span> Fat: <strong>{totalFat} g</strong></div>
      </div>

      <h2>Food Locations</h2>
      <div className={styles.mapWrapper}>
        <MapComponent restaurants={restaurants} userLocation={userLocation} />
      </div>
    </aside>
  );
};

export default ThirdColumn;
