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
import GetDestinasi from "../../../hooks/getDestinasi";
import { useNavigate } from "react-router-dom";

const EditData = () => {
  const { auth } = useAuth();
  const { dataDestinasi } = useContext(GetDestinasi);
  const [idKetegori, setIdKategori] = useState(0);
  const [nama_desinasi, setNama_Destinasi] = useState("");
  const [idDestinasi, setIdDestinasi] = useState(0);
  const [deskripsi, setDeskripsi] = useState("");
  const [link, setLink] = useState("");
  const [url, setUrl] = useState("");
  const [alert, setAlert] = useState(false);
  const [color, setColor] = useState("success");
  const arr = [];
  const number = parseInt(localStorage.getItem("index"));

  const navigate = useNavigate();

  const handleSubmit = (e) => {
    e.preventDefault();
    axios
      .put(
        "/editDest",
        {
          id_destinasi: idDestinasi,
          id_kategori_destinasi: idKetegori,
          nama_destinasi: nama_desinasi,
          deskripsi: deskripsi,
          pic_destinasi: link,
          url_destinasi: url,
        },
        {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
        }
      )
      .then((res) => {
        setIdKategori();
        setNama_Destinasi("");
        setDeskripsi("");
        setLink("");
        setUrl("");
        setColor("success");
        setAlert(true);
        navigate("/adminYourney/data");
        return res;
      })
      .catch((err) => {
        setColor("danger");
        setAlert(true);
        console.log(err);
      });
  };
  // (-) select from ID destinasi
  useEffect(() => {
    axios
      .get("/destinasi", {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
      })
      .then((res) => {
        arr.push(res.data);

        for (let i = 0; i < arr.length; i++) {
          const element = arr[i];
          setIdDestinasi(element[number].id_destinasi);
          setIdKategori(element[number].id_kategori_destinasi);
          setDeskripsi(element[number].deskripsi);
          setNama_Destinasi(element[number].nama_desinasi);
          setLink(element[number].pic_destinasi);
          setUrl(element[number].url_destinasi);
        }
      });
  }, []);

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
              placeholder="ID Destinasi"
              aria-label="default input example"
              label="ID Destinasi"
              value={idDestinasi}
              onChange={(e) => setIdDestinasi(e.target.value)}
              style={{ pointerEvents: "none" }}
              required
            />
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
            <CAlert
              color={color}
              dismissible
              visible={alert}
              onClose={() => setAlert(false)}
            >
              success
            </CAlert>
          </CCardBody>
        </CCard>
      </CCol>
    </CRow>
  );
};

export default EditData;
