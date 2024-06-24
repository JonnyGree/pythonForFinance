import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { TextField, Button, Grid, Paper, Typography, MenuItem, Select, FormControl, InputLabel, Autocomplete } from '@mui/material';
import StockTable from '../components/StockTable';

// API URLs
import { API_GET_TICKER_URL, API_GET_SECTORS_URL, API_GET_TOP_STOCKS_URL } from '../config';

const availableYears = [
  2024, 2023, 2022, 2021, 2020,
  2019, 2018, 2017, 2016, 2015,
  2014, 2013, 2012, 2011, 2010
];

const StockComparison = () => {
  const [year, setYear] = useState('');
  const [selectedTicker, setSelectedTicker] = useState('');
  const [sector, setSector] = useState('');
  const [tickers, setTickers] = useState([]);
  const [sectors, setSectors] = useState([]);
  const [stocks, setStocks] = useState([]);

  const fetchStocks = async () => {
    try {
      const response = await axios.get(API_GET_TOP_STOCKS_URL, {
        params: { year, ticker: selectedTicker, sector }
      });
      const formattedStocks = response.data.map(stock => ({
        ...stock,
        roi: `${(stock.roi * 100).toFixed(2)}%`
      }));
      setStocks(formattedStocks);
    } catch (error) {
      console.error('Error fetching stock data:', error.message);
    }
  };

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

    const fetchSectors = async () => {
      try {
        const response = await axios.get(API_GET_SECTORS_URL);
        setSectors(response.data);
      } catch (error) {
        console.error('Error fetching sectors:', error.message);
      }
    };

    fetchTickers();
    fetchSectors();
  }, []);

  return (
    <Paper style={{ padding: 16 }}>
      <Grid container spacing={2} alignItems="center" justify="center">
        <Grid item xs={12} sm={4}>
          <FormControl variant="outlined" fullWidth>
            <InputLabel>Year</InputLabel>
            <Select
              value={year}
              onChange={(e) => setYear(e.target.value)}
              label="Year"
            >
              {availableYears.map((yr) => (
                <MenuItem key={yr} value={yr}>
                  {yr}
                </MenuItem>
              ))}
            </Select>
          </FormControl>
        </Grid>
        <Grid item xs={12} sm={4}>
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
        </Grid>
        <Grid item xs={12} sm={4}>
          <FormControl variant="outlined" fullWidth>
            <InputLabel>Sector</InputLabel>
            <Select
              value={sector}
              onChange={(e) => setSector(e.target.value)}
              label="Sector"
            >
              {sectors.map((sec) => (
                <MenuItem key={sec} value={sec}>
                  {sec}
                </MenuItem>
              ))}
            </Select>
          </FormControl>
        </Grid>
        <Grid item xs={12} style={{ textAlign: 'center', marginTop: 16 }}>
          <Button variant="contained" color="primary" onClick={fetchStocks}>
            Fetch Stocks
          </Button>
        </Grid>
      </Grid>
      <Typography variant="h5" style={{ marginTop: 16, textAlign: 'center' }}>
        Top Stocks by ROI
      </Typography>
      <StockTable stocks={stocks} />
    </Paper>
  );
};

export default StockComparison;
