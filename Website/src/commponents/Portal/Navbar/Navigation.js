import React, { useState } from "react";
import {
  CNavbar,
  CContainer,
  CNavbarBrand,
  CNavbarNav,
  CCollapse,
  CNavbarToggler,
  CNavItem,
  CNavLink,
} from "@coreui/react";
import "./styles.css";

import { Iyourney2 } from "../../../assets/logo/index";

const Navigation = () => {
  const [nav, setNav] = useState("");

  window.onscroll = function () {
    toggleVisible();
  };
  const toggleVisible = () => {
    const scrolled = document.documentElement.scrollTop;
    const scrolled2 = document.body.scrollTop;
    if (scrolled > 300 || scrolled2 > 300) {
      setNav("bg-dark trans");
    } else {
      setNav("trans");
    }
    console.log(scrolled);
  };

  const scrollToTop = () => {
    window.scrollTo({
      top: 0,
      behavior: "auto",
    });
  };
  console.log("ini", nav);
  window.addEventListener("scroll", toggleVisible);

  const [visible, setVisible] = useState(false);
  return (
    <div className="App" onScroll={scrollToTop}>
      <CNavbar
        expand="lg"
        colorScheme="dark"
        className={nav}
        placement="fixed-top"
      >
        <CContainer fluid>
          <CNavbarBrand href="#home" style={{ marginLeft: "2rem" }}>
            <img src={Iyourney2} height={60} />
          </CNavbarBrand>
          <CNavbarToggler onClick={() => setVisible(!visible)} />
          <CCollapse
            className="navbar-collapse justify-content-end"
            visible={visible}
            style={{ marginRight: "5rem" }}
          >
            <CNavbarNav>
              <CNavItem>
                <CNavLink href="#Portofolio">Portofolio</CNavLink>
              </CNavItem>
              <CNavItem>
                <CNavLink href="#Contact">Contact</CNavLink>
              </CNavItem>
            </CNavbarNav>
          </CCollapse>
        </CContainer>
      </CNavbar>
    </div>
  );
};

export default Navigation;
