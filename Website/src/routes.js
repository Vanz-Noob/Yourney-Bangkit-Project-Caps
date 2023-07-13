import React from "react";

const Dashboard = React.lazy(() =>
  import("./commponents/Admin/Dashboard/index")
);
const Data = React.lazy(() => import("./commponents/Admin/Data/data"));

//Forms
const FormControl = React.lazy(() => import("./commponents/Admin/FormInput"));

const editDest = React.lazy(() =>
  import("./commponents/Admin/Editdata/editData")
);

// const Widgets = React.lazy(() => import("./commponents/Admin/widgets/Widgets"));

const routes = [
  { path: "/adminYourney/dasboard", exact: true, name: "admin" },
  { path: "/adminYourney/dashboard", name: "Dashboard", element: Dashboard },
  {
    path: "/adminYourney/forms",
    name: "Forms",
    element: FormControl,
  },
  { path: "/adminYourney/data", name: "Data", element: Data },
  { path: "/adminYourney/editDest", name: "editDest", element: editDest },
];

export default routes;
