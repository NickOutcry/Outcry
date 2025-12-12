# Outcry Projects - React Frontend

React frontend for Outcry Projects built with Vite, React, and Tailwind CSS.

## Quick Start

### Install Dependencies

```bash
npm install
```

### Development Server

```bash
npm run dev
```

The app will be available at http://localhost:3000

### Build for Production

```bash
npm run build
```

The production build will be in the `dist/` directory.

### Preview Production Build

```bash
npm run preview
```

## Project Structure

```
frontend/
├── src/
│   ├── components/     # Reusable React components
│   ├── pages/          # Page components
│   ├── styles/         # CSS and design tokens
│   ├── api/            # API client and endpoints
│   ├── App.jsx         # Main app component
│   └── main.jsx        # Entry point
├── index.html
├── package.json
├── tailwind.config.js
└── vite.config.js
```

## Design System

The project uses a design token system defined in `src/styles/tokens.css`. All colors, spacing, and other design values are mapped to Tailwind through the `tailwind.config.js`.

### Using Design Tokens

```jsx
// Colors
<div className="bg-primary text-white">Primary Button</div>
<div className="bg-neutral-100">Light Background</div>

// Spacing
<div className="p-4 m-6">Padding and Margin</div>

// Border Radius
<button className="rounded-md">Rounded Button</button>
```

## API Integration

API clients are organized by domain in `src/api/`:

- `client.js` - Client API
- `job.js` - Job API
- `product.js` - Product API
- `staff.js` - Staff API

### Example Usage

```jsx
import { clientApi } from './api/client';

// Get all clients
const clients = await clientApi.getAll();

// Create a client
const newClient = await clientApi.create({
  name: 'Acme Corp',
  address: '123 Main St'
});
```

## Environment Variables

Create a `.env` file in the frontend directory:

```env
VITE_API_URL=http://localhost:5001/api
```

## Dark Mode

Dark mode is configured and can be toggled by adding/removing the `dark` class on the root element.

