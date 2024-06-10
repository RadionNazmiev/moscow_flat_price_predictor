import React from "react"

const ApartmentFormItem = () => {
  return (
    <div style={{ marginBottom: "10px" }}>
        <label>
        Apartment Type:
        <select
            name="apartment_type"
            value={formData.apartment_type}
            onChange={handleChange}
        >
            <option value="">Select Apartment Type</option>
            {apartmentTypes.map((type) => (
            <option key={type} value={type}>
                {type}
            </option>
            ))}
        </select>
        </label>
    </div> 
  )
}