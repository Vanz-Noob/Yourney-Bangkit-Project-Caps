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
  const [loop, setLoop] = useState();
  const { auth } = useAuth();
  const [length, setLength] = useState(200);
  const navigate = useNavigate();
  const [visibleXL, setVisibleXL] = useState(false);
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
  console.log(Destinasi);
  const clickDestinasi = () => {
    setDatadestinasi(Destinasi[localStorage.getItem("index")].id_destinasi);
    navigate("/adminYourney/editDest");
  };
  // console.log(Destinasi[n].id_destinasi);
  const handleDelete = () => {
    axios
      .delete(
        "/delDest",

        {
          headers: {
            Authorization: `Bearer ${auth.accessToken}`,
          },
          data: {
            id_destinasi: localStorage.getItem("idDes"),
          },
        }
      )
      .then((res) => {
        setVisibleXL(false);
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
              <CTable align="middle" className="mb-0 border" hover responsive>
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
                    <CTableRow
                      v-for="item in tableItems"
                      key={index}
                      onClick={() => {
                        setN(index);
                        localStorage.setItem("idDes", item.id_destinasi);
                        localStorage.setItem(
                          "idKatDes",
                          item.id_kategori_destinasi
                        );
                        localStorage.setItem("NamaDest", item.nama_desinasi);
                        localStorage.setItem("Desk", item.deskripsi);
                        localStorage.setItem("pic", item.pic_destinasi);
                        localStorage.setItem("url", item.url_destinasi);
                        setVisibleXL(true);
                      }}
                    >
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
                        <CButton
                          color="warning"
                          onClick={() => {
                            localStorage.setItem("index", index);
                            clickDestinasi();
                          }}
                        >
                          Edit
                        </CButton>
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
        <CModalFooter>
          <CButton color="danger" onClick={handleDelete}>
            <CIcon icon={cilTrash} />
          </CButton>
        </CModalFooter>
      </CModal>
    </>
  );
};

export default Destinasi;
