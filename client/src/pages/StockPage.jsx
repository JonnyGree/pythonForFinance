import React, { useEffect, useState } from 'react';
import { Box, Button, FormControl, Grid, InputLabel, Autocomplete, TextField } from '@mui/material';
import StockChart from '../components/StockChart';
import axios from 'axios';

const API_GET_STOCK_DATA_URL = 'http://localhost:3000/GetStocksDataFromDb';
const API_GET_TICKER_URL = 'http://localhost:3000/getTicker';

const StockPage = () => {
  const [stockData, setStockData] = useState([]);
  const [tickers, setTickers] = useState([]);
  const [selectedTicker, setSelectedTicker] = useState('AAPL');

  useEffect(() => {
    const fetchTickers = async () => {
      try {
        const response = await axios.get(API_GET_TICKER_URL);
        setTickers(response.data);
        if (response.data.length > 0) {
          setSelectedTicker(response.data[0]); // Set default selected ticker
        }
      } catch (error) {
        console.error('Error fetching tickers:', error.message);
      }
    };

    fetchTickers();
  }, []);

  const fetchStockData = async () => {
    const startDate = '2020-01-01'; // Replace with your desired fixed start date
  
    try {
      const response = await axios.post(API_GET_STOCK_DATA_URL, {
        ticker: selectedTicker,
        startDate: startDate  // Include the fixed startDate here
      });
      setStockData(response.data);
    } catch (error) {
      console.error('Error fetching stock data:', error.message);
    }
  };


  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', height: '100vh' }}>
      <FormControl variant="outlined" sx={{ minWidth: 200, marginBottom: 2 }}>
        <Autocomplete
          id="ticker-autocomplete"
          disableClearable
          options={tickers}
          value={selectedTicker}
          onInputChange={(event, newInputValue) => {
            setSelectedTicker(newInputValue);
          }}
          renderInput={(params) => <TextField {...params} label="Ticker" variant="outlined" />}
        />
      </FormControl>
      <Button variant="contained" onClick={fetchStockData} sx={{ marginBottom: 2 }}>
        Fetch Stock Data
      </Button>
      <Box sx={{ width: '100%', height: 'calc(100vh - 200px)' }}>
        <StockChart data={stockData} />
      </Box>
    </Box>
  );
};

export default StockPage;
