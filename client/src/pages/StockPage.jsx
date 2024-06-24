import React, { useEffect, useState } from 'react';
import { Box, Button, FormControl, Autocomplete, TextField, MenuItem, Select, InputLabel, Grid } from '@mui/material';
import StockChart from '../components/StockChart';
import axios from 'axios';
import { API_GET_TICKER_URL, API_GET_STOCK_DATA_URL } from '../config';

const StockPage = () => {
  const [stockData, setStockData] = useState([]);
  const [tickers, setTickers] = useState([]);
  const [selectedTicker, setSelectedTicker] = useState('');
  const [selectedTimePeriod, setSelectedTimePeriod] = useState('YTD'); // Default time period
  const [chartType, setChartType] = useState('line'); // Default chart type

  useEffect(() => {
    const fetchTickers = async () => {
      try {
        const response = await axios.get(API_GET_TICKER_URL);
        setTickers(response.data);
        if (response.data.length > 0) {
          setSelectedTicker(response.data[0]);
        }
      } catch (error) {
        console.error('Error fetching tickers:', error.message);
      }
    };

    fetchTickers();
  }, []);

  const fetchStockData = async () => {
    let startDate;
    switch (selectedTimePeriod) {
      case '1D':
        startDate = getFormattedDate(-1);
        break;
      case '5D':
        startDate = getFormattedDate(-5);
        break;
      case '1M':
        startDate = getFormattedDate(-30);
        break;
      case '6M':
        startDate = getFormattedDate(-180);
        break;
      case 'YTD':
        startDate = getFormattedDateYTD();
        break;
      case '1Y':
        startDate = getFormattedDate(-365);
        break;
      case '5Y':
        startDate = getFormattedDate(-1825); // approximately 5 years
        break;
      case 'Max':
        startDate = '1970-01-01'; // or any suitable default start date for 'Max'
        break;
      default:
        startDate = getFormattedDate(-1); // Default to 1 day if no valid period selected
        break;
    }

    try {
      const response = await axios.post(API_GET_STOCK_DATA_URL, {
        ticker: selectedTicker,
        startDate: startDate
      });
      setStockData(response.data);
    } catch (error) {
      console.error('Error fetching stock data:', error.message);
    }
  };

  useEffect(() => {
    fetchStockData();
  }, [selectedTimePeriod, selectedTicker]);

  const getFormattedDate = (daysAgo) => {
    const today = new Date();
    const priorDate = new Date().setDate(today.getDate() + daysAgo);
    return new Date(priorDate).toISOString().split('T')[0];
  };

  const getFormattedDateYTD = () => {
    const today = new Date();
    const yearStart = new Date(today.getFullYear(), 0, 1);
    return yearStart.toISOString().split('T')[0];
  };

  const calculateROI = () => {
    if (stockData.length > 0) {
      const startPrice = stockData[0].adj_close; // Use open price of the first day
      const endPrice = stockData[stockData.length - 1].adj_close; // Use close price of the last day
      const roi = ((endPrice - startPrice) / startPrice) * 100;
      const formattedROI = roi.toFixed(2); // Return ROI as a percentage with two decimal places

      // Determine color based on ROI
      const color = roi > 0 ? 'green' : 'red';

      return (
        <span style={{ color }}>
          {endPrice.toFixed(2)} ({formattedROI}%)
        </span>
      );
    }
    return null; // Return null if no data or insufficient data
  };

  return (
    <Grid container spacing={2} sx={{ height: '100vh', padding: '16px' }}>
      {/* Ticker Autocomplete */}
      <Grid item xs={12} md={3}>
        <Box sx={{ display: 'flex', justifyContent: 'flex-end', alignItems: 'center' }}>
          <Autocomplete
            id="ticker-autocomplete"
            disableClearable
            options={tickers}
            value={selectedTicker}
            onChange={(event, newValue) => {
              setSelectedTicker(newValue);
            }}
            style={{width: '300px'}}
            renderInput={(params) => (
              <TextField {...params} label="Ticker" variant="outlined" />
            )}
          />
          {/* Chart Type Selector */}
          <FormControl variant="outlined" sx={{ minWidth: 120, marginLeft: 2 }}>
            <InputLabel id="chart-type-label">Chart Type</InputLabel>
            <Select
              labelId="chart-type-label"
              value={chartType}
              onChange={(event) => setChartType(event.target.value)}
              label="Chart Type"
            >
              <MenuItem value="line">Line</MenuItem>
              <MenuItem value="candlestick">Candlestick</MenuItem>
            </Select>
          </FormControl>
          <FormControl variant="outlined" sx={{ minWidth: 120, marginLeft: 2 }}>
          {calculateROI() }
          </FormControl>
        </Box>
      </Grid>

      {/* Price and ROI */}
      <Grid item xs={12} md={3}>
        <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
          {/* Placeholder for ROI */}

        </Box>
      </Grid>

      {/* Time Period Selector and Chart Type */}
      <Grid item xs={12} md={6}>
        <Box sx={{ display: 'flex', justifyContent: 'flex-end', alignItems: 'center' }}>
          {/* Time Period Selector Buttons */}
          <Button variant="outlined" onClick={() => setSelectedTimePeriod('1D')} sx={{ marginRight: 1 }}>
            1D
          </Button>
          <Button variant="outlined" onClick={() => setSelectedTimePeriod('5D')} sx={{ marginRight: 1 }}>
            5D
          </Button>
          <Button variant="outlined" onClick={() => setSelectedTimePeriod('1M')} sx={{ marginRight: 1 }}>
            1M
          </Button>
          <Button variant="outlined" onClick={() => setSelectedTimePeriod('6M')} sx={{ marginRight: 1 }}>
            6M
          </Button>
          <Button variant="outlined" onClick={() => setSelectedTimePeriod('YTD')} sx={{ marginRight: 1 }}>
            YTD
          </Button>
          <Button variant="outlined" onClick={() => setSelectedTimePeriod('1Y')} sx={{ marginRight: 1 }}>
            1Y
          </Button>
          <Button variant="outlined" onClick={() => setSelectedTimePeriod('5Y')} sx={{ marginRight: 1 }}>
            5Y
          </Button>
          <Button variant="outlined" onClick={() => setSelectedTimePeriod('Max')}>
            Max
          </Button>


        </Box>
      </Grid>

      {/* Stock Chart */}
      <Grid item xs={12}>
        <Box sx={{ height: 'calc(100vh - 250px)', overflowY: 'scroll' }}>
          <StockChart data={stockData} chartType={chartType} />
        </Box>
      </Grid>
    </Grid>
  );
};


export default StockPage;
