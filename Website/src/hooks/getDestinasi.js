import { createContext, useState } from "react";

const GetDestinasi = createContext({});

export const DestinasiProvider = ({ children }) => {
  const [dataDestinasi, setDatadestinasi] = useState({});
  return (
    <GetDestinasi.Provider value={{ dataDestinasi, setDatadestinasi }}>
      {children}
    </GetDestinasi.Provider>
  );
};

export default GetDestinasi;
