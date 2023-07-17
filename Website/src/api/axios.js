import axios from "axios";

const BASE_URL = "https://yourney-api.et.r.appspot.com";

const cancelToken = axios.CancelToken.source();

export default axios.create({
  cancelToken: cancelToken.token,
  baseURL: BASE_URL,
  headers: {
    "Access-Control-Allow-Credentials": true,
    "Access-Control-Allow-Origin": "*",
  },
});
