import React from "react";
import {
  Brand,
  Footer,
  Highlight,
  Home,
  Member,
  Navigation,
  Portofolio,
} from "../commponents/Portal";

const DefaultLayoutPortal = () => {
  return (
    <div style={{ width: "100vw", overflowX: "hidden" }}>
      <Navigation />
      <Home />
      <Highlight />
      <Brand />
      <Portofolio />
      <Member />
      <Footer />
    </div>
  );
};

export default DefaultLayoutPortal;
