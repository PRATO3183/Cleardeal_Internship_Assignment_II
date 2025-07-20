import joblib
import pandas as pd
from pathlib import Path
from ..model.lead import LeadInput

class ScoringService:
    """Handles loading the model and scoring leads."""
    _model = None
    _model_path = Path(__file__).parent.parent.parent / "model/intent_model_pipeline.pkl"

    @classmethod
    def get_model(cls):
        """Loads the trained model pipeline from disk."""
        if cls._model is None:
            try:
                print(f"Loading model from: {cls._model_path}")
                cls._model = joblib.load(cls._model_path)
                print("Model loaded successfully.")
            except FileNotFoundError:
                print(f"Error: Model file not found at {cls._model_path}")
                raise
        return cls._model

    @staticmethod
    def predict(lead_data: LeadInput) -> int:
        """
        Generates an initial intent score (0-100) for a lead.
        """
        model = ScoringService.get_model()
        
        # Convert Pydantic model to a DataFrame for prediction
        input_df = pd.DataFrame([lead_data.dict(exclude={'Comments'})])
        
        # Predict the probability of the positive class (High_Intent=1)
        # The output of predict_proba is an array like [[prob_class_0, prob_class_1]]
        probability = model.predict_proba(input_df)[0][1]
        
        # Scale the probability to a score of 0-100
        initial_score = int(probability * 100)
        
        return initial_score

    @staticmethod
    def rerank_score(initial_score: int, comments: str) -> int:
        """
        Adjusts the score based on keywords in the comments.
        This simulates a rule-based LLM re-ranker.
        """
        reranked_score = initial_score
        lower_comments = comments.lower()

        # Define keyword rules and their impact on the score
        rules = {
            "urgent": 20,
            "immediate": 20,
            "asap": 15,
            "serious": 15,
            "ready to buy": 25,
            "appointment": 10,
            "schedule a call": 10,
            "not interested": -30,
            "unsubscribe": -50,
            "spam": -40,
            "just browsing": -15,
            "researching": -10,
        }

        for keyword, adjustment in rules.items():
            if keyword in lower_comments:
                reranked_score += adjustment
        
        # Cap the score between 0 and 100
        final_score = max(0, min(100, reranked_score))
        
        return final_score

scoring_service = ScoringService()