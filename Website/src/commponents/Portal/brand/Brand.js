import React from "react";
import {
  CCard,
  CCardBody,
  CCardTitle,
  CContainer,
  CRow,
  CCol,
} from "@coreui/react";
import {
  Ibangkit,
  Ibtp2,
  Igoogle2,
  Ikemendikbud,
} from "../../../assets/logo/index";
import "./styles.css";

function Brand() {
  return (
    <CContainer style={{ marginTop: 100, marginBottom: 100 }}>
      <CRow className="align-items-center justify-content-center">
        <CCol>
          {[{ color: "light" }].map((item, index) => (
            <CCard
              style={{
                backgroundColor: "#dfebd9",
                width: "35rem",
                borderRadius: 20,
                color: "#8A4200",
              }}
              className={`text-center border-${item.color} text`}
              key={index}
            >
              <CCardTitle>Funded by:</CCardTitle>
              <CCardBody>
                <img
                  src={Ikemendikbud}
                  width={90}
                  style={{ marginLeft: 20, marginRight: 20 }}
                  alt=""
                />
                <img
                  src={Igoogle2}
                  width={150}
                  style={{ marginLeft: 20, marginRight: 20 }}
                  alt=""
                />
              </CCardBody>
            </CCard>
          ))}
        </CCol>
        <CCol>
          {[{ color: "light" }].map((item, index) => (
            <CCard
              style={{
                backgroundColor: "#dfebd9",
                width: "35rem",
                borderRadius: 20,
                color: "#8A4200",
              }}
              className={`text-center border-${item.color} text`}
            >
              <CCardTitle>Supported by:</CCardTitle>
              <CCardBody>
                <img
                  src={Ibtp2}
                  width={150}
                  style={{ marginLeft: 20, marginRight: 20 }}
                  alt=""
                />
                <img
                  src={Ibangkit}
                  width={70}
                  style={{ marginLeft: 20, marginRight: 20 }}
                  alt=""
                />
              </CCardBody>
            </CCard>
          ))}
        </CCol>
      </CRow>
    </CContainer>
  );
}

export default Brand;
