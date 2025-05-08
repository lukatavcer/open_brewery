# Open Brewery Explorer

A Vue.js application that connects to the Open Brewery API, retrieves brewery data, and displays it in a table view. This project is built with Vue 3 and Vite.

## Features

- Connects to the [Open Brewery DB API](https://api.openbrewerydb.org/v1/breweries)
- Fetches a list of breweries from across the United States
- Display the fetched data in a table or list view.
- Filtering: Provide at least one filter input or dropdown (e.g., search by name, type, or category).
- Grouping: Group items by a relevant attribute (e.g., brewery type, etc.) and display grouped totals or subtotals.
- Include a simple chart to visualize the grouped data (pie chart, bar chart, etc.).

## Project Setup

```sh
npm install
```

### Compile and Hot-Reload for Development

```sh
npm run dev
```

### Compile and Minify for Production

```sh
npm run build
```

### Linting and Formatting

This project uses ESLint for code linting and Prettier for code formatting.

#### Lint with ESLint

```sh
npm run lint
```

#### Format with Prettier

```sh
npm run format
```
