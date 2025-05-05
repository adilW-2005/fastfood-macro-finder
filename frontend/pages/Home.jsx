import React, { useState, useEffect } from 'react';
import FirstColumn from '../components/FirstColumn';
import SecondColumn from '../components/SecondColumn';
import ThirdColumn from '../components/ThirdColumn';

const Home = () => {
  
    const [data, setData] = useState(null);
    const [restaurants, setRestaurants] = useState([]);
    const [userLocation, setUserLocation] = useState({ lat: 30.2849, lng: -97.7341 });
    const [nutritionData, setNutritionData] = useState({
      totalCalories: 0,
      totalProtein: 0,
      totalCarbs: 0,
      totalFat: 0
    });
  
    const userId = 1;
  
  
  
    const refreshNutrition = async () => {
      try {
          const response = await fetch(`http://127.0.0.1:5000/user_nutrition`);
          const result = await response.json();
          console.log("Updated Nutrition Data:", result);
  
          setNutritionData({
              totalCalories: result.totalCalories,
              totalProtein: result.totalProtein,
              totalCarbs: result.totalCarbs,
              totalFat: result.totalFat,
              logs: result.logs || []
          });
  
      } catch (error) {
          console.error("Error fetching user nutrition:", error);
      }
  };
  
    useEffect(() => {
      refreshNutrition();
    }, []);
    
    return (
      <div className="container">
          
        <FirstColumn setData={setData} setRestaurants={setRestaurants} setUserLocation={setUserLocation}/>
        
  
        <SecondColumn data={data} nutritionData={nutritionData} setNutritionData={setNutritionData} userId={userId} refreshNutrition={refreshNutrition} restaurants={restaurants}/>
        
        <ThirdColumn key={JSON.stringify(nutritionData)} nutritionData={nutritionData} restaurants={restaurants} userLocation={userLocation}/>
  
      </div>
      
    )
  }
  
  
  export default Home
