import React from 'react';
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Navbar from './components/Navbar';
import StockPage from './pages/StockPage';
import 'bootstrap/dist/css/bootstrap.min.css';
import StockComparison from './pages/StockComparison';
import TopROICards from './pages/TopROICards'

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Navbar />}>
          <Route index element={<StockPage />} />
          <Route path="stockcomparison" element={<StockComparison />} />
          <Route path="top-roi-cards" element={<TopROICards />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
