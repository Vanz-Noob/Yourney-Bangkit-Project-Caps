import React, { useRef, useEffect, useState, useContext } from "react";

import { Link, useNavigate, Navigate, useLocation } from "react-router-dom";
import {
  CButton,
  CCard,
  CCardBody,
  CCardGroup,
  CCol,
  CContainer,
  CForm,
  CFormInput,
  CInputGroup,
  CInputGroupText,
  CRow,
  CAlert,
  CSpinner,
} from "@coreui/react";

import { Ibackground1 } from "../../../assets/bg/index";
import axios from "../../../api/axios";
import { FaRegUser, FaLock } from "react-icons/fa";
import useAuth from "../../../hooks/useAuth";
import setCookie from "../../../hooks/setCookie";
import removeCookie from "../../../hooks/removeCookie";

const Login = () => {
  const { setAuth } = useAuth();

  const navigate = useNavigate();
  const location = useLocation();
  const from = location.state?.from?.pathname || "/adminYourney/dashboard";

  const [username, setUsername] = useState("");
  const [password, setPass] = useState("");
  const [visible, setVisible] = useState(false);
  const [errmsg, setErrmsg] = useState("");
  const [visual, setVisual] = useState("visually-hidden");

  const userRef = useRef();
  const errRef = useRef();

  useEffect(() => {
    userRef.current.focus();
  }, []);

  useEffect(() => {
    setErrmsg("");
  }, [username, password]);
  removeCookie("usrin");

  const handleSubmit = async (e) => {
    setVisual("");

    e.preventDefault();

    try {
      // Using Axios

      const res = await axios.post(
        "/login",
        JSON.stringify({ username, password }),
        {
          headers: {
            "Content-Type": "application/json",
            withCredentials: true,
            "Access-Control-Allow-Origin": "*", // Required for CORS support to work
            "Access-Control-Allow-Credentials": true, // Required for cookies, authorization headers with HTTPS
          },
          // timeout: 5000,
        }
      );

      // Using Fetch

      // const res = await fetch("https://yourney-api.et.r.appspot.com/login", {
      //   method: "POST",
      //   mode: "cors",
      //   headers: {
      //     "Content-Type": "application/json",
      //   },
      //   credentials: "same-origin",
      //   body: JSON.stringify({ username, password }),
      // });
      setCookie("usrin", JSON.stringify(res.data.access));
      const accessToken = res?.data?.access;
      localStorage.setItem("token", accessToken);
      setAuth({ username, password, accessToken });
      console.log("berhasil");
      setUsername("");
      setPass("");
      navigate(from, { replace: true });

      return res;
    } catch (err) {
      setVisual("visually-hidden");

      if (!err.response) {
        setErrmsg("No server respone");
        setVisible(true);
      } else if (err.response.status === 400) {
        setErrmsg("Username atau password salah");
        setVisible(true);
      } else if (err.response.status === 401) {
        setErrmsg("Unauthorized");
        setVisible(true);
      } else {
        setErrmsg("Login Failed");
        setVisible(true);
      }
      // errRef.current.focus();
    }
  };

  return (
    <section className="bg-light min-vh-100 d-flex flex-row align-items-center">
      <CContainer>
        <CRow className="justify-content-center">
          <CCol md={8}>
            <CCardGroup>
              <CCard className="p-4">
                <CCardBody>
                  <CForm>
                    <h1>Login</h1>
                    <p className="text-medium-emphasis">Sign In for admin</p>
                    <CAlert
                      color="warning"
                      dismissible
                      visible={visible}
                      onClose={() => setVisible(false)}
                    >
                      {errmsg}
                    </CAlert>
                    <CInputGroup className="mb-3">
                      <CInputGroupText>
                        <FaRegUser />
                      </CInputGroupText>
                      <CFormInput
                        ref={userRef}
                        placeholder="Username"
                        autoComplete="username"
                        onChange={(e) => setUsername(e.target.value)}
                        required
                      />
                    </CInputGroup>
                    <CInputGroup className="mb-4">
                      <CInputGroupText>
                        <FaLock />
                      </CInputGroupText>
                      <CFormInput
                        ref={userRef}
                        type="password"
                        placeholder="Password"
                        onChange={(e) => setPass(e.target.value)}
                        required
                      />
                    </CInputGroup>
                    <CRow>
                      <CCol xs={6}>
                        <CButton
                          color="primary"
                          className="px-4"
                          onClick={handleSubmit}
                          type="submit"
                        >
                          Login
                          <CSpinner
                            className={`${visual}`}
                            component="span"
                            size="sm"
                            aria-hidden="true"
                            style={{ marginLeft: 10 }}
                          />
                        </CButton>
                      </CCol>
                    </CRow>
                  </CForm>
                </CCardBody>
              </CCard>
              <CCard
                className="text-white bg-primary py-5"
                style={{
                  width: "44%",
                  backgroundImage: `url(${Ibackground1})`,
                  backgroundRepeat: "no-repeat",
                  backgroundSize: "cover",
                  backgroundPosition: "center",
                }}
              >
                <CCardBody className="text-center">
                  <div>
                    <h2>Yourney</h2>
                    <p>Make Your Journey</p>
                  </div>
                </CCardBody>
              </CCard>
            </CCardGroup>
          </CCol>
        </CRow>
      </CContainer>
    </section>
  );
};

export default Login;
