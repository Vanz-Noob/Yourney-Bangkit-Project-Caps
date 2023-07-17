import React, { useState, useEffect } from "react";

import { CCard, CCardBody, CCol, CRow } from "@coreui/react";
import { CChartLine } from "@coreui/react-chartjs";
import { getStyle, hexToRgba } from "@coreui/utils";

import WidgetsDropdown from "./WidgetsDropdown";
import axios from "../../../api/axios";
import useAuth from "../../../hooks/useAuth";
import getCookie from "../../../hooks/getCookie";

const Dashboard = () => {
  const { auth } = useAuth();
  const [jan, setJan] = useState(0);
  const [feb, setFeb] = useState(0);
  const [mar, setMar] = useState(0);
  const [apr, setApr] = useState(0);
  const [mei, setMei] = useState(0);
  const [jun, setJun] = useState(0);
  const [jul, setJul] = useState(0);
  const [aug, setAug] = useState(0);
  const [sep, setSep] = useState(0);
  const [oct, setOct] = useState(0);
  const [nov, setNov] = useState(0);
  const [des, setDes] = useState(0);

  useEffect(() => {
    axios
      .get("/db", {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
      })
      .then((respone) => {
        for (let i = 0; i < respone.data.length; i++) {
          const element = respone.data[i].created_time;
          console.log(element.slice(0, 3));
          if ("Jan" === element.slice(8, 11)) {
            setJan(jan + i);
          } else if ("Feb" === element.slice(8, 11)) {
            setFeb(feb + i);
          } else if ("Mar" === element.slice(8, 11)) {
            setMar(mar + i);
          } else if ("Apr" === element.slice(8, 11)) {
            setApr(apr + i);
          } else if ("Mei" === element.slice(8, 11)) {
            setMei(mei + i);
          } else if ("Jun" === element.slice(8, 11)) {
            setJun(jun + i);
          } else if ("Jul" === element.slice(8, 11)) {
            setJul(jul + i);
          } else if ("Aug" === element.slice(8, 11)) {
            setAug(aug + i);
          } else if ("Sep" === element.slice(8, 11)) {
            setSep(sep + i);
          } else if ("Oct" === element.slice(8, 11)) {
            setOct(oct + i);
          } else if ("Nov" === element.slice(8, 11)) {
            setNov(nov + i);
          } else if ("Des" === element.slice(8, 11)) {
            setDes(des + i);
          } else {
            console.log("err");
          }
        }
      });
  }, []);

  return (
    <>
      <WidgetsDropdown />
      <CCard className="mb-4">
        <CCardBody>
          <CRow>
            <CCol sm={5}>
              <h4 id="traffic" className="card-title mb-0">
                User
              </h4>
              <div className="small text-medium-emphasis">
                January - December 2023
              </div>
            </CCol>
            <CCol sm={7} className="d-none d-md-block"></CCol>
          </CRow>
          <CChartLine
            style={{ height: "300px", marginTop: "40px" }}
            data={{
              labels: [
                "January",
                "February",
                "March",
                "April",
                "May",
                "June",
                "July",
                "August",
                "September",
                "October",
                "November",
                "December",
              ],
              datasets: [
                {
                  label: "My First dataset",
                  backgroundColor: hexToRgba(getStyle("--cui-info"), 10),
                  borderColor: getStyle("--cui-info"),
                  pointHoverBackgroundColor: getStyle("--cui-info"),
                  borderWidth: 2,
                  data: [
                    jan,
                    feb,
                    mar,
                    apr,
                    mei,
                    jun,
                    jul,
                    aug,
                    sep,
                    oct,
                    nov,
                    des,
                  ],
                  fill: true,
                },
              ],
            }}
            options={{
              maintainAspectRatio: false,
              plugins: {
                legend: {
                  display: false,
                },
              },
              scales: {
                x: {
                  grid: {
                    drawOnChartArea: false,
                  },
                },
                y: {
                  grid: {
                    drawOnChartArea: true,
                  },
                  ticks: {
                    maxTicksLimit: 5,
                  },
                },
              },
              elements: {
                line: {
                  tension: 0.4,
                },
                point: {
                  radius: 0,
                  hitRadius: 10,
                  hoverRadius: 4,
                },
              },
            }}
          />
        </CCardBody>
      </CCard>
    </>
  );
};

export default Dashboard;
