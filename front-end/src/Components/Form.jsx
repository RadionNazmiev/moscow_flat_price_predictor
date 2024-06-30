import React, { useState } from "react";
import * as Y from "yup";
import { Button, Checkbox, Form, Input, Select } from 'antd';

const { Option } = Select;

function useEditProfile(profile) {
  let [inputs, setInputs] = useState({
    apartment_type: profile.apartment_type || "",
    area: profile.area,
    floor: profile.floor,
    is_penthouse: profile.is_penthouse || false,
    kitchen_area: profile.kitchen_area,
    living_area: profile.living_area,
    metro_station: profile.selected_metro_station || "",
    minutes_to_metro: profile.minutes_to_metro,
    number_of_floors: profile.number_of_floors,
    number_of_rooms: profile.number_of_rooms,
    region: profile.region || "",
    renovation_type: profile.renovation_type || ""
  });
  let [errors, setErrors] = useState({});
  let [busy, setBusy] = useState(false);
  return { inputs, errors, busy, setInputs, setErrors, setBusy };
}

export default function EditProfileForm({ data }) {
  if (!data) return null;

  const metro_stations = data.metro_station || [];

  let { inputs, errors, busy, setInputs, setErrors, setBusy } = useEditProfile({
    area: "... sq m",
    floor: "1-300",
    kitchen_area: "Enter kitchen area...",
    living_area: "Enter living area",
    minutes_to_metro: "Enter how far is subway station",
    number_of_floors: "Enter how many floors",
    number_of_rooms: "Enter how many rooms",
  });

  const schema = Y.object().shape({
    // Define validation schema
  });

  async function onChange(event) {
    let { type, name, value, checked } = event.target;
    value = type === "checkbox" ? checked : value;
    let inputErrors = await schema.validateAt(name, { [name]: value }, { abortEarly: false })
      .then(() => ({ [name]: "" }))
      .catch(err => ({ [name]: err.errors.join(", ") }));
    setInputs(inputs => ({ ...inputs, [name]: value }));
    setErrors(errors => ({ ...errors, ...inputErrors }));
  }

  function onSelectApartmentType(value) {
    setInputs(inputs => ({ ...inputs, apartment_type: value }));
  }

  function onRegionChange(value) {
    setInputs(inputs => ({ ...inputs, region: value }));
  }

  function onRenovationChange(value) {
    setInputs(inputs => ({ ...inputs, renovation_type: value }));
  }

  function onMetroStationChange(value) {
    setInputs(inputs => ({ ...inputs, selected_metro_station: value }));
  }

  async function handleSubmit(values) {
    console.log(values);
    try {
      const response = await fetch('http://172.17.0.1:5000/predict_apartment_price', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(values)
      });
      const data = await response.json();
      console.log('Response from server:', data);
      alert(`Estimated Price: ${data.price}`);
    } catch (error) {
      console.error('Error:', error);
    }
  }

  return (
    <div className="p-3">
      <h1 className="h3 mb-3">Input your Preferences</h1>
      <Form autoComplete="off" style={{ maxWidth: "800px" }} onFinish={handleSubmit}>
        <Form.Item label="Area" name="area" rules={[{ required: true, message: 'Please input the area!' }]}>
          <Input type="number" value={inputs.area} onChange={onChange} />
        </Form.Item>
        <Form.Item label="Floor" name="floor" rules={[{ required: true, message: 'Please input the floor!' }]}>
          <Input type="number" value={inputs.floor} onChange={onChange} />
        </Form.Item>
        <Form.Item label="Kitchen Area" name="kitchen_area" rules={[{ required: true, message: 'Please input the kitchen area!' }]}>
          <Input type="number" value={inputs.kitchen_area} onChange={onChange} />
        </Form.Item>
        <Form.Item label="Living Area" name="living_area" rules={[{ required: true, message: 'Please input the living area!' }]}>
          <Input type="number" value={inputs.living_area} onChange={onChange} />
        </Form.Item>
        <Form.Item label="Time to get to Subway" name="minutes_to_metro" rules={[{ required: true, message: 'Please input the time to subway!' }]}>
          <Input type="number" value={inputs.minutes_to_metro} onChange={onChange} />
        </Form.Item>
        <Form.Item label="Number of Floors" name="number_of_floors" rules={[{ required: true, message: 'Please input the number of floors!' }]}>
          <Input type="number" value={inputs.number_of_floors} onChange={onChange} />
        </Form.Item>
        <Form.Item label="Number of Rooms" name="number_of_rooms" rules={[{ required: true, message: 'Please input the number of rooms!' }]}>
          <Input type="number" value={inputs.number_of_rooms} onChange={onChange} />
        </Form.Item>
        <Form.Item label="Apartment Type" name="apartment_type" rules={[{ required: true, message: 'Please select an apartment type!' }]}>
          <Select placeholder="Select an apartment type" value={inputs.apartment_type} onChange={onSelectApartmentType}>
            {data.apartment_type.map((item, index) => (
              <Option key={index} value={item}>{item}</Option>
            ))}
          </Select>
        </Form.Item>
        <Form.Item name="is_penthouse" valuePropName="checked">
          <Checkbox checked={inputs.is_penthouse} onChange={onChange}>Is Penthouse</Checkbox>
        </Form.Item>
        <Form.Item label="Region" name="region" rules={[{ required: true, message: 'Please select a region!' }]}>
          <Select placeholder="Select a region" value={inputs.region} onChange={onRegionChange}>
            {data.region.map((item, index) => (
              <Option key={index} value={item}>{item}</Option>
            ))}
          </Select>
        </Form.Item>
        <Form.Item label="Renovation Type" name="renovation_type" rules={[{ required: true, message: 'Please select a renovation type!' }]}>
          <Select placeholder="Select a renovation type" value={inputs.renovation_type} onChange={onRenovationChange}>
            {data.renovation_type.map((item, index) => (
              <Option key={index} value={item}>{item}</Option>
            ))}
          </Select>
        </Form.Item>
        <Form.Item label="Select a subway station" name="selected_metro_station" rules={[{ required: true, message: 'Please select a subway station!' }]}>
          <Select placeholder="Select an option" value={inputs.selected_metro_station} onChange={onMetroStationChange}>
            {metro_stations.map((item, index) => (
              <Option key={index} value={item}>{item}</Option>
            ))}
          </Select>
        </Form.Item>
        <Form.Item>
          <Button type="primary" htmlType="submit" disabled={busy}>
            Process {busy && <i className="fa fa-spinner fa-pulse fa-1x fa-fw"></i>}
          </Button>
        </Form.Item>
      </Form>
    </div>
  );
}
let schema = Y.object().shape({
  area: Y.number().required()
      .min(1, 'Area must be at least 1 sq m')
      .max(10000, 'Area must be at most 10,000 sq m')
      .typeError('Area must be a number'),
  floor: Y.number().required()
      .min(1, 'Floor must be at least 1')
      .max(10000, 'Floor must be at most 300')
      .typeError('Floor must be a number'),
  kitchen_area: Y.number().required()
      .min(1, 'Area must be at least 1 sq m')
      .max(10000, 'Area must be at most 1000 sq m')
      .typeError('Kitchen area must be a number'),
  living_area: Y.number().required()
      .min(1, 'Area must be at least 1 sq m')
      .max(10000, 'Area must be at most 10000 sq m')
      .typeError('Living area must be a number'),
  minutes_to_metro: Y.number().required()
      .min(1, 'Time must be at least 1 minute')
      .max(10000, 'Time must be at most 1000 minutes')
      .typeError('Time must be a number'),
  number_of_floors: Y.number().required()
      .min(1, 'Number of floors must be at least 1')
      .max(10000, 'Number of floors must be max 1000')
      .typeError('Floors must be a number'),
  number_of_rooms: Y.number().required()
      .min(1, 'Number of rooms must be at least 1')
      .max(10000, 'Number of floors must be max 100')
      .typeError('Rooms must be a number'),
  is_penthouse: Y.boolean(), // Add is_penthouse field
  apartment_type: Y.string().required('Apartment type is required'),
  region: Y.string().required('Region is required'),
  renovation_type: Y.string().required('Renovation type is required'),
  selected_metro_station: Y.string().required('Metro station is required')
})
let convert = (errors) => {
  return errors.inner.reduce((z, item) => {
    let name = (item.path || "").includes(".")
        ? item.path.split(".")[0]
        : item.path || ""
    return z[item.path || ""] ? z : {...z, [name]: item.message}
  }, {})
}

function delay(ms) {
  return new Promise((resolve, reject) => {
    setTimeout(resolve, ms)
  })
}