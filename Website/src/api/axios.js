import axios from "axios";

const BASE_URL = "https://yourney-api.et.r.appspot.com";

export default axios.create({
  baseURL: BASE_URL,
  headers: { "Access-Control-Allow-Credentials": true },
});

export const axioPrivate = axios.create({
  baseURL: BASE_URL,
  headers: { "Content-Type": "application/json" },
  withCredentials: true,
});
