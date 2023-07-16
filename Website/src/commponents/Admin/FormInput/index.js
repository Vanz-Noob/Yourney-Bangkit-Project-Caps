import React, { useState, useEffect, useContext } from "react";
import {
  CButton,
  CCard,
  CCardBody,
  CCardHeader,
  CCol,
  CFormInput,
  CRow,
  CInputGroup,
  CInputGroupText,
  CFormTextarea,
  CAlert,
} from "@coreui/react";
import axios from "../../../api/axios";
import useAuth from "../../../hooks/useAuth";
import getCookie from "../../../hooks/getCookie";

const FormControl = () => {
  const { auth } = useAuth();
  const [idKetegori, setIdKategori] = useState();
  const [nama_desinasi, setNama_Destinasi] = useState("");
  const [deskripsi, setDeskripsi] = useState("");
  const [link, setLink] = useState("");
  const [url, setUrl] = useState("");
  const [success, setSuccess] = useState(false);
  const [color, setColor] = useState("success");
  const [desk, setDesk] = useState("");
  const arr = [];
  const [des, setDes] = useState([]);

  const handleSubmit = async () => {
    try {
      const res = await axios.post(
        "/addDest",
        JSON.stringify({
          id_kategori_destinasi: idKetegori,
          nama_destinasi: nama_desinasi,
          deskripsi,
          pic_destinasi: link,
          url_destinasi: url,
        }),
        {
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${getCookie("usrin").slice(1, -1)}`,
            "Access-Control-Allow-Origin": "*", // Required for CORS support to work
            "Access-Control-Allow-Credentials": true,
          },
        }
      );
      setIdKategori();
      setNama_Destinasi("");
      setDeskripsi("");
      setLink("");
      setUrl("");
      setDesk("Input Berhasil!");
      console.log("input berhasil");
      setSuccess(true);
    } catch (err) {
      setColor("warning");
      setSuccess(true);
      console.log(err);

      setDesk(err);
    }
  };

  return (
    <CRow>
      <CCol xs={12}>
        <CCard className="mb-4">
          <CCardHeader>
            <strong>Input Data Destinasi</strong>
          </CCardHeader>
          <CCardBody>
            <br />
            <CFormInput
              type="number"
              placeholder="ID Kategori Destinasi"
              aria-label="default input example"
              label="ID Kategori Destinasi"
              value={idKetegori}
              onChange={(e) => setIdKategori(e.target.value)}
              required
            />
            <br />
            <CFormInput
              type="text"
              placeholder="Nama Destinasi"
              aria-label="default input example"
              label="Nama Desitinasi"
              value={nama_desinasi}
              onChange={(e) => setNama_Destinasi(e.target.value)}
              required
            />
            <br />
            <CInputGroup>
              <CInputGroupText>Deskripsi</CInputGroupText>

              <CFormTextarea
                aria-label="With textarea"
                value={deskripsi}
                onChange={(e) => setDeskripsi(e.target.value)}
                required
              ></CFormTextarea>
            </CInputGroup>
            <br />
            <CFormInput
              type="text"
              value={link}
              placeholder="Link Gambar Destinasi"
              aria-label="default input example"
              label="Link Gambar Destinasi"
              onChange={(e) => setLink(e.target.value)}
              required
            />
            <br />
            <CFormInput
              type="text"
              placeholder="Url Destinasi"
              value={url}
              aria-label="default input example"
              label="Url Destinasi"
              onChange={(e) => setUrl(e.target.value)}
              required
            />
            <br />
            <CButton type="submit" className="mb-3" onClick={handleSubmit}>
              Submit
            </CButton>
            {/* <CAlert
              color={color}
              dismissible
              visible={success}
              onClose={() => setSuccess(false)}
            >
              {desk}
            </CAlert> */}
          </CCardBody>
        </CCard>
      </CCol>
    </CRow>
  );
};

export default FormControl;
