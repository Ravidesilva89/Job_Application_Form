import { useState } from "react";
import axios from "axios";

export default function CVUploadForm() {
  const [formData, setFormData] = useState({
    name: "",
    phoneNumber: "",
    email: "",
    cv: null,
  });
  const [message, setMessage] = useState("");

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleFileChange = (e) => {
    setFormData({ ...formData, cv: e.target.files[0] });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const data = new FormData();
    data.append("name", formData.name);
    data.append("phone_number", formData.phoneNumber);
    data.append("email", formData.email);
    data.append("cv", formData.cv);

    try {
      axios.post("http://localhost:8000/upload", data, {
        headers: { "Content-Type": "multipart/form-data" },
        timeout:1000*60
      },);
      setMessage('CV Uploaded');
      setFormData(
        {
          name: "",
          phoneNumber: "",
          email: "",
          cv: null,
        }
      )
    } catch (error) {
      setMessage("Upload failed: " + (error.response?.data?.detail || error.message));
    }
  };

  return (
    
        <div className="max-w-md mx-auto p-6 bg-white rounded-lg shadow-lg border border-gray-200">
          <h2 className="text-2xl font-semibold mb-6 text-gray-700 text-center">Upload Your CV</h2>
          {message && <p className="text-green-600 mb-4 text-center">{message}</p>}
          <form onSubmit={handleSubmit} className="space-y-4">
            <input
              type="text"
              name="name"
              placeholder="Full Name"
              value={formData.name}
              onChange={handleChange}
              className="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400"
              required
            />
            <input
              type="text"
              name="phoneNumber"
              placeholder="Phone Number"
              value={formData.phoneNumber}
              onChange={handleChange}
              className="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400"
              required
            />
            <input
              type="email"
              name="email"
              placeholder="Email Address"
              value={formData.email}
              onChange={handleChange}
              className="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400"
              required
            />
            <input
              type="file"
              accept=".pdf"
              onChange={handleFileChange}
              className="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400"
              required
            />
            <button
              type="submit"
              className="w-full bg-blue-500 text-white p-3 rounded-lg font-semibold hover:bg-blue-600 transition duration-300"
            >
              Upload CV
            </button>
          </form>
        </div>
  );
}