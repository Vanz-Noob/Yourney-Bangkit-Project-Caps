import React, { useContext, useEffect, useState } from "react";
import axios from "../../../api/axios";
import {
  CButton,
  CCard,
  CCardBody,
  CCardHeader,
  CCol,
  CRow,
  CTable,
  CTableBody,
  CTableDataCell,
  CTableHead,
  CTableHeaderCell,
  CTableRow,
  CModal,
  CModalHeader,
  CModalTitle,
  CModalBody,
  CModalFooter,
} from "@coreui/react";
import useAuth from "../../../hooks/useAuth";
import getCookie from "../../../hooks/getCookie";
import GetDestinasi from "../../../hooks/getDestinasi";
import { useNavigate } from "react-router-dom";
import CIcon from "@coreui/icons-react";
import { cilTrash } from "@coreui/icons";

const Destinasi = () => {
  const { setDatadestinasi } = useContext(GetDestinasi);
  const [Destinasi, setDestinasi] = useState([]);
  const [idDes, setIdDes] = useState(0);
  const { auth } = useAuth();
  const navigate = useNavigate();
  const [visibleXL, setVisibleXL] = useState(false);
  const [visible, setVisible] = useState(false);
  const [n, setN] = useState(0);

  const arr = [];

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
          setDestinasi(element);
        }
      });
  }, []);
  const clickDestinasi = () => {
    setDatadestinasi(idDes);
    navigate("/adminYourney/editDest");
  };

  const handleDelete = () => {
    axios
      .delete("/delDest", {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
        data: {
          id_destinasi: localStorage.getItem("idDes"),
        },
      })
      .then((res) => {
        setVisible(false);
        window.location.reload();
        return res;
      })
      .catch((err) => {
        console.log(err);
      });
  };

  return (
    <>
      <CRow>
        <CCol xs>
          <CCard className="mb-4">
            <CCardHeader>List Data</CCardHeader>
            <CCardBody>
              <CTable
                align="middle"
                className="mb-0 border"
                hover
                responsive
                style={{ overflowX: "hidden" }}
              >
                <CTableHead color="light">
                  <CTableRow>
                    <CTableHeaderCell>Nama Destinasi</CTableHeaderCell>
                    <CTableHeaderCell>Deskripsi</CTableHeaderCell>
                    <CTableHeaderCell>Image</CTableHeaderCell>
                    <CTableHeaderCell>Action</CTableHeaderCell>
                  </CTableRow>
                </CTableHead>
                <CTableBody>
                  {Destinasi.map((item, index) => (
                    <CTableRow v-for="item in tableItems" key={index}>
                      <CTableDataCell>
                        <div>{item.nama_desinasi}</div>
                      </CTableDataCell>
                      <CTableDataCell>
                        <div style={{ width: 300 }}>
                          <p>{item.deskripsi}</p>
                        </div>
                      </CTableDataCell>
                      <CTableDataCell>
                        <div style={{ width: 200 }}>
                          <p>{item.pic_destinasi}</p>
                        </div>
                      </CTableDataCell>
                      <CTableDataCell>
                        <CRow xs={{ gutter: 2 }}>
                          <CCol xs lg={4}>
                            <CButton
                              color="success"
                              onClick={() => {
                                localStorage.setItem(
                                  "idDes",
                                  item.id_destinasi
                                );
                                localStorage.setItem(
                                  "idKatDes",
                                  item.id_kategori_destinasi
                                );
                                localStorage.setItem(
                                  "NamaDest",
                                  item.nama_desinasi
                                );
                                localStorage.setItem("Desk", item.deskripsi);
                                localStorage.setItem("pic", item.pic_destinasi);
                                localStorage.setItem("url", item.url_destinasi);
                                setVisibleXL(true);
                              }}
                            >
                              Detail
                            </CButton>
                          </CCol>
                          <CCol xs lg={3}>
                            <CButton
                              color="warning"
                              onClick={() => {
                                localStorage.setItem("index", index);
                                setIdDes(item.id_destinasi);
                                clickDestinasi();
                              }}
                            >
                              Edit
                            </CButton>
                          </CCol>
                          <CCol xs lg={2}>
                            <CButton
                              color="danger"
                              onClick={() => {
                                localStorage.setItem(
                                  "idDes",
                                  item.id_destinasi
                                );
                                localStorage.setItem(
                                  "NamaDest",
                                  item.nama_desinasi
                                );
                                setVisible(!visible);
                              }}
                            >
                              <CIcon icon={cilTrash} />
                            </CButton>
                          </CCol>
                        </CRow>
                      </CTableDataCell>
                    </CTableRow>
                  ))}
                </CTableBody>
              </CTable>
            </CCardBody>
          </CCard>
        </CCol>
      </CRow>
      <CModal size="xl" visible={visibleXL} onClose={() => setVisibleXL(false)}>
        <CModalHeader>
          <CModalTitle>Detail Destinasi</CModalTitle>
        </CModalHeader>
        <CModalBody>
          <CTable align="middle" className="mb-0 border" hover responsive>
            <CTableHead color="light">
              <CTableRow>
                <CTableHeaderCell>Id Destinasi</CTableHeaderCell>
                <CTableHeaderCell>Id Kategori Destinasi</CTableHeaderCell>
                <CTableHeaderCell>Nama Destinasi</CTableHeaderCell>
                <CTableHeaderCell>Deskripsi</CTableHeaderCell>
                <CTableHeaderCell>Image</CTableHeaderCell>
                <CTableHeaderCell>url Destinasi</CTableHeaderCell>
              </CTableRow>
            </CTableHead>
            <CTableBody>
              <CTableRow v-for="item in tableItems">
                <CTableDataCell>
                  <div>{localStorage.getItem("idDes")}</div>
                </CTableDataCell>
                <CTableDataCell>
                  <div>{localStorage.getItem("idKatDes")}</div>
                </CTableDataCell>
                <CTableDataCell>
                  <div>{localStorage.getItem("NamaDest")}</div>
                </CTableDataCell>
                <CTableDataCell>
                  <div style={{ width: 300 }}>
                    <p>{localStorage.getItem("Dest")}</p>
                  </div>
                </CTableDataCell>
                <CTableDataCell>
                  <div style={{ width: 200 }}>
                    <p>{localStorage.getItem("pic")}</p>
                  </div>
                </CTableDataCell>
                <CTableDataCell>
                  <div>{localStorage.getItem("url")}</div>
                </CTableDataCell>
              </CTableRow>
            </CTableBody>
          </CTable>
        </CModalBody>
        <CModalFooter></CModalFooter>
      </CModal>

      {/* alert modal */}

      <CModal visible={visible} onClose={() => setVisible(false)}>
        <CModalHeader>
          <CModalTitle>Delete destinasi?</CModalTitle>
        </CModalHeader>
        <CModalBody>
          <p>
            Anda yakin menghapus destinasi ini id:
            {localStorage.getItem("idDes")} dan Nama Destinasi :{" "}
            {localStorage.getItem("NamaDest")}?
          </p>
        </CModalBody>
        <CModalFooter>
          <CButton onClick={() => setVisible(false)}>Tidak</CButton>
          <CButton onClick={handleDelete}>Iya</CButton>
        </CModalFooter>
      </CModal>
    </>
  );
};

export default Destinasi;
