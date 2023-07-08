import React from "react";
import { useLocation, Navigate, Outlet } from "react-router-dom";
import useAuth from "../../hooks/useAuth";
import getCookie from "../../hooks/getCookie";

const RequireAuth = () => {
  const { auth } = useAuth();
  const location = useLocation();
  const uid = getCookie("usrin");

  return auth?.accessToken ? (
    <Outlet />
  ) : (
    <Navigate to="/adminYourney" state={{ from: location }} replace />
  );
};

export default RequireAuth;
