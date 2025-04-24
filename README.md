## Setup Instructions
1. **Clone the Repository**
   ```bash
   git clone https://github.com/SpurthiSrivatsa04/email-pii-masker/
   cd email-pii-masker
   ```

2. **Set Up Virtual Environment**
   Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```
   Ensure `requirements.txt` includes:
   ```
   fastapi
   uvicorn
   pandas
   scikit-learn
   joblib
   openpyxl
   ```

4. **Prepare the Dataset**
   - Place `combined_emails_with_natural_pii.xlsx` in the `data/` directory.
   - This file should contain columns `email` (text) and `type` (labels).

5. **Train the Model**
   Run the training script to generate the model file:
   ```bash
   python models.py
   ```
   This will create `model/classifier.pkl` in the `model/` directory and print the model accuracy.

6. **Run the Application**
   Start the FastAPI server:
   ```bash
   python app.py
   ```
   The server will run on `http://127.0.0.1:8000/`.

## Usage Instructions
### API Endpoint
- **POST `/`**
  - **Request Body**: JSON with `input_email_body` (e.g., `{"input_email_body": "Your email text here"}`).
  - **Response**: JSON with `input_email_body`, `list_of_masked_entities`, `masked_email`, and `category_of_the_email`.
  - **Example**:
    ```bash
    curl -X POST "http://127.0.0.1:8000/" -H "Content-Type: application/json" -d '{"input_email_body": "My name is John Doe, and my Aadhar number is 1234 5678 9123,"}'
    ```
    Expected response:
    ```json
    {
      "input_email_body": "My name is John Doe, and my Aadhar number is 1234 5678 9123",
      "list_of_masked_entities": [
        {
          "position": [
            11,
            19
          ],
          "classification": "full_name",
          "entity": "John Doe"
        },
        {
          "position": [
            45,
            59
          ],
          "classification": "aadhar_num",
          "entity": "1234 5678 9123"
        }
      ],
      "masked_email": "My name is [full_name], and my Aadhar number is [aadhar_num]",
      "category_of_the_email": "Incident"
    }
    ```

### Notes
- The model predicts email categories based on the trained classifier.
- PII (e.g., names, credit card numbers) is masked using regex patterns defined in `utils.py`.
- Ensure `model/classifier.pkl` exists before running the API, or train it first with `train.py`.
