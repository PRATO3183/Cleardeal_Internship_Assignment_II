from fastapi import APIRouter, HTTPException
from ....model.lead import LeadInput, LeadOutput
from ....services.scoring_service import scoring_service

router = APIRouter()

# In-memory storage for scored leads
scored_leads_db = []

@router.post("/score", response_model=LeadOutput)
def score_lead(lead_input: LeadInput):
    """
    Accepts lead data, computes an initial score, applies a re-ranker,
    and returns the results.
    """
    try:
        # 1. Get initial score from the ML model
        initial_score = scoring_service.predict(lead_input)
        
        # 2. Apply the rule-based re-ranker
        reranked_score = scoring_service.rerank_score(initial_score, lead_input.Comments)
        
        # 3. Create the response object
        result = LeadOutput(
            Email=lead_input.Email,
            InitialScore=initial_score,
            RerankedScore=reranked_score,
            Comments=lead_input.Comments
        )
        
        # 4. Store the result in memory (for demonstration)
        scored_leads_db.append(result)
        
        return result
        
    except Exception as e:
        # Log the error for debugging
        print(f"An error occurred during scoring: {e}")
        raise HTTPException(
            status_code=500, 
            detail="An internal error occurred while processing the lead."
        )

@router.get("/leads", response_model=list[LeadOutput])
def get_all_leads():
    """
    Returns all the leads that have been scored in the current session.
    """
    return scored_leads_db