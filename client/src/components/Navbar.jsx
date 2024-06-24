import React from 'react';
import { AppBar, Toolbar, Typography } from '@mui/material';
import { Outlet, Link } from 'react-router-dom';

const Navbar = () => {
  return (
    <>
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6" component={Link} to="/" color="inherit" style={{ textDecoration: 'none' }}  sx={{mr: 2}}>
            Stock App
          </Typography>
          <Typography variant="h6" component={Link} to="/stockcomparison" color="inherit" style={{ textDecoration: 'none' }} sx={{mr: 2}}>
            Stock Comparison
          </Typography>
          <Typography variant="h6" component={Link} to="/top-roi-cards" color="inherit" style={{ textDecoration: 'none' }} sx={{mr: 2}}>
            top-roi-cards
          </Typography>
        </Toolbar>
      </AppBar>
      <Outlet />
    </>
  );
};

export default Navbar;
