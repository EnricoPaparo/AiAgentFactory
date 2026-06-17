const request = require('supertest');
const app = require('../src/index');

describe('GET /health', () => {
  test('should return 200 status code', async () => {
    const res = await request(app).get('/health');
    expect(res.statusCode).toBe(200);
  });

  test('should return JSON with status and timestamp', async () => {
    const res = await request(app).get('/health');
    expect(res.body).toHaveProperty('status');
    expect(res.body).toHaveProperty('timestamp');
  });

  test('should return status ok', async () => {
    const res = await request(app).get('/health');
    expect(res.body.status).toBe('ok');
  });

  test('should return valid ISO8601 timestamp', async () => {
    const res = await request(app).get('/health');
    const timestamp = res.body.timestamp;
    // Verify timestamp is a valid ISO8601 string
    expect(typeof timestamp).toBe('string');
    // Parse the timestamp and verify it's valid
    const date = new Date(timestamp);
    expect(date.toISOString()).toBe(timestamp);
  });

  test('should return application/json content type', async () => {
    const res = await request(app).get('/health');
    expect(res.headers['content-type']).toMatch(/application\/json/);
  });
});
