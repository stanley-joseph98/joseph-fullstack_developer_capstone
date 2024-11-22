// Dealer.jsx
import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import "./Dealers.css";
import "../assets/style.css";
import positive_icon from "../assets/positive.png";
import neutral_icon from "../assets/neutral.png";
import negative_icon from "../assets/negative.png";
import review_icon from "../assets/reviewbutton.png";
import Header from '../Header/Header';
import ErrorBoundary from './ErrorBoundary';

const Dealer = () => {
  const [dealer, setDealer] = useState({
    full_name: "",
    city: "",
    address: "",
    zip: "",
    state: "",
  });
  const [reviews, setReviews] = useState([]);
  const [unreviewed, setUnreviewed] = useState(false);
  const [postReview, setPostReview] = useState(null);

  const params = useParams();
  const id = params.id;

  const curr_url = window.location.href;
  const root_url = curr_url.substring(0, curr_url.indexOf("dealer"));
  const dealer_url = `${root_url}djangoapp/dealer/${id}`;
  const reviews_url = `${root_url}djangoapp/reviews/dealer/${id}`;
  const post_review_url = `${root_url}postreview/${id}`;

  const getDealer = async () => {
    try {
      const res = await fetch(dealer_url, { method: "GET" });
      const retobj = await res.json();
      if (res.ok && retobj.dealer.length > 0) {
        setDealer(retobj.dealer[0]);
      } else {
        console.error("Dealer data not found:", retobj);
      }
    } catch (error) {
      console.error("Error fetching dealer data:", error);
    }
  };

  const getReviews = async () => {
    try {
      const res = await fetch(reviews_url, { method: "GET" });
      const retobj = await res.json();
      if (res.ok) {
        if (retobj.reviews.length > 0) {
          setReviews(retobj.reviews);
        } else {
          setUnreviewed(true);
        }
      } else {
        console.error("Error fetching reviews:", retobj);
      }
    } catch (error) {
      console.error("Error fetching reviews:", error);
    }
  };

  const sentimentIcon = (sentiment) => {
    return sentiment === "positive"
      ? positive_icon
      : sentiment === "negative"
      ? negative_icon
      : neutral_icon;
  };

  useEffect(() => {
    if (id) {
      getDealer();
      getReviews();
      if (sessionStorage.getItem("username")) {
        setPostReview(
          <a href={post_review_url} className="review_icon">
            <img
              src={review_icon}
              alt="Post Review"
              className="review_icon"
            />
          </a>
        );
      }
    } else {
      console.error("Dealer ID is missing.");
    }
  }, [id]);

  return (
    <ErrorBoundary>
      <div className="container">
        <Header />
        <div className="banner">
          <h1 className="title">
            {dealer.full_name || "Dealer not found"}
            {postReview}
          </h1>
          <h4 className="details">
            {dealer.city}, {dealer.address}, Zip - {dealer.zip}, {dealer.state}
          </h4>
        </div>
        <div className="reviews_panel">
          {reviews.length === 0 && !unreviewed ? (
            <p>Loading Reviews...</p>
          ) : unreviewed ? (
            <div className="small_header">No reviews yet!</div>
          ) : (
            reviews.map((review, index) => (
              <div className="review_panel" key={index}>
                <img
                  src={sentimentIcon(review.sentiment)}
                  className="emotion_icon"
                  alt="Sentiment"
                />
                <div className="review">{review.review}</div>
                <div className="reviewer">
                  {review.name} {review.car_make} {review.car_model} {review.car_year}
                </div>
              </div>
            ))
          )}
        </div>
      </div>
    </ErrorBoundary>
  );
};

export default Dealer;