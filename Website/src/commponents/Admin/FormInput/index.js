import React, { useState, useEffect } from "react";
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
} from "@coreui/react";
import axios from "../../../api/axios";
import useAuth from "../../../hooks/useAuth";
import getCookie from "../../../hooks/getCookie";

const FormControl = () => {
  const { auth } = useAuth();

  // const [idDestinasi, setIdDestinasi] = useState();
  const [idKetegori, setIdKategori] = useState();
  const [nama_desinasi, setNama_Destinasi] = useState("");
  const [deskripsi, setDeskripsi] = useState("");
  const [link, setLink] = useState("");
  const [url, setUrl] = useState("");

  const handleSubmit = async (e) => {
    try {
      const res = await axios.post(
        "/addDest",
        JSON.stringify({ idKetegori, nama_desinasi, deskripsi, link, url }),
        {
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${getCookie("usrin").slice(1, -1)}`,
          },
        }
      );
      setIdKategori();
      setNama_Destinasi("");
      setDeskripsi("");
      setLink("");
      setUrl("");
    } catch (err) {
      console.log(err);
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
            {/* <CFormInput
              type="number"
              placeholder="ID Destinasi"
              aria-label="default input example"
              label="ID Destinasi"
              onChange={(e) => setIdDestinasi(e.target.value)}
              required
            /> */}
            <br />
            <CFormInput
              type="number"
              placeholder="ID Kategori Destinasi"
              aria-label="default input example"
              label="ID Kategori Destinasi"
              onChange={(e) => setIdKategori(e.target.value)}
              required
            />
            <br />
            <CFormInput
              type="text"
              placeholder="Nama Destinasi"
              aria-label="default input example"
              label="Nama Desitinasi"
              onChange={(e) => setNama_Destinasi(e.target.value)}
              required
            />
            <br />
            <CInputGroup>
              <CInputGroupText>Deskripsi</CInputGroupText>

              <CFormTextarea
                aria-label="With textarea"
                onChange={(e) => setDeskripsi(e.target.value)}
                required
              ></CFormTextarea>
            </CInputGroup>
            <br />
            <CFormInput
              type="text"
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
              aria-label="default input example"
              label="Url Destinasi"
              onChange={(e) => setUrl(e.target.value)}
              required
            />
            <br />
            <CButton type="submit" className="mb-3" onClick={handleSubmit}>
              Submit
            </CButton>
          </CCardBody>
        </CCard>
      </CCol>
    </CRow>
  );
};

export default FormControl;
