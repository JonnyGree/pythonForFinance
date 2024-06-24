const express = require('express');
const router = express.Router();
const stocksController  = require('../50_controllers/stocksController ');

// Endpoint to fetch stock data by ticker
router.post('/GetStocksDataFromDb', stocksController.getStocksData);

// Endpoint to fetch all distinct tickers
router.get('/getTicker', stocksController.getAllTickers);

// Endpoint to fetch top 10 stocks by ROI for a given year with optional filters
router.get('/getTopStocks', stocksController.getTopStocksByROI);

// Endpoint to fetch all distinct sectors
router.get('/getSectors', stocksController.getAllSectors);

module.exports = router;