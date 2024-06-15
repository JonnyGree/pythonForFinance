require('dotenv').config();
const express = require('express');
const cors = require('cors');
const apiRoutes  = require('./100_routes/apiRoutes');

const app = express();
const PORT = process.env.PORT;

// Middleware
app.use(express.json());
app.use(cors()); // Enable CORS for all routes

console.log(process.env.DB_CONNECTION)
// Routes
app.use('/', apiRoutes);

app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});