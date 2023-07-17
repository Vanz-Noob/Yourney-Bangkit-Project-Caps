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

const Destinasi = () => {
  const { setDatadestinasi } = useContext(GetDestinasi);
  const [Destinasi, setDestinasi] = useState([]);
  const [loop, setLoop] = useState();
  const { auth } = useAuth();
  const [length, setLength] = useState(200);
  const navigate = useNavigate();

  const arr = [];
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
          setDestinasi(element);
        }
      });
  }, []);
  console.log(Destinasi);
  const clickDestinasi = () => {
    setDatadestinasi(Destinasi[localStorage.getItem("index")].id_destinasi);
    navigate("/adminYourney/editDest");
  };

  // localStorage.setItem("modal", 0);

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
    </>
  );
};

export default Destinasi;
