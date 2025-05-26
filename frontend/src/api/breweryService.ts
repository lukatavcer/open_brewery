import { Brewery } from "../types/brewery";

// API configuration
export const API_CONFIG = {
  // Set to true to use the Django backend, false to use the Open Brewery DB API directly
  USE_DJANGO_BACKEND: false,
  // Django backend API URL
  DJANGO_API_URL: "http://localhost:8000/api/breweries/",
  // Open Brewery DB API URL
  OPEN_BREWERY_API_URL: "https://api.openbrewerydb.org/v1/breweries"
};

/**
 * Fetches brewery data from either the Django backend or the Open Brewery DB API
 * @returns Promise with brewery data
 */
export const fetchBreweries = async (): Promise<Brewery[]> => {
  try {
    const apiUrl = API_CONFIG.USE_DJANGO_BACKEND 
      ? API_CONFIG.DJANGO_API_URL 
      : API_CONFIG.OPEN_BREWERY_API_URL;

    console.log(`Fetching breweries from: ${apiUrl}`);
    const response = await fetch(apiUrl);

    if (!response.ok) {
      throw new Error(`API request failed with status ${response.status}`);
    }

    let data = await response.json();

    // Handle different response formats
    if (API_CONFIG.USE_DJANGO_BACKEND && data.results) {
      // Django REST Framework with pagination
      data = data.results;
    }

    console.log("Fetched breweries:", data);
    return data;
  } catch (err: any) {
    console.error("Error fetching breweries:", err);
    throw new Error(err.message || "Failed to fetch breweries");
  }
};

/**
 * Triggers the Django backend to fetch and store brewery data from the Open Brewery DB API
 * Only works when using the Django backend
 * @returns Promise with the result of the operation
 */
export const syncBreweriesWithBackend = async (): Promise<{ message: string }> => {
  if (!API_CONFIG.USE_DJANGO_BACKEND) {
    console.warn("This function only works when using the Django backend");
    return { message: "Not using Django backend" };
  }

  try {
    const response = await fetch(`${API_CONFIG.DJANGO_API_URL}fetch_from_api/`);

    if (!response.ok) {
      throw new Error(`API request failed with status ${response.status}`);
    }

    const data = await response.json();
    console.log("Sync result:", data);
    return data;
  } catch (err: any) {
    console.error("Error syncing breweries:", err);
    throw new Error(err.message || "Failed to sync breweries");
  }
};
