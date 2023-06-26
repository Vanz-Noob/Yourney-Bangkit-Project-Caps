import { useEffect } from "react";
import { useRecoilValue } from "recoil";
import { authenticated } from "../store";
import { useNavigate } from "react-router";

function Auth(props) {
  const auth = useRecoilValue(authenticated);
  const navigate = useNavigate();
  useEffect(() => {
    if (!auth.check) {
      navigate("/adminYourney");
    }
  }, []);
  return props.children;
}

export default Auth;
