# Named-Entity-Recognition Project

This project is designed for Named Entity Recognition (NER), featuring a Flask backend and a Streamlit frontend. It includes an API endpoint for entity extraction and basic authentication using an API key.   

## Installation  

1. **Clone the repository**  
   ```sh
   git clone <repo-url>
   cd <repo-folder>
   ```  

2. **Create a virtual environment (optional but recommended)**  
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```  

3. **Install dependencies**  
   ```sh
   pip install -r requirements.txt
   ```  

## Running the Project  

### Step 1: Start the Backend (Flask API)  

Run the `api.py` file to start the backend server:  
```sh
python api.py
```  

The API has the following endpoint:  

- **`POST /predict`**  
  - **Request**: JSON with text input  
  - **Authentication**: Requires an API key in the request headers  
  - **Header Example (Postman):**  
    ```
    Key: X-API-Key
    Value: f7a6dcb9832b47e8b81c4c5c13f0a2d6
    ```
  - **Example Request (JSON)**  
    ```json
    {
      "text": "Barack Obama was the 44th President of the United States."
    }
    ```
  - **Example Response**  
    ```json
    {
    "entities": [
        {
            "end": 12,
            "entity_group": "PER",
            "score": 0.9916036128997803,
            "start": 0,
            "word": "Barack Obama"
        },
        {
            "end": 56,
            "entity_group": "LOC",
            "score": 0.9869198203086853,
            "start": 43,
            "word": "United States"
        }
    ]
}
    ```

### Step 2: Start the Frontend (Streamlit)  

In a new terminal, run the Streamlit app:  
```sh
streamlit run app.py
```  

## Testing and Screenshots  

The following images show successful testing in:  
1. **Postman** - Demonstrating API authentication and entity recognition.  
2. **Streamlit UI** - Displaying the recognized entities interactively.

![postman](https://github.com/user-attachments/assets/8276e2de-4262-49f7-9c19-dc90f3a9ba77)
![streamlit](https://github.com/user-attachments/assets/6bd6f08d-4ca0-4e68-abf1-39ce57bb584a)
 
---
