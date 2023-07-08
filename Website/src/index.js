import React from "react";
import ReactDOM from "react-dom/client";
import "./index.css";
import App from "./App";
// import reportWebVitals from "./reportWebVitals";
import "bootstrap/dist/css/bootstrap.min.css";

import { AuthProvider } from "./middleware/authProvider";
import { Provider } from "react-redux";
import store from "./store";
import { DestinasiProvider } from "./hooks/getDestinasi";

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
  <React.StrictMode>
    <Provider store={store}>
      <AuthProvider>
        <DestinasiProvider>
          <App />
        </DestinasiProvider>
      </AuthProvider>
    </Provider>
  </React.StrictMode>,
  document.getElementById("root")
);

// reportWebVitals();
