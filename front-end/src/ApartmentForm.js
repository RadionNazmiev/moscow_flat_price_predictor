import React, { useState } from "react";
import axios from 'axios';
import ApartmentFormItem from './ApartmentFormItem'; 

const ApartmentForm = () => {
  axios.get('http://localhost:5000')
  .then(response => {
    console.log(response.data); 
  })
  .catch(error => {
    console.error('Error:', error);
  });
  
  const [formData, setFormData] = useState({
    apartment_type: "",
    metro_station: "",
    minutes_to_metro: "",
    region: "",
    number_of_rooms: "",
    area: "",
    living_area: "",
    kitchen_area: "",
    floor: "",
    number_of_floors: "",
    renovation_type: "",
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value,
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log(formData);
  };

  if (!formInfo) {
    return <div>Loading...</div>;
  }

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
      <form onSubmit={handleSubmit}>
        {formInfo.map((item, index) => (
          <ApartmentFormItem
            key={index}
            item={item}
            value={formData[item.name]}
            onChange={handleChange}
          />
        ))}

        <button
          type="submit"
          style={{
            padding: "10px 20px",
            border: "none",
            backgroundColor: "#28a745",
            color: "#fff",
            borderRadius: "5px",
          }}
        >
          Submit
        </button>
      </form>
    </div>
  );
};

export default ApartmentForm;
