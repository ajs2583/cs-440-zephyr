# Zephyr - Flight Price Tracker

Zephyr is a web-based flight tracking application that helps spontaneous travelers find the lowest flight prices within a three-month period. The system is designed to provide flexibility and ease of use while integrating with external APIs to fetch real-time flight data.

## Features
- **Track Lowest Flight Prices** – Displays the most affordable flight options within a three-month timeframe.
- **API Integration** – Uses the Amadeus API for flight data and potentially Google Maps for visualization.
- **User-Friendly Interface** – A modern, intuitive web app for seamless interaction.
- **Database Integration** – Stores and manages flight-related data efficiently.
- **Scalable Architecture** – Designed to allow easy modifications and improvements over time.

## Tech Stack
- **Frontend:** React.js and Bootsrap HTML/Jinja (Flask)
- **Backend:** Flask (Python)
- **Database:** SQLite (for local testing) / PostgreSQL (for production)
- **APIs:** Amadeus API (for flight data), Google Maps API (optional for visualization)
- **Hosting:** OnRender

## Project Structure
```
cs-440-zephyr/
│── app/
│   ├── website/
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── services.py
│   │   ├── views.py
│── main.py  # Entry point of the application
│── requirements.txt  # Dependencies
│── README.md  # Project documentation
```

## Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/ajs2583/cs-440-zephyr.git
cd cs-440-zephyr
```

### 2. Create a Virtual Environment & Install Dependencies
```bash
python -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate  # On Windows
pip install -r requirements.txt
```

### 3. Set Up Environment Variables
Create a `.env` file in the root directory and add your API keys:
```
FLASK_APP=main.py
FLASK_ENV=development
DATABASE_URL=sqlite:///zephyr.db
AMADEUS_API_KEY=your_amadeus_api_key
```

### 4. Run the Application
```bash
flask run
```
The app will be accessible at `http://127.0.0.1:5000/`.

## Usage
1. Enter your departure and destination locations.
2. Select a date range within three months.
3. Get a list of the cheapest available flights.
4. (Optional) View flight routes on a map.

## Future Enhancements
- User authentication for saved searches.
- Email notifications for price drops.
- More API integrations for additional flight providers.

## License
This project is licensed under the MIT License.

## Contributing
Contributions are welcome! Feel free to submit a pull request or open an issue.

## Contact & Support
For any questions or feedback, reach out via GitHub Issues or email the maintainers.
