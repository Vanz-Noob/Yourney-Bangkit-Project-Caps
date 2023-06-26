import Cookies from "js-cookie";

const setCookie = (cookiename, usrin) => {
  Cookies.set(cookiename, usrin, {
    expires: 0.1,
    secure: true,
    sameSite: "strict",
    path: "/adminYourney",
  });
};

export default setCookie;
