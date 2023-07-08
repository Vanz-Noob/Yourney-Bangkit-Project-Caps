import React from "react";
import CIcon from "@coreui/icons-react";
import {
  cilNotes,
  cilSpeedometer,
  cilStar,
  cilInput,
  cilFile,
} from "@coreui/icons";
import { CNavGroup, CNavItem, CNavTitle } from "@coreui/react";

const _nav = [
  {
    component: CNavItem,
    name: "Dashboard",
    to: "/adminYourney/dashboard",
    icon: <CIcon icon={cilSpeedometer} customClassName="nav-icon" />,
  },

  {
    component: CNavItem,
    name: "Tambah Destinasi",
    to: "/adminYourney/forms",
    icon: <CIcon icon={cilNotes} customClassName="nav-icon" />,
  },
  {
    component: CNavItem,
    name: "List Destinasi",
    to: "/adminYourney/data",
    icon: <CIcon icon={cilFile} customClassName="nav-icon" />,
  },
  // {
  //   component: CNavGroup,
  //   name: "Data",
  //   icon: <CIcon icon={cilStar} customClassName="nav-icon" />,
  //   items: [
  //     {
  //       component: CNavItem,
  //       name: "Edit Data",
  //       to: "?",
  //     },
  //   ],
  // },
];

export default _nav;
