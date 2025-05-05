import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <App />
  </StrictMode>,
)



// import React, { useState } from "react";

// function App() {
//   const [location, setLocation] = useState("");
//   const [maxCalories, setMaxCalories] = useState("");
//   const [minProtein, setMinProtein] = useState("");
//   const [radius, setRadius] = useState("");
//   const [data, setData] = useState(null);
//   const [error, setError] = useState(null);

//   // ✅ Fetch data from Flask backend
//   const fetchData = async () => {
    

//     const requestData = {
//       location: location.trim(),
//       max_calories: maxCalories ? parseInt(maxCalories, 10) : null,
//       min_protein: minProtein ? parseInt(minProtein, 10) : null,
//       radius_search: radius ? parseInt(radius, 10) : 1000, 
//     };

//     console.log("📡 Sending POST request to Flask API with payload:", requestData);

//     const response = await fetch("http://127.0.0.1:5000/recommendations", {
//         method: "POST",
//         mode: "cors",
//         headers: {
//           "Content-Type": "application/json",
//         },
//         body: JSON.stringify(requestData),
//       });

//       const result = await response.json();
//       console.log("✅ API Response:", result);

//       // ✅ Update UI with data
//       setData({
//         message: result.message || "No message",
//         location: result.location || "Unknown Location",
//         brand_names: result.brand_names || [],  // Default to empty array
//         restaurants: result.restaurants || [],
//         food_name: result.food_name || [],  // Default to empty array
//       });
//     } 

//   return (
//     <div style={{ padding: "20px", fontFamily: "Arial, sans-serif" }}>
//       <h1>Healthy Fast Food Finder</h1>

//       {/* User Input Form */}
//       <div style={{ marginBottom: "10px" }}>
//         <input
//           type="text"
//           placeholder="Enter Location"
//           value={location}
//           onChange={(e) => setLocation(e.target.value)}
//           style={{ marginRight: "5px" }}
//         />
//         <input
//           type="number"
//           placeholder="Max Calories"
//           value={maxCalories}
//           onChange={(e) => setMaxCalories(e.target.value)}
//           style={{ marginRight: "5px" }}
//         />
//         <input
//           type="number"
//           placeholder="Min Protein"
//           value={minProtein}
//           onChange={(e) => setMinProtein(e.target.value)}
//           style={{ marginRight: "5px" }}
//         />
//         <input
//           type="number"
//           placeholder="Search Radius (meters)"
//           value={radius}
//           onChange={(e) => setRadius(e.target.value)}
//         />
//       </div>

//       <button
//         onClick={fetchData}
//         style={{ padding: "10px", cursor: "pointer", marginTop: "10px" }}
//       >
//         Get Recommendations
//       </button>

//       {/* Display API Response */}
//       {data && (
//         <div style={{ marginTop: "20px" }}>
//           <h2>Results for {data.location}</h2>

//           <h3>Restaurants:</h3>
//           {data.brand_names.length > 0 ? (
//             <ul>
//               {data.brand_names.map((name, index) => (
//                 <li key={index}>{name}</li>
//               ))}
//             </ul>
//           ) : (
//             <p>No restaurants found.</p>
//           )}

//           <h3>Recommended Menu Items:</h3>
//           {data.restaurants.length > 0 ? (
//             <ul>
//               {data.restaurants.map((item, index) => (
//                 <li key={index}>
//                   {item.restaurant_name}: {item.food_name} - {item.calories} cal, {item.protein}g protein
//                 </li>
//               ))}
//             </ul>
//           ) : (
//             <p>No menu items found.</p>
//           )}
//         </div>
//       )}
//     </div>
//   );
// }

// export default App;
