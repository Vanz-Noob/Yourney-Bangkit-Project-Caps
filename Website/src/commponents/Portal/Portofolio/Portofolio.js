import React from "react";
import "./styles.css";
import { CCard, CCardTitle, CCardText, CRow, CCol } from "@coreui/react";
import { Iplaystore } from "../../../assets/logo";
import { Ibackground } from "../../../assets/bg";
import {
  Ismartphone2,
  Ismartphone3,
  Ismartphone4,
  Ismartphone5,
} from "../../../assets/Smartphone";

function Portofolio() {
  return (
    <div
      id="Portofolio"
      className="Portofolio"
      style={{
        backgroundImage: `url(${Ibackground})`,
        backgroundSize: "cover",
        width: "100%",
        height: "100vh",
      }}
    >
      <CRow className="Pdesk">
        <CCol className="col1 Pflex" sm={5}>
          {[{ color: "rgb(1,1,1,0)" }].map((item, index) => (
            <CCard className={`Pcard border-${item.color}`} key={index}>
              <CCardTitle className="Ptitle">OUR APPLICATION</CCardTitle>
              <CCardText className="Ptext">
                Yourney merupakan aplikasi rekomendasi traveling berbasis
                android yang bertujuan untuk membantu meningkatkan pendapatan
                kepariwisataan Indonesia dan dapat membantu pengguna untuk
                mendapatkan rekomendasi wisata. Pengguna akan mendapatkan
                rekomendasi berdasarkan sosial media Twitter dan diproses
                menggunakan Machine Learning untuk mendapatkan hasil rekomendasi
                wisatanya.
              </CCardText>
            </CCard>
          ))}
          <a
            href="https://play.google.com/store/apps/details?id=com.bangkit.yourney"
            className="Plink"
            target="_blank"
          >
            <img src={Iplaystore} className="Limg"></img>
          </a>
        </CCol>
        <CCol sm={7} className="col1">
          <CCol className="col-img">
            <img src={Ismartphone5} className="Pimg-left1" />
            <img src={Ismartphone2} className="Pimg-right1" />
          </CCol>
          <CCol className="col-img">
            <img src={Ismartphone4} className="Pimg-left2" />

            <img src={Ismartphone3} className="Pimg-right2" />
          </CCol>
        </CCol>
      </CRow>
    </div>
  );
}

export default Portofolio;