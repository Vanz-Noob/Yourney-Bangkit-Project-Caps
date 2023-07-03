import React from "react";
import "./styles.css";
import { CCol, CRow } from "@coreui/react";

function Highlight() {
  return (
    <>
      <CRow className="containerHighlight">
        <CRow>
          <CCol className="middle"></CCol>
          <CCol className="middle">
            <div className="containterText">
              <h1
                style={{ overflow: "hidden", textAlign: "center" }}
                className="Htext"
              >
                TOP 15
              </h1>
              <h5
                style={{ overflow: "hidden", textAlign: "center" }}
                className="header5"
              >
                PRODUCT CAPSTONE BANGKIT 2022
              </h5>
            </div>
            <div className="Rhombus"></div>
          </CCol>
          <CCol className="middle"></CCol>
        </CRow>
      </CRow>
    </>
  );
}

export default Highlight;
