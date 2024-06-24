const stocksService  = require('../200_services/stocksService');

const getStocksData = async (req, res) => {
    const { ticker, startDate, endDate } = req.body;

    console.log(ticker)
    if (!ticker) {
      return res.status(400).json({ error: 'Ticker parameter is required' });
    }
  
    try {
      const data = await stocksService.getStocksDataByTicker(ticker, startDate, endDate);
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

  const getTopStocksByROI = async (req, res) => {
    const { year, ticker, sector } = req.query;
    try {
        const topStocks = await stocksService.getTopStocksByROI(year, ticker, sector);
        res.json(topStocks);
    } catch (error) {
        console.error('Error fetching top stocks by ROI:', error);
        res.status(500).json({ error: 'An error occurred while fetching top stocks by ROI' });
    }
};

const getAllSectors = async (req, res) => {
  try {
    const sectors = await stocksService.getAllDistinctSectors();
    res.json(sectors);
  } catch (error) {
    console.error('Error fetching distinct sectors:', error);
    res.status(500).json({ error: 'An error occurred while fetching distinct sectors' });
  }
};

 module.exports = {
  getStocksData,
  getAllTickers,
  getTopStocksByROI,
  getAllSectors
};