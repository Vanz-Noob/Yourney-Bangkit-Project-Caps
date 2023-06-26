import Cookies from "js-cookie";

const getCookie = (cookiename) => {
  return Cookies.get(cookiename);
};

export default getCookie;
