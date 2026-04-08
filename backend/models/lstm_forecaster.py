"""
LSTM-based Demand Forecasting Model
Based on research methodology: Time-series forecasting for demand prediction
Falls back to sklearn RandomForest if TensorFlow is not available.
"""

import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.ensemble import RandomForestRegressor
import joblib
import os

# Try to import TensorFlow, use fallback if not available
TENSORFLOW_AVAILABLE = False
try:
    from tensorflow.keras.models import Sequential, load_model
    from tensorflow.keras.layers import LSTM, Dense, Dropout
    from tensorflow.keras.optimizers import Adam
    TENSORFLOW_AVAILABLE = True
except ImportError:
    print("TensorFlow not available. Using sklearn fallback for demand forecasting.")


class LSTMDemandForecaster:
    """
    LSTM model for predicting product demand based on historical sales data.
    Implements time-series forecasting as described in the research paper.
    """
    
    def __init__(self, lookback=30, lstm_units=64, dropout_rate=0.2):
        """
        Initialize LSTM forecaster
        
        Args:
            lookback: Number of time steps to look back
            lstm_units: Number of LSTM units in each layer
            dropout_rate: Dropout rate for regularization
        """
        self.lookback = lookback
        self.lstm_units = lstm_units
        self.dropout_rate = dropout_rate
        self.model = None
        self.scaler = MinMaxScaler()
        self.is_trained = False
        self.use_tensorflow = TENSORFLOW_AVAILABLE
        
    def build_model(self, input_shape):
        """Build LSTM model architecture or sklearn fallback"""
        if self.use_tensorflow:
            model = Sequential([
                LSTM(self.lstm_units, return_sequences=True, input_shape=input_shape),
                Dropout(self.dropout_rate),
                LSTM(self.lstm_units // 2, return_sequences=False),
                Dropout(self.dropout_rate),
                Dense(32, activation='relu'),
                Dense(1)
            ])
            
            model.compile(optimizer=Adam(learning_rate=0.001),
                         loss='mse',
                         metrics=['mae'])
            
            self.model = model
        else:
            # Fallback to RandomForest for sklearn-based forecasting
            self.model = RandomForestRegressor(n_estimators=100, random_state=42)
        return self.model
    
    def prepare_sequences(self, data):
        """
        Prepare sequences for LSTM training
        
        Args:
            data: Time series data (1D array or DataFrame)
            
        Returns:
            X, y: Feature sequences and targets
        """
        if isinstance(data, pd.DataFrame):
            data = data.values
        
        # Normalize data
        scaled_data = self.scaler.fit_transform(data.reshape(-1, 1))
        
        X, y = [], []
        for i in range(self.lookback, len(scaled_data)):
            X.append(scaled_data[i-self.lookback:i, 0])
            y.append(scaled_data[i, 0])
        
        return np.array(X), np.array(y)
    
    def train(self, historical_data, epochs=50, batch_size=32, validation_split=0.2):
        """
        Train LSTM model on historical sales data
        
        Args:
            historical_data: Historical sales/demand data
            epochs: Number of training epochs
            batch_size: Batch size for training
            validation_split: Validation data split ratio
            
        Returns:
            Training history
        """
        X, y = self.prepare_sequences(historical_data)
        
        # Build model if not already built
        if self.model is None:
            if self.use_tensorflow:
                # Reshape for LSTM [samples, time steps, features]
                X_lstm = X.reshape((X.shape[0], X.shape[1], 1))
                self.build_model((X_lstm.shape[1], 1))
            else:
                self.build_model(None)
        
        if self.use_tensorflow:
            # Reshape for LSTM [samples, time steps, features]
            X = X.reshape((X.shape[0], X.shape[1], 1))
            
            # Train model
            history = self.model.fit(
                X, y,
                epochs=epochs,
                batch_size=batch_size,
                validation_split=validation_split,
                verbose=1
            )
        else:
            # Train sklearn model (no need to reshape)
            self.model.fit(X, y)
            history = None
        
        self.is_trained = True
        return history
    
    def predict(self, recent_data, steps_ahead=7):
        """
        Predict future demand
        
        Args:
            recent_data: Recent historical data (at least lookback length)
            steps_ahead: Number of future steps to predict
            
        Returns:
            Predicted demand values
        """
        if not self.is_trained:
            raise ValueError("Model must be trained before making predictions")
        
        if isinstance(recent_data, pd.DataFrame):
            recent_data = recent_data.values
        
        # Ensure we have enough data
        if len(recent_data) < self.lookback:
            raise ValueError(f"Need at least {self.lookback} data points")
        
        # Scale recent data
        scaled_data = self.scaler.transform(recent_data[-self.lookback:].reshape(-1, 1))
        
        predictions = []
        current_sequence = scaled_data.flatten().tolist()
        
        for _ in range(steps_ahead):
            # Prepare input
            X_pred = np.array(current_sequence[-self.lookback:])
            
            if self.use_tensorflow:
                X_pred = X_pred.reshape(1, self.lookback, 1)
                next_pred = self.model.predict(X_pred, verbose=0)[0, 0]
            else:
                X_pred = X_pred.reshape(1, -1)
                next_pred = self.model.predict(X_pred)[0]
            
            predictions.append(next_pred)
            
            # Update sequence
            current_sequence.append(next_pred)
        
        # Inverse transform predictions
        predictions = self.scaler.inverse_transform(np.array(predictions).reshape(-1, 1))
        
        return predictions.flatten()
    
    def save_model(self, path='models/lstm_forecaster'):
        """Save trained model and scaler"""
        if not self.is_trained:
            raise ValueError("Cannot save untrained model")
        
        os.makedirs(path, exist_ok=True)
        
        if self.use_tensorflow:
            self.model.save(f'{path}/lstm_model.h5')
        else:
            joblib.dump(self.model, f'{path}/sklearn_model.pkl')
        
        joblib.dump(self.scaler, f'{path}/scaler.pkl')
        
        # Save configuration
        config = {
            'lookback': self.lookback,
            'lstm_units': self.lstm_units,
            'dropout_rate': self.dropout_rate,
            'use_tensorflow': self.use_tensorflow
        }
        joblib.dump(config, f'{path}/config.pkl')
    
    def load_model(self, path='models/lstm_forecaster'):
        """Load trained model and scaler"""
        # Load configuration
        config = joblib.load(f'{path}/config.pkl')
        self.lookback = config['lookback']
        self.lstm_units = config['lstm_units']
        self.dropout_rate = config['dropout_rate']
        self.use_tensorflow = config.get('use_tensorflow', TENSORFLOW_AVAILABLE)
        
        if self.use_tensorflow and TENSORFLOW_AVAILABLE:
            self.model = load_model(f'{path}/lstm_model.h5')
        else:
            self.model = joblib.load(f'{path}/sklearn_model.pkl')
            self.use_tensorflow = False
        
        self.scaler = joblib.load(f'{path}/scaler.pkl')
        self.is_trained = True
    
    def evaluate_forecast_accuracy(self, actual_data, predicted_data):
        """
        Evaluate forecast accuracy using multiple metrics
        
        Args:
            actual_data: Actual demand values
            predicted_data: Predicted demand values
            
        Returns:
            Dictionary with accuracy metrics
        """
        actual = np.array(actual_data)
        predicted = np.array(predicted_data)
        
        mse = np.mean((actual - predicted) ** 2)
        rmse = np.sqrt(mse)
        mae = np.mean(np.abs(actual - predicted))
        mape = np.mean(np.abs((actual - predicted) / actual)) * 100
        
        return {
            'MSE': mse,
            'RMSE': rmse,
            'MAE': mae,
            'MAPE': mape
        }
