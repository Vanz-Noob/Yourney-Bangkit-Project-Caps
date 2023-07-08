import React from "react";
import "./styles.css";
import { Ibackground1 } from "../../../assets/bg";
import { CContainer } from "@coreui/react";

function Home() {
  return (
    <div
      style={{
        backgroundImage: `url(${Ibackground1})`,
        backgroundRepeat: "no-repeat",
        backgroundSize: "cover",
        height: "100vh",
        width: "100%",

        backgroundPosition: "center center",
        zIndex: -99,
      }}
      id="Home"
    >
      <CContainer
        style={{
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          height: "100vh",
        }}
      >
        <h1 style={{ color: "#ffff", textAlign: "center" }} className="tag">
          MAKE YOUR JOURNEY YOURS
        </h1>
      </CContainer>
    </div>
  );
}

export default Home;
