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
    <CContainer className="containerBrand">
      <CRow className=" containterRow">
        <CCol className="side">
          {[{ color: "light" }].map((item, index) => (
            <CCard
              className={`text-center border-${item.color} text containerCard`}
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
        <CCol className="side">
          {[{ color: "light" }].map((item, index) => (
            <CCard
              className={`text-center border-${item.color} text containerCard`}
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
