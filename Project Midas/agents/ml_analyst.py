import pandas as pd
import numpy as np
import sys

# Path Hacking
sys.path.append(r"c:\Users\z143d\OneDrive\Desktop\Project Aergia")
sys.path.append(r"c:\Users\z143d\OneDrive\Desktop\Project Aergia\Project Midas")

try:
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import accuracy_score
except ImportError:
    print("scikit-learn not installed.")

class MLAnalyst:
    """
    Blueprint Section 1.3: Signal Generation & Prediction Agent
    Role: Probabilistic Oracle using Random Forest
    """
    def __init__(self):
        try:
            self.model = RandomForestClassifier(n_estimators=100, random_state=42)
            self.active = True
        except NameError:
            print("ML Analyst Warning: Sklearn not found. Using Fallback.")
            self.model = None
            self.active = False
        
    def generate_probability(self, snapshot):
        """
        Trains a model ON THE FLY using the provided history and predicts the next move.
        Returns: { "direction": "UP/DOWN", "probability": 0-100 }
        """
        print(f"--- ML Analyst: Crunching Numbers for {snapshot['ticker']} ---")
        
        if not self.active:
             return {"direction": "UNKNOWN (ML Offline)", "probability": 50.0}

        df = snapshot.get('daily_candles')
        if df is None or df.empty or len(df) < 50:
            return {"direction": "UNKNOWN", "probability": 50.0}
            
        # 1. Feature Engineering
        # We need to create features that predict the 'Target'
        data = df.copy()
        
        # Simple Features suitable for daily data
        data['Returns'] = data['close'].pct_change()
        data['Range'] = (data['high'] - data['low']) / data['close']
        data['Vol_Ratio'] = data['volume'] / data['volume'].rolling(5).mean()
        
        # Lagged Features (The info we actually have at time t)
        data['Ret_Lag1'] = data['Returns'].shift(1)
        data['Ret_Lag2'] = data['Returns'].shift(2)
        data['Vol_Lag1'] = data['Vol_Ratio'].shift(1)
        
        data.dropna(inplace=True)
        
        # 2. Target Creation
        # Target: Did close rise the NEXT day? 
        # We shift returns BACKWARDS (-1) to align "Today's Features" with "Tomorrow's Outcome"
        data['Target'] = (data['Returns'].shift(-1) > 0).astype(int)
        
        # Drop the last row because it has no target (we don't know tomorrow yet)
        train_data = data_clean = data[:-1]
        
        features = ['Ret_Lag1', 'Ret_Lag2', 'Vol_Lag1', 'Range']
        X = train_data[features]
        y = train_data['Target']
        
        if len(X) < 30:
            return {"direction": "INSUFFICIENT_DATA", "probability": 50.0}

        # 3. Train the Model (The "Oracle" learns *this* stock's recent behavior)
        self.model.fit(X, y)
        
        # 4. Predict for TODAY (The row we dropped earlier, but now using its features)
        # We want to predict if TOMORROW will be up based on TODAY's data.
        # The 'last_row' of 'data' (before drop) contains today's closed features.
        today_features = data.iloc[[-1]][features]
        
        prediction = self.model.predict(today_features)[0]
        probs = self.model.predict_proba(today_features)
        
        # Safety Check: If model only learned one class (e.g. only UP), predict_proba has 1 column
        if probs.shape[1] == 2:
            prob = probs[0][1] * 100
        else:
            # If only one class, look at that class
            only_class = self.model.classes_[0]
            prob = 100.0 if only_class == 1 else 0.0
            
        direction = "UP" if prediction == 1 else "DOWN"
        
        return {
            "direction": direction,
            "probability": round(prob, 1),
            "model_accuracy": "N/A (Live Training)"
        }

if __name__ == "__main__":
    # Test Stub
    # Create fake candle data
    dates = pd.date_range(start='2025-01-01', periods=100)
    closes = np.random.normal(100, 2, 100).cumsum()
    vols = np.random.randint(1000, 5000, 100)
    mock_df = pd.DataFrame({'close': closes, 'high': closes+1, 'low': closes-1, 'volume': vols}, index=dates)
    
    mock_snapshot = {"ticker": "TEST", "daily_candles": mock_df}
    
    agent = MLAnalyst()
    print(agent.generate_probability(mock_snapshot))
