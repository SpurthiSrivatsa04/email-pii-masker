from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
from utils import mask_pii  # Custom utility for PII masking


# Define the request model for email input
class EmailRequest(BaseModel):
    input_email_body: str


# Initialize FastAPI application
app = FastAPI(
    title="Email Classification API",
    description="API to classify emails and mask PII data",
    version="1.0.0",
)


# Load the pre-trained model and vectorizer at startup
try:
    model, vectorizer = joblib.load("model/classifier.pkl")
except FileNotFoundError:
    # Raise an HTTP exception if model loading fails
    raise HTTPException(
        status_code=500,
        detail="Model file not found. Ensure 'model/classifier.pkl' exists."
    )


@app.post(
    "/",
    response_description="Classify email, mask PII, return category",
)
async def classify_email(email: EmailRequest):
    """
    Classify an email based on its content and mask sensitive PII data.

    Args:
        email (EmailRequest): Request body containing the input email text.

    Returns:
        dict: Holds email, masked email, PII entities, and category.

    Raises:
        HTTPException: If model prediction or PII masking fails.
    """
    # Extract raw email content from request
    raw_email = email.input_email_body

    # Apply PII masking to protect sensitive information
    masked_email, entities = mask_pii(raw_email)

    # Transform masked email for model prediction
    transformed_email = vectorizer.transform([masked_email])

    # Predict email category using the loaded model
    predicted_category = model.predict(transformed_email)[0]

    # Return response with all required details
    return {
        "input_email_body": raw_email,
        "list_of_masked_entities": entities,
        "masked_email": masked_email,
        "category_of_the_email": predicted_category,
    }
