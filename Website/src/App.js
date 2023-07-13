import React, { Component, Suspense } from "react";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import "./scss/style.scss";
import "./Font/font.css";
import RequireAuth from "./commponents/Admin/RequireAuth";
import getCookie from "./hooks/getCookie";
import EditData from "./commponents/Admin/Editdata/editData";

const cookie = getCookie("usrin");

const DefaultLayout = React.lazy(() => import("./layout/DefaultLayout"));
const loading = (
  <div className="pt-3 text-center">
    <div className="sk-spinner sk-spinner-pulse"></div>
  </div>
);
const Login = React.lazy(() => import("./commponents/Admin/login/Login"));
const DefaultLayoutPortal = React.lazy(() =>
  import("./layout/DefaultLayoutPortal")
);

function App() {
  return (
    <BrowserRouter>
      <Suspense fallback={loading}>
        <Routes>
          <Route
            exact
            path="/"
            name="Portal"
            element={<DefaultLayoutPortal />}
          />
          <Route path="/adminYourney" name="login" element={<Login />} />
          <Route element={<RequireAuth />}>
            <Route path="*" name="admin" element={<DefaultLayout />} />
          </Route>
        </Routes>
      </Suspense>
    </BrowserRouter>
  );
}

export default App;
