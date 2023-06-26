import { useContext } from "react";
import AuthContext from "../middleware/authProvider";

const useAuth = () => {
  return useContext(AuthContext);
};

export default useAuth;
