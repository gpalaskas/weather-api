# Weather API Project

# Python 3.9.13

## How to Run

1. Clone the repository:

 ```bash
 git clone https://github.com/your-username/weather-api.git
 cd weather-api


2. Create and activate a virtual environment:

 python -m venv venv
 # On Windows
 venv\Scripts\activate
 # On macOS/Linux
 source venv/bin/activate


3. Install dependencies:

 pip install -r requirements.txt


4. Set environment variables in .env file:

 MY_USERNAME=repathsolutions_palaskas_giorgos
 PASSWORD=50TUH8hrr3
 #username and password are valid until 7-June-2025


5. Run the data fetcher to populate the database:

 python fetch_data.py


6. Start the FastAPI server:

 uvicorn main:app --reload


7. Then open your browser at:
 
 http://127.0.0.1:8000/docs

 or testis live at:

 https://weather-api-nk0x.onrender.com/docs