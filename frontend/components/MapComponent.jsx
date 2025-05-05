import React from "react";
import { GoogleMap, LoadScript, Marker } from "@react-google-maps/api";

const containerStyle = {
  width: "100%",
  height: "350px"
};

const token = import.meta.env.googleMapsApiKey;


const MapComponent = ({ restaurants = [], userLocation }) => {
    return (
        <LoadScript googleMapsApiKey={googleMapsApiKey}>
            <GoogleMap mapContainerStyle={containerStyle} center={userLocation} zoom={12}>
                
                {/* ✅ User Location Marker */}
                <Marker position={userLocation} icon="http://maps.google.com/mapfiles/ms/icons/blue-dot.png" />

                {/* ✅ Restaurant Markers (Ensure restaurants exists) */}
                {restaurants.length > 0 ? (
                    restaurants.map((restaurant, index) => (
                        <Marker key={index} position={{ lat: restaurant.latitude, lng: restaurant.longitude }} />
                    ))
                ) : (
                    console.log("No restaurants to display on the map.")
                )}
            </GoogleMap>
        </LoadScript>
    );
};

export default MapComponent;
