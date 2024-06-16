const pool = require('../00_config/database');

const getStocksDataByTicker = async (ticker, startDate, endDate) => {
  try {
    let query = 'SELECT * FROM stock_data WHERE ticker = $1';
    const queryParams = [ticker];

    // Check if startDate and endDate are provided
    if (startDate && endDate) {
      query += ' AND date >= $2 AND date <= $3';
      queryParams.push(startDate, endDate);
    } else if (startDate) {
      query += ' AND date >= $2';
      queryParams.push(startDate);
    } else if (endDate) {
      query += ' AND date <= $2';
      queryParams.push(endDate);
    }

    query += ' ORDER BY date ASC';

    const { rows } = await pool.query(query, queryParams );
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