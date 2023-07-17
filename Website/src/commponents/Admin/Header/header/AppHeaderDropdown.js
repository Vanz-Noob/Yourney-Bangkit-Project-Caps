import React from "react";
import {
  CAvatar,
  CDropdown,
  CDropdownHeader,
  CDropdownItem,
  CDropdownMenu,
  CDropdownToggle,
} from "@coreui/react";
import CIcon from "@coreui/icons-react";
import { cilAccountLogout } from "@coreui/icons";
import avatar8 from "../../../../assets/logo/img/user.png";
import axios from "../../../../api/axios";
import useAuth from "../../../../hooks/useAuth";
import { useNavigate } from "react-router-dom";
import removeCookie from "../../../../hooks/removeCookie";
import getCookie from "../../../../hooks/getCookie";

const AppHeaderDropdown = () => {
  const { auth } = useAuth();
  const navigate = useNavigate();
  const handleOut = () => {
    axios
      .delete("/logout", {
        headers: {
          Authorization: `Bearer ${auth.accessToken}`,
        },
      })
      .then((res) => {
        removeCookie("usrin");
        navigate("/adminYourney");
        return res;
      })
      .catch((err) => {
        console.log(err);
      });
  };

  return (
    <CDropdown variant="nav-item">
      <CDropdownToggle placement="bottom-end" className="py-0" caret={false}>
        <CAvatar src={avatar8} size="md" />
      </CDropdownToggle>
      <CDropdownMenu className="pt-0" placement="bottom-end">
        <CDropdownHeader className="bg-light fw-semibold py-2">
          Account
        </CDropdownHeader>
        <CDropdownItem onClick={handleOut}>
          <CIcon icon={cilAccountLogout} className="me-2" />
          Logout
        </CDropdownItem>
      </CDropdownMenu>
    </CDropdown>
  );
};

export default AppHeaderDropdown;
