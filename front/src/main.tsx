import * as React from "react";
import * as ReactDOM from "react-dom/client";
import {
  createBrowserRouter,
  RouterProvider,
  RouteObject,
} from "react-router-dom";
import "./index.css";
import Orders from "./routes/Orders";

const router: RouteObject[] = [
  {
    path: "/",
    element: <div>Hello world!</div>,
  },
  {
    path: "/orders",
    element: <Orders/>,
  },
];

const root = ReactDOM.createRoot(
  document.getElementById("root") as HTMLElement
);

root.render(
  <React.StrictMode>
    <RouterProvider router={createBrowserRouter(router)} />
  </React.StrictMode>
);
