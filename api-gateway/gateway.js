const express = require('express');
const { createProxyMiddleware } = require('http-proxy-middleware');
const app = express();

app.use('/auth', createProxyMiddleware({ target: 'http://auth-service:5001', changeOrigin: true }));
app.use('/orders', createProxyMiddleware({ target: 'http://order-service:5003', changeOrigin: true }));
app.use('/inventory', createProxyMiddleware({ target: 'http://inventory-service:5002', changeOrigin: true }));

app.listen(8080, () => {
    console.log('API Gateway running on port 8080');
});