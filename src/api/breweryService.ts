import { Brewery } from "../types/brewery";

/**
 * Fetches brewery data from the Open Brewery DB API
 * @returns Promise with brewery data
 */
export const fetchBreweries = async (): Promise<Brewery[]> => {
  try {
    const response = await fetch("https://api.openbrewerydb.org/v1/breweries");

    if (!response.ok) {
      throw new Error(`API request failed with status ${response.status}`);
    }

    const data = await response.json();
    console.log("Fetched breweries:", data);
    return data;
  } catch (err: any) {
    console.error("Error fetching breweries:", err);
    throw new Error(err.message || "Failed to fetch breweries");
  }
};
