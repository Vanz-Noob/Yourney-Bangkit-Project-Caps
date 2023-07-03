import axios from "axios";

const BASE_URL = "http://127.0.0.1";

export default axios.create({
  baseURL: BASE_URL,
  headers: { "Access-Control-Allow-Credentials": true },
});

export const axioPrivate = axios.create({
  baseURL: BASE_URL,
  headers: { "Content-Type": "application/json" },
  withCredentials: true,
});
