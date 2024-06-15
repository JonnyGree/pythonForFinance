import React from 'react';
import { AppBar, Toolbar, Typography } from '@mui/material';
import { Outlet, Link } from 'react-router-dom';

const Navbar = () => {
  return (
    <>
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6" component={Link} to="/" color="inherit" style={{ textDecoration: 'none' }}>
            Stock App
          </Typography>
        </Toolbar>
      </AppBar>
      <Outlet />
    </>
  );
};

export default Navbar;
