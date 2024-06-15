const stocksService  = require('../200_services/stocksService');

const getStocksData = async (req, res) => {
    const { ticker } = req.body;

    console.log(ticker)
    if (!ticker) {
      return res.status(400).json({ error: 'Ticker parameter is required' });
    }
  
    try {
      const data = await stocksService.getStocksDataByTicker(ticker);
      console.log(data)
      res.json(data);
    } catch (error) {
      console.error('Error fetching stock data:', error);
      res.status(500).json({ error: 'An error occurred while fetching stock data' });
    }
  };
  
  const getAllTickers = async (req, res) => {
    try {
      const tickers = await stocksService.getAllDistinctTickers();
      res.json(tickers);
    } catch (error) {
      console.error('Error fetching distinct tickers:', error);
      res.status(500).json({ error: 'An error occurred while fetching distinct tickers' });
    }
  };

 module.exports = {
  getStocksData,
  getAllTickers
};