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

const getTopStocksByROI = async (year, ticker, sector) => {
  try {
      let query = `SELECT ticker, sector, return_${year} AS roi FROM stock_returns WHERE return_${year} IS NOT NULL`;
      const queryParams = [];

      if (ticker) {
          query += ` AND ticker = $${queryParams.length + 1}`;
          queryParams.push(ticker);
      }
      if (sector) {
          query += ` AND sector = $${queryParams.length + 1}`;
          queryParams.push(sector);
      }

      query += ` ORDER BY return_${year} DESC LIMIT 10`;

      const { rows } = await pool.query(query, queryParams);
      return rows;
  } catch (error) {
      console.error('Error fetching top stocks by ROI:', error);
      throw error;
  }
};

const getAllDistinctSectors = async () => {
  try {
    const query = 'SELECT DISTINCT sector FROM stock_returns';
    const { rows } = await pool.query(query);
    return rows.map(row => row.sector);
  } catch (error) {
    console.error('Error fetching distinct sectors:', error);
    throw error;
  }
};

module.exports = {
  getStocksDataByTicker,
  getAllDistinctTickers,
  getTopStocksByROI,
  getAllDistinctSectors,
};