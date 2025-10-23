import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { makePrediction, getHistory } from '../services/api';
import '../App.css';

function Dashboard() {
  const [location, setLocation] = useState('');
  const [date, setDate] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [prediction, setPrediction] = useState(null);
  const [history, setHistory] = useState([]);
  const [historyLoading, setHistoryLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem('accessToken');
    if (!token) {
      navigate('/login');
      return;
    }

    fetchHistory();
  }, [navigate]);

  const fetchHistory = async () => {
    setHistoryLoading(true);
    try {
      const response = await getHistory();
      if (response.success) {
        setHistory(response.data.predictions);
      }
    } catch (err) {
      console.error('Failed to fetch history:', err);
    } finally {
      setHistoryLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    setPrediction(null);

    try {
      const response = await makePrediction(location, date);
      
      if (response.success) {
        setPrediction(response.data);
        fetchHistory();
      } else {
        setError(response.error || 'Prediction failed');
      }
    } catch (err) {
      setError(err.error || 'An error occurred during prediction');
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('accessToken');
    localStorage.removeItem('refreshToken');
    navigate('/login');
  };

  const today = new Date().toISOString().split('T')[0];

  return (
    <div className="dashboard">
      <div className="container">
        <div className="dashboard-header">
          <h1>Rain Prediction Dashboard</h1>
          <button onClick={handleLogout} className="logout-btn">
            Logout
          </button>
        </div>

        <div className="prediction-card">
          <h2>Make a Prediction</h2>
          
          {error && <div className="error-message">{error}</div>}
          
          <form onSubmit={handleSubmit} className="prediction-form">
            <div className="form-group">
              <label htmlFor="location">Location</label>
              <input
                type="text"
                id="location"
                value={location}
                onChange={(e) => setLocation(e.target.value)}
                required
                placeholder="Enter city name (e.g., London, New York)"
              />
            </div>
            
            <div className="form-group">
              <label htmlFor="date">Date</label>
              <input
                type="date"
                id="date"
                value={date}
                onChange={(e) => setDate(e.target.value)}
                required
                min={today}
              />
            </div>
            
            <button type="submit" className="btn" disabled={loading}>
              {loading ? 'Predicting...' : 'Get Prediction'}
            </button>
          </form>
        </div>

        {prediction && (
          <div className="prediction-result">
            <h2>Prediction Result</h2>
            <div className="result-content">
              <h3>
                {prediction.prediction === 'Rain' ? '🌧️ Rain Expected' : '☀️ No Rain Expected'}
              </h3>
              <p><strong>Location:</strong> {prediction.location}</p>
              <p><strong>Date:</strong> {prediction.date}</p>
              <p><strong>Confidence:</strong> {(prediction.confidence * 100).toFixed(0)}%</p>
              {prediction.weather_data && (
                <>
                  <p><strong>Precipitation Probability:</strong> {prediction.weather_data.precipitation_probability}%</p>
                  <p><strong>Precipitation Amount:</strong> {prediction.weather_data.precipitation_sum} mm</p>
                </>
              )}
            </div>
          </div>
        )}

        <div className="history-card">
          <h2>Prediction History</h2>
          
          {historyLoading ? (
            <div className="loading">Loading history...</div>
          ) : history.length === 0 ? (
            <div className="empty-state">
              No predictions yet. Make your first prediction above!
            </div>
          ) : (
            <ul className="history-list">
              {history.map((item) => (
                <li key={item.id} className="history-item">
                  <div className="history-item-header">
                    <span className="history-item-location">
                      {item.location}
                    </span>
                    <span className={`history-item-result ${
                      item.prediction_result === 'Rain' ? 'result-rain' : 'result-no-rain'
                    }`}>
                      {item.prediction_result === 'Rain' ? '🌧️ Rain' : '☀️ No Rain'}
                    </span>
                  </div>
                  <div className="history-item-date">
                    <strong>Date:</strong> {item.date} | 
                    <strong> Predicted on:</strong> {new Date(item.created_at).toLocaleString()} |
                    <strong> Confidence:</strong> {(item.confidence * 100).toFixed(0)}%
                  </div>
                </li>
              ))}
            </ul>
          )}
        </div>
      </div>
    </div>
  );
}

export default Dashboard;
