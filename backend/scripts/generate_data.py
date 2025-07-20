import pandas as pd
import numpy as np
from faker import Faker
import os

# Initialize Faker
fake = Faker('en_IN')

# Define the number of records
NUM_ROWS = 10000

# Define lists for categorical data
AGE_GROUPS = ["18-25", "26-35", "36-50", "51+"]
FAMILY_BACKGROUNDS = ["Single", "Married", "Married with Kids"]
LEAD_SOURCES = ["Organic Search", "Paid Ads", "Referral", "Social Media", "Direct"]

def create_dataset(num_rows):
    """Generates a synthetic dataset of leads."""
    data = []
    for _ in range(num_rows):
        age_group = np.random.choice(AGE_GROUPS, p=[0.2, 0.4, 0.3, 0.1])
        family_bg = np.random.choice(FAMILY_BACKGROUNDS, p=[0.3, 0.4, 0.3])
        
        # Generate income based on age and family background
        income_base = 100000
        if "26-35" in age_group:
            income_base = 250000
        elif "36-50" in age_group:
            income_base = 500000
        elif "51+" in age_group:
            income_base = 400000
        
        if "Married" in family_bg:
            income_base *= 1.2
        
        income = int(np.random.normal(loc=income_base, scale=50000))
        
        # Generate credit score based on income
        credit_score_base = 300 + (income / 100000) * 50
        credit_score = int(np.random.normal(loc=credit_score_base, scale=50))
        credit_score = max(300, min(850, credit_score))

        data.append({
            "PhoneNumber": fake.phone_number(),
            "Email": fake.email(),
            "CreditScore": credit_score,
            "AgeGroup": age_group,
            "FamilyBackground": family_bg,
            "Income": income,
            "LeadSource": np.random.choice(LEAD_SOURCES),
            "TimeOnPage": int(np.random.uniform(10, 300)), # seconds
            "PagesVisited": int(np.random.uniform(1, 15)),
        })
    return pd.DataFrame(data)

def create_target_variable(df):
    """Creates the 'High_Intent' target variable based on defined rules."""
    conditions = [
        (df['CreditScore'] > 700) & (df['Income'] > 600000) & (df['PagesVisited'] > 8),
        (df['CreditScore'] > 650) & (df['TimeOnPage'] > 180) & (df['AgeGroup'] == '36-50'),
        (df['Income'] > 800000) | (df['CreditScore'] > 750),
        (df['FamilyBackground'] == 'Married with Kids') & (df['Income'] > 500000)
    ]
    
    # Assign a probability of being high intent based on conditions
    probabilities = np.zeros(len(df))
    probabilities[conditions[0]] = 0.85
    probabilities[conditions[1]] = 0.75
    probabilities[conditions[2]] = 0.70
    probabilities[conditions[3]] = 0.65
    
    # Add some noise
    noise = np.random.uniform(0, 0.25, len(df))
    final_probabilities = np.clip(probabilities + noise, 0, 1)

    # Create binary target variable
    df['High_Intent'] = (final_probabilities > 0.6).astype(int)
    return df

if __name__ == "__main__":
    print("Generating synthetic dataset...")
    
    # Create directory if it doesn't exist
    output_dir = "../data"
    os.makedirs(output_dir, exist_ok=True)
    
    leads_df = create_dataset(NUM_ROWS)
    leads_df_with_target = create_target_variable(leads_df)
    
    output_path = os.path.join(output_dir, "synthetic_leads.csv")
    leads_df_with_target.to_csv(output_path, index=False)
    
    print(f"Successfully created {NUM_ROWS} records.")
    print(f"Dataset saved to: {output_path}")
    print("\nHigh Intent Distribution:")
    print(leads_df_with_target['High_Intent'].value_counts(normalize=True))