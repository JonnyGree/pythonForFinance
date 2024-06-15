import React from 'react';
import Plot from 'react-plotly.js';

const StockChart = ({ data }) => {
  const dates = [];
  const closes = [];
  const opens = [];
  const highs = [];
  const lows = [];
  
  data.forEach(item => {
    dates.push(item.date);
    closes.push(item.close);
    opens.push(item.open);
    highs.push(item.high);
    lows.push(item.low);
  });

  return (
    <div style={{ width: '100%', height: '100%' }}>
      <Plot
        data={[
          {
            x: dates,
            close: closes,
            decreasing: { line: { color: 'red' } },
            high: highs,
            increasing: { line: { color: 'green' } },
            line: { color: 'rgba(31,119,180,1)' },
            low: lows,
            open: opens,
            type: 'candlestick',
            xaxis: 'x',
            yaxis: 'y'
          }
        ]}
        layout={{
          title: 'Stock Price',
          xaxis: {
            title: 'Date',
            type: 'date'
          },
          yaxis: {
            title: 'Price'
          },
          autosize: true // Ensure the plot adjusts to the size of its container
        }}
        style={{ width: '100%', height: '100%' }}
      />
    </div>
  );
};

export default StockChart;
