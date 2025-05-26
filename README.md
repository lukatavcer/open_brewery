# Open Brewery Explorer

A Vue.js application with a Django backend that connects to the Open Brewery API, retrieves brewery data, and displays it in a table view. The frontend is built with Vue 3 and Vite, while the backend is built with Django and Django REST Framework.

## Features

- Connects to the [Open Brewery DB API](https://api.openbrewerydb.org/v1/breweries)
- Fetches a list of breweries from across the United States
- Display the fetched data in a table or list view.
- Filtering: Provide at least one filter input or dropdown (e.g., search by name, type, or category).
- Grouping: Group items by a relevant attribute (e.g., brewery type, etc.) and display grouped totals or subtotals.
- Include a simple chart to visualize the grouped data (pie chart, bar chart, etc.).
- Django backend for data persistence and API endpoints

## Live Demo

The site is available at: https://lukatavcer.github.io/open_brewery/

## Project Setup

### Frontend Setup

```sh
cd frontend
npm install
```

### Backend Setup

1. Create a virtual environment (recommended):

```sh
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:

```sh
pip install -r requirements.txt
```

3. Set up environment variables:

```sh
cp .env.example .env
# Edit the .env file to configure your environment variables
# Make sure to change the SECRET_KEY for production
```

4. Run migrations:

```sh
python manage.py migrate
```

5. Create a superuser (optional, for admin access):

```sh
python manage.py createsuperuser
```

## Running the Application

### Frontend Development Server

```sh
cd frontend
npm run dev
```

### Backend Development Server

```sh
cd backend
python manage.py runserver
```

The Django admin interface will be available at http://localhost:8000/admin/

### Fetching Brewery Data

To fetch brewery data from the Open Brewery DB API and save it to the Django database, visit:
http://localhost:8000/api/breweries/fetch_from_api/

## Building for Production

### Compile and Minify Frontend for Production

```sh
cd frontend
npm run build
```

### Linting and Formatting

This project uses ESLint for code linting and Prettier for code formatting.

#### Lint with ESLint

```sh
cd frontend
npm run lint
```

#### Format with Prettier

```sh
cd frontend
npm run format
```
