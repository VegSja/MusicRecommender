import React from 'react';
import { createRoot } from 'react-dom/client';
import { App } from './app';

import './index.css'

const rootElement = document.getElementById('root');
createRoot(rootElement!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>

)

