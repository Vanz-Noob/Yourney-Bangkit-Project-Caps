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

const EditData = () => {
  const { auth } = useAuth();
  const { dataDestinasi } = useContext(GetDestinasi);
  const [idKetegori, setIdKategori] = useState();
  const [nama_desinasi, setNama_Destinasi] = useState("");
  const [deskripsi, setDeskripsi] = useState("");
  const [link, setLink] = useState("");
  const [url, setUrl] = useState("");
  const [alert, setAlert] = useState(false);
  const [color, setColor] = useState("alert");
  const [desk, setDesk] = useState("");
  const arr = [];
  const [des, setDes] = useState([]);
  const number = parseInt(localStorage.getItem("index"));

  const handleSubmit = async () => {
    try {
      const res = await axios.put(
        "/editDest",
        JSON.stringify({
          id_destinasi: number,
          id_kategori_destinasi: idKetegori,
          nama_desinasi: nama_desinasi,
          pic_destinasi: link,
          url_destinasi: url,
        }),

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
      setDesk("Input Berhasil!");
      setAlert(true);
      return res;
    } catch (err) {
      setColor("warning");
      setAlert(true);
      setDesk(err);
    }
  };
  // (-) select from ID destinasi
  useEffect(() => {
    axios
      .get("/destinasi", {
        headers: {
          Authorization: `Bearer ${getCookie("usrin").slice(1, -1)}`,
        },
      })
      .then((res) => {
        arr.push(res.data);

        for (let i = 0; i < arr.length; i++) {
          const element = arr[i];
          console.log(element);
          setIdKategori(element[number].id_kategori_destinasi);
          setDeskripsi(element[number].deskripsi);
          setNama_Destinasi(element[number].nama_desinasi);
          setLink(element[number].pic_destinasi);
          setUrl(element[number].url_destinasi);
          console.log("local", localStorage.getItem("index"));
          // if (
          //   element[i].id_destinasi === parseInt(localStorage.getItem("index"))
          // ) {
          //   console.log("test", dataDestinasi);
          //   setIdKategori(element[i].id_kategori_destinasi);
          //   setDeskripsi(element[i].deskripsi);
          //   setNama_Destinasi(element[i].nama_desinasi);
          //   setLink(element[i].pic_destinasi);
          //   setUrl(element[i].url_destinasi);
          // } else {
          //   console.log("er");
          // }
        }
      });
  }, []);

  // console.log(dataDestinasi);

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
            <CAlert
              color={color}
              dismissible
              visible={alert}
              onClose={() => setAlert(false)}
            >
              {desk}
            </CAlert>
          </CCardBody>
        </CCard>
      </CCol>
    </CRow>
  );
};

export default EditData;
