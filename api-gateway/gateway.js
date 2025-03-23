const express = require('express');
const { createProxyMiddleware } = require('http-proxy-middleware');
const app = express();

app.use('/auth', createProxyMiddleware({ target: 'http://auth-service:5001', changeOrigin: true }));
app.use('/saved', createProxyMiddleware({ target: 'http://saved-service:5003', changeOrigin: true }));
app.use('/flight', createProxyMiddleware({ target: 'http://flight-service:5002', changeOrigin: true }));

app.listen(8080, () => {
    console.log('API Gateway running on port 8080');
});