import {
  Navigate,
  Outlet,
} from "react-router";

import Sidebar from "./Sidebar";
import TopBar from "./TopBar";

import {
  getStoredStudent,
} from "../../utils/studentStorage";


export default function AppShell() {
  const student =
    getStoredStudent();

  if (!student) {
    return (
      <Navigate
        to="/setup"
        replace
      />
    );
  }

  return (
    <div className="app-shell">
      <Sidebar />

      <div className="app-main">
        <TopBar />

        <main className="app-content">
          <Outlet />
        </main>
      </div>
    </div>
  );
}