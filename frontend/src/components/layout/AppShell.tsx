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


  // ======================================
  // No active learner session
  //
  // After logout the stored student
  // is removed, so protected routes
  // return the learner to /login.
  // ======================================

  if (
    !student
  ) {

    return (

      <Navigate
        to="/login"
        replace
      />

    );
  }


  // ======================================
  // Authenticated application shell
  // ======================================

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