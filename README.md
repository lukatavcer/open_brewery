# Open Brewery Explorer

A Vue.js application that connects to the Open Brewery API, retrieves brewery data, and displays it in a table view. This project is built with Vue 3 and Vite.

## Features

- Connects to the [Open Brewery DB API](https://api.openbrewerydb.org/v1/breweries)
- Fetches a list of breweries from across the United States
- Displays brewery information in a responsive table, including:
  - Brewery name
  - Brewery type
  - City and state location
  - Website link (when available)
- Handles loading states and error conditions
- Responsive design that works on desktop and mobile devices

## Recommended IDE Setup

[VSCode](https://code.visualstudio.com/) + [Volar](https://marketplace.visualstudio.com/items?itemName=Vue.volar) (and disable Vetur).

## Customize configuration

See [Vite Configuration Reference](https://vite.dev/config/).

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
