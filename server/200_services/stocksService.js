const pool = require('../00_config/database');

const getStocksDataByTicker = async (ticker) => {
  try {
    const query = 'SELECT * FROM stock_data WHERE ticker = $1 ORDER BY date ASC';
    const { rows } = await pool.query(query, [ticker]);
    return rows;
  } catch (error) {
    console.error('Error fetching stock data:', error);
    throw error;
  }
};

const getAllDistinctTickers = async () => {
  try {
    const query = 'SELECT DISTINCT ticker FROM stock_data';
    const { rows } = await pool.query(query);
    return rows.map(row => row.ticker);
  } catch (error) {
    console.error('Error fetching distinct tickers:', error);
    throw error;
  }
};

module.exports = {
  getStocksDataByTicker,
  getAllDistinctTickers,
};