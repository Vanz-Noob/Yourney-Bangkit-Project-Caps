import axios from "axios";

const BASE_URL = "http://127.0.0.1:8080";

export default axios.create({
  baseURL: BASE_URL,
  headers: {
    "Access-Control-Allow-Credentials": true,
    "Access-Control-Allow-Origin": "*",
  },
});
