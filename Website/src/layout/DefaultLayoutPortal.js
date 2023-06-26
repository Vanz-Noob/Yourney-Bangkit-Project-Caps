import React from "react";
import {
  Brand,
  Footer,
  Home,
  Member,
  Navigation,
  Portofolio,
} from "../commponents/Portal";

const DefaultLayoutPortal = () => {
  return (
    <div>
      <Navigation />
      <Home />
      <Brand />
      <Portofolio />
      <Member />
      <Footer />
    </div>
  );
};

export default DefaultLayoutPortal;
