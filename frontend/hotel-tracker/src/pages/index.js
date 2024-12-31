import { useEffect, useState } from 'react';
import styles from '../styles/Home.module.css';

export default function Home() {
  const [hotels, setHotels] = useState([]);
  const [filteredHotels, setFilteredHotels] = useState([]);
  const [priceRange, setPriceRange] = useState([0, Infinity]);
  const [minReviewScore, setMinReviewScore] = useState(0);

  useEffect(() => {
    // Fetch the hotel data from the public directory
    fetch('/hotels_list.json')
      .then((response) => response.json())
      .then((data) => {
        setHotels(data);
        setFilteredHotels(data);
      })
      .catch((error) => console.error('Error fetching hotel data:', error));
  }, []);

  const filterHotels = () => {
    const filtered = hotels.filter((hotel) => {
      // Extract numeric values from price and review_score
      const price = parseFloat(hotel.price.replace(/[^0-9.]/g, ''));
      const reviewScore = parseFloat(hotel.review_score.split(' ')[1]);
      return price >= priceRange[0] && price <= priceRange[1] && reviewScore >= minReviewScore;
    });
    setFilteredHotels(filtered);
  };

  return (
    <div className={styles.container}>
      <h1 className={styles.header}>Hotel Listings</h1>

      {/* Filters Section */}
      <div className={styles.filters}>
        <label>
          Price Range:
          <input
            type="number"
            placeholder="Min"
            onChange={(e) => setPriceRange([+e.target.value || 0, priceRange[1]])}
          />
          <input
            type="number"
            placeholder="Max"
            onChange={(e) => setPriceRange([priceRange[0], +e.target.value || Infinity])}
          />
        </label>
        <label>
          Min Review Score:
          <input
            type="number"
            step="0.1"
            placeholder="e.g., 8.0"
            onChange={(e) => setMinReviewScore(+e.target.value || 0)}
          />
        </label>
        <button onClick={filterHotels}>Apply Filters</button>
      </div>

      {/* Hotel Counter */}
      <p className={styles.hotelCount}>
        {filteredHotels.length} hotel(s) listed
      </p>

      {/* Display Filtered Hotels */}
      {filteredHotels.length > 0 ? (
        filteredHotels.map((hotel, index) => (
          <div key={index} className={styles.hotelCard}>
            <h2 className={styles.hotelName}>{hotel.name}</h2>
            <p className={styles.hotelDetail}>
              <strong>Location:</strong> {hotel.location}
            </p>
            <p className={styles.hotelDetail}>
              <strong>Price:</strong> {hotel.price}
            </p>
            <p className={styles.hotelDetail}>
              <strong>Review Score:</strong> {hotel.review_score}
            </p>
            <p className={styles.hotelDetail}>
              <strong>Review Count:</strong> {hotel.review_count}
            </p>
            <div>
              <h4 className={styles.hotelDetail}>Details:</h4>
              <ul className={styles.detailsList}>
                {hotel.details.map((detail, i) => (
                  <li key={i}>{detail}</li>
                ))}
              </ul>
            </div>
          </div>
        ))
      ) : (
        <p>No hotels match the applied filters.</p>
      )}
    </div>
  );
}
