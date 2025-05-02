# Expense Tracker 💸

Welcome to **Expense Tracker**, a sleek and intuitive web application designed to help you manage your finances with ease! Built with Flask, PostgreSQL, and Docker, this app allows you to track expenses and incomes, convert currencies, filter transactions, and visualize your financial data through interactive charts. Whether you're a budgeting enthusiast or just want to keep an eye on your spending, this app has you covered.

---

## 🌟 Key Features

- **User Authentication** 🔐  
  Secure registration and login with password hashing using `passlib` (PBKDF2-SHA256).

- **Transaction Management** 📊  
  Add, delete, and view transactions with details like amount, category, currency, and date.

- **Currency Conversion** 💱  
  Supports USD, EUR, and RUB with real-time conversion via the [ExchangeRate-API](https://www.exchangerate-api.com/).

- **Data Filtering** 📅  
  Filter transactions by period (last month or year) to focus on specific timeframes.

- **Interactive Visualizations** 📈  
  Visualize your spending and income with dynamic charts (pie and bar charts, toggleable display).

- **Responsive Design** 🎨  
  A modern, user-friendly interface styled with Bootstrap and custom CSS animations.

- **Containerized Deployment** 🐳  
  Fully containerized with Docker and Docker Compose for easy setup and deployment.

---

## 📸 Screenshots

*(Add screenshots of your app here to showcase the UI, e.g., login page, transaction list, and charts. You can use placeholder text for now:)*
- **Login Page**: [Insert screenshot]
- **Dashboard with Transactions**: [Insert screenshot]
- **Interactive Charts**: [Insert screenshot]

---

## 🛠️ Technologies Used

- **Backend**: Flask 2.3.2 (Python web framework)
- **Database**: PostgreSQL 17 (via `psycopg2-binary`)
- **Frontend**: Bootstrap 5, Custom CSS animations
- **Currency Conversion**: ExchangeRate-API (`requests` library)
- **Authentication**: `passlib` for secure password hashing
- **Containerization**: Docker, Docker Compose
- **Dependencies**: Managed via `requirements.txt`

---

## 📋 Prerequisites

To run this application, ensure you have the following installed:

- [Docker](https://www.docker.com/get-started) 🐳
- [Docker Compose](https://docs.docker.com/compose/install/) 🐙
- An API key from [ExchangeRate-API](https://www.exchangerate-api.com/) for currency conversion

---

## 🚀 Getting Started

Follow these steps to set up and run the Expense Tracker on your local machine.

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/expense-tracker.git
cd expense-tracker
```

### 2. Configure Environment Variables
The application requires an API key for currency conversion. Create or edit the `.env` file in the root directory and add your API key:

```env
EXCHANGE_RATE_API_KEY=your_api_key_here
```

To obtain an API key:
1. Sign up at [ExchangeRate-API](https://www.exchangerate-api.com/).
2. Copy your API key and paste it into the `.env` file.

### 3. Build and Run the Application
Ensure Docker and Docker Compose are installed and running. Then, execute the following command to build and start the application:

```bash
./run.sh
```

This script will:
- Run the `prepare-app.sh` script to build the Docker image for the Flask app.
- Start the application using `docker-compose up --build`.

### 4. Access the Application
Once the containers are running, open your browser and navigate to:

```
http://localhost:5000
```

You should see the login page of the Expense Tracker.

### 5. Stop the Application
To stop the application, press `Ctrl+C` in the terminal where `docker-compose` is running, then run:

```bash
docker-compose down
```

To also remove the database volume (if you want to reset the database):

```bash
docker-compose down -v
```

---

## 📂 Project Structure

```
expense-tracker/
│
├── app/                          # Flask application directory
│   ├── app.py                    # Main Flask application
│   ├── prepare-app.sh            # Script to build and tag the Docker image
│   ├── templates/                # HTML templates (Jinja2)
│   │   ├── index.html            # Main dashboard
│   │   ├── login.html            # Login page
│   │   └── register.html         # Registration page
│   ├── static/                   # Static files (CSS, JS, images)
│   │   ├── css/                  # Custom CSS styles
│   │   └── js/                   # JavaScript for charts and interactivity
│   └── requirements.txt          # Python dependencies
│
├── .env                          # Environment variables (API key)
├── Dockerfile                    # Dockerfile for the Flask app
├── docker-compose.yml            # Docker Compose configuration
├── run.sh                        # Main script to run the app
├── start-app.sh                  # Script to start the Flask app container
└── README.md                     # This documentation
```

---

## 🖥️ Usage

### 1. Register an Account
- Navigate to the registration page (`/register`).
- Enter a username and a password (minimum 8 characters).
- Click "Register" to create your account and be automatically logged in.

### 2. Log In
- On the login page (`/login`), enter your username and password.
- Click "Login" to access the dashboard.

### 3. Manage Transactions
- **Add a Transaction**:
  - On the dashboard (`/`), fill out the transaction form (amount, category, currency, date, type: expense/income).
  - Submit to add the transaction.
- **Delete a Transaction**:
  - Click the "Delete" button next to a transaction to remove it.
- **Filter Transactions**:
  - Use the dropdowns to filter by period (month/year) and currency (USD/EUR/RUB).

### 4. Visualize Data
- View your expenses and incomes in interactive charts (pie or bar).
- Toggle chart visibility or switch chart types using the buttons.

### 5. Log Out
- Click "Logout" to end your session and return to the login page.

---

## 🐳 Docker Architecture

The application is containerized using Docker Compose with two services:

- **web**: The Flask application.
  - Built from the `Dockerfile` in the `app/` directory.
  - Runs on port `5000`.
  - Depends on the `db` service.
- **db**: PostgreSQL database.
  - Uses the `postgres:17` image.
  - Stores data in a persistent volume (`db-data`).

Both services communicate over a bridge network (`app-network`).

---

## ⚙️ Configuration Details

- **Database**:
  - User: `user`
  - Password: `password`
  - Database Name: `expense_db`
  - Host: `db` (Docker service name)
  - Port: `5432`

- **Currency Conversion**:
  - The app uses the ExchangeRate-API to fetch real-time exchange rates.
  - Supported currencies: USD, EUR, RUB.
  - Ensure your API key is valid to avoid conversion errors.

- **Security**:
  - Passwords are hashed using PBKDF2-SHA256 for secure storage.
  - Session management is handled by Flask's built-in session mechanism.

---

## 🖌️ Frontend Details

- **Styling**: The app uses Bootstrap 5 for responsive design, enhanced with custom CSS animations for a smooth user experience.
- **Charts**: Interactive charts are implemented using JavaScript (likely Chart.js, though not explicitly included in the provided files).
- **Templates**: Jinja2 templates (`index.html`, `login.html`, `register.html`) are used for dynamic rendering.

---

## 📈 Future Improvements

- **More Currencies**: Add support for additional currencies (e.g., GBP, JPY).
- **Advanced Filtering**: Allow custom date ranges for filtering transactions.
- **Export Data**: Enable users to export transactions as CSV or PDF.
- **Mobile App**: Develop a companion mobile app using Flutter or React Native.
- **Enhanced Charts**: Add more chart types (e.g., line charts for trends over time).
- **User Profiles**: Allow users to update their profile and password.

---

## 🐞 Troubleshooting

- **"Database connection failed"**:
  - Ensure the `db` service is running (`docker-compose ps`).
  - Check if the PostgreSQL credentials in `docker-compose.yml` match those in `app.py`.
- **"Currency conversion failed"**:
  - Verify that your `EXCHANGE_RATE_API_KEY` in `.env` is valid.
  - Check your internet connection, as the API requires an external request.
- **"Docker build failed"**:
  - Ensure Docker and Docker Compose are installed and running.
  - Check for errors in the `Dockerfile` or `docker-compose.yml`.

---

## 🤝 Contributing

Contributions are welcome! To contribute:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature`).
3. Make your changes and commit (`git commit -m "Add your feature"`).
4. Push to your branch (`git push origin feature/your-feature`).
5. Open a Pull Request.

---

## 📜 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## 📧 Contact

For questions or feedback, feel free to reach out:
- **GitHub**: [your-username](https://github.com/your-username)
- **Email**: your-email@example.com

Happy budgeting! 💰