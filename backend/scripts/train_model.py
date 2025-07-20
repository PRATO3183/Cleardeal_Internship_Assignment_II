import pandas as pd
import joblib
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report

def train_model():
    """Trains the lead scoring model and saves the artifacts."""
    
    # --- 1. Load Data ---
    try:
        data_path = "../data/synthetic_leads.csv"
        df = pd.read_csv(data_path)
    except FileNotFoundError:
        print(f"Error: Data file not found at {data_path}")
        print("Please run 'scripts/generate_data.py' first.")
        return

    # --- 2. Define Features and Target ---
    TARGET = 'High_Intent'
    
    # Define categorical and numerical features
    categorical_features = ['AgeGroup', 'FamilyBackground', 'LeadSource']
    numerical_features = ['CreditScore', 'Income', 'TimeOnPage', 'PagesVisited']
    
    features = categorical_features + numerical_features
    
    X = df[features]
    y = df[TARGET]

    # --- 3. Preprocessing ---
    # Create a preprocessor to handle different feature types
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), numerical_features),
            ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
        ],
        remainder='passthrough' # Keep other columns if any
    )

    # --- 4. Define the Model ---
    # We use GradientBoostingClassifier as it's robust and effective
    model = GradientBoostingClassifier(
        n_estimators=100,
        learning_rate=0.1,
        max_depth=3,
        random_state=42
    )

    # --- 5. Create the Pipeline ---
    # The pipeline chains the preprocessor and the model
    pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('classifier', model)
    ])

    # --- 6. Split Data and Train ---
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    print("Training the model...")
    pipeline.fit(X_train, y_train)
    print("Training complete.")

    # --- 7. Evaluate the Model ---
    print("\nEvaluating model performance on the test set:")
    y_pred = pipeline.predict(X_test)
    print(classification_report(y_test, y_pred))

    # --- 8. Save the Pipeline ---
    # The pipeline object contains both the preprocessor and the trained model
    output_dir = "../model"
    os.makedirs(output_dir, exist_ok=True)
    
    model_path = os.path.join(output_dir, "intent_model_pipeline.pkl")
    joblib.dump(pipeline, model_path)
    
    print(f"\nModel pipeline saved successfully to: {model_path}")

if __name__ == "__main__":
    train_model()