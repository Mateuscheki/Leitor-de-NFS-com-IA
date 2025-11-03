import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import './index.css'; // Opcional, mas bom para reset básico

const root = ReactDOM.createRoot(
  document.getElementById('root') as HTMLElement
);

root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);