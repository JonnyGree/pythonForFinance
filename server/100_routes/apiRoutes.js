const express = require('express');
const router = express.Router();
const stocksController  = require('../50_controllers/stocksController ');

// Endpoint to fetch stock data by ticker
router.post('/GetStocksDataFromDb', stocksController.getStocksData);

// Endpoint to fetch all distinct tickers
router.get('/getTicker', stocksController.getAllTickers);

module.exports = router;