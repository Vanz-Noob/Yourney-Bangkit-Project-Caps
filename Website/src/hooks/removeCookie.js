import Cookies from "js-cookie";

const removeCookie = (cookiename) => {
  Cookies.remove("usrin", {
    path: "/adminYourney",
  });
};

export default removeCookie;
