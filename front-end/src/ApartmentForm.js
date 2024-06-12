import React from "react";
import axios from 'axios';

const ApartmentForm = () => {
  axios.get('http://localhost:5000')
  .then(response => {
    console.log(response.data); 
  })
  .catch(error => {
    console.error('Error:', error);
  });
  


  return (
    <div
      style={{
        maxWidth: "600px",
        margin: "0 auto",
        padding: "20px",
        border: "1px solid #ccc",
        borderRadius: "10px",
      }}
    >
      <h2>Apartment Information</h2>

    </div>
  );
};

export default ApartmentForm;
