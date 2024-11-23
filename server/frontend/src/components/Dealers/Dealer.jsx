import React, { useState, useEffect } from "react";
import "./Dealers.css";

const Dealers = () => {
  const [dealersList, setDealersList] = useState([]);
  const [originalDealers, setOriginalDealers] = useState([]);
  const [searchQuery, setSearchQuery] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const getDealers = async () => {
      setLoading(true);
      try {
        const res = await fetch("/api/dealers");
        if (!res.ok) {
          throw new Error(`Server error: ${res.status}`);
        }
        const data = await res.json();
        console.log("Fetched Dealers:", data); // Debug API data
        setOriginalDealers(data);
        setDealersList(data);
      } catch (error) {
        console.error("Error fetching dealers:", error);
      } finally {
        setLoading(false);
      }
    };

    getDealers();
  }, []);

  const handleInputChange = (event) => {
    const query = event.target.value;
    setSearchQuery(query);
    const filtered = originalDealers.filter((dealer) =>
      dealer.state?.toLowerCase().includes(query.toLowerCase())
    );
    setDealersList(filtered);
  };

  const handleLostFocus = () => {
    if (!searchQuery) {
      setTimeout(() => setDealersList(originalDealers), 200);
    }
  };

  return (
    <div className="dealers-container">
      <h1>Dealerships</h1>
      <input
        type="text"
        placeholder="Search states..."
        value={searchQuery}
        onChange={handleInputChange}
        onBlur={handleLostFocus}
        className="search-box"
      />
      <div className="dealers-list">
        {loading ? (
          <p>Loading dealerships...</p>
        ) : dealersList.length > 0 ? (
          dealersList.map((dealer, index) => (
            <div key={dealer.id || index} className="dealer-item">
              <h3>{dealer.full_name}</h3>
              <p>{dealer.city}, {dealer.state}</p>
              <p>{dealer.address}</p>
              {dealer.id ? (
                <a href={`/searchcars/${dealer.id}`}>SearchCars</a>
              ) : (
                <p>ID not available</p>
              )}
            </div>
          ))
        ) : (
          <p>No dealerships found.</p>
        )}
      </div>
    </div>
  );
};

export default Dealers;
