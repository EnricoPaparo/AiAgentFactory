const express = require('express');

const app = express();
const port = process.env.PORT || 3000;

// GET /health endpoint
app.get('/health', (req, res) => {
  res.json({
    status: 'ok',
    timestamp: new Date().toISOString()
  });
});

// Start server
const server = app.listen(port, () => {
  console.log(`Server started on port ${port}`);
});

// Export app for testing
module.exports = app;
