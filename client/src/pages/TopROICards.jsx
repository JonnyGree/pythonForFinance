import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Grid, Paper, Typography, Select, MenuItem, FormControl, InputLabel } from '@mui/material';

// API URLs
import {API_GET_SECTORS_URL, API_GET_TOP_STOCKS_URL } from '../config';
const years = [2023, 2022, 2021, 2020, 2019]; // Past 5 years

const TopROICards = () => {
  const [sector, setSector] = useState('');
  const [sectors, setSectors] = useState([]);
  const [stocks, setStocks] = useState([]);

  const fetchTopStocks = async () => {
    try {
      const promises = years.map(year => axios.get(API_GET_TOP_STOCKS_URL, {
        params: { year, sector }
      }));
      const results = await Promise.all(promises);
      const stocksByYear = results.map((response, index) => ({
        year: years[index],
        stocks: response.data.map(stock => ({
          ...stock,
          roi: `${(stock.roi * 100).toFixed(2)}%`
        }))
      }));
      setStocks(stocksByYear);
      console.log(stocksByYear)
    } catch (error) {
      console.error('Error fetching top stocks:', error.message);
    }
  };

  useEffect(() => {
    const fetchSectors = async () => {
      try {
        const response = await axios.get(API_GET_SECTORS_URL);
        setSectors(response.data);
      } catch (error) {
        console.error('Error fetching sectors:', error.message);
      }
    };

    fetchSectors();
  }, []);

  useEffect(() => {
    if (sector) {
      fetchTopStocks();
    }
  }, [sector]);

  return (
    <Paper style={{ padding: 16 }}>
      <Grid container spacing={2} alignItems="center" justify="center">
        <Grid item xs={12} sm={6}>
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
      </Grid>
      {stocks.length > 0 && stocks.map(({ year, stocks }) => (
        <div key={year}>
          <Typography variant="h6" style={{ marginTop: 16 }}>
            Top Stocks for {year}
          </Typography>
          <Grid container spacing={2}>
            {stocks.slice(0, 6).map(stock => (
              <Grid item xs={12} sm={6} md={4} lg={2} key={stock.ticker}>
                <Paper style={{ padding: 16 }}>
                  <Typography variant="h6">{stock.ticker}</Typography>
                  <Typography variant="body1">ROI: {stock.roi}</Typography>
                </Paper>
              </Grid>
            ))}
          </Grid>
        </div>
      ))}
    </Paper>
  );
};

export default TopROICards;
