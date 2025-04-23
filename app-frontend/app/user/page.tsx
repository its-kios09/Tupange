"use client";
import { Logout, Notification as NotificationIcon } from "@carbon/icons-react";
import {
  Content,
  Header,
  HeaderContainer,
  HeaderGlobalAction,
  HeaderGlobalBar,
  HeaderMenuButton,
  HeaderName,
  HeaderPanel,
  InlineLoading,
  InlineNotification,
  SideNav,
  SideNavItems,
  SideNavMenu,
  SideNavMenuItem,
  Tile,
} from "@carbon/react";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";
import { useAuth } from "../context/auth-context";
import styles from "./page.module.scss";
import IncomingAppointments from "./appointments-incoming/page";
import { UserAvatar } from "@carbon/ibm-products";
import { ActiveComponent, Doctor, Patient, Notification } from "../types";
import UserPanelWorkspace from "../workspace/user-panel";

export default function Dashboard() {
  const { user, logout, isLoading, getPatientProfile, getDoctorProfile } =
    useAuth();
  const [patientData, setPatientData] = useState<Patient | null>(null);
  const [doctorData, setDoctorData] = useState<Doctor | null>(null);
  const [patientLoading, setPatientLoading] = useState(false);
  const [doctorLoading, setDoctorLoading] = useState(false);

  const router = useRouter();
  const { t } = useTranslation();

  const [activeComponent, setActiveComponent] = useState<ActiveComponent>(
    "incoming-appointments"
  );

  const [notifications, setNotifications] = useState<Notification[]>([]);
  const [hasUnreadNotifications, setHasUnreadNotifications] = useState(false);
  const [notificationsOpen, setNotificationsOpen] = useState(false);
  const [userMenuOpen, setUserMenuOpen] = useState(false);
  const [panelExpanded, setPanelExpanded] = useState(false);

  const [snackbar, setSnackbar] = useState({
    isOpen: false,
    message: "",
    kind: "error" as "error" | "success" | "info" | "warning",
  });

  useEffect(() => {
    const fetchUserData = async () => {
      if (!user) return;

      try {
        if (user.role === "patient") {
          setPatientLoading(true);
          const patients = await getPatientProfile();
          if (patients && patients.length > 0) {
            setPatientData(patients[0]);
          } else {
            setNotifications((prev) => [
              {
                id: "account-pending",
                title: "Account Pending Approval",
                message:
                  "Your account has not been approved by an available doctor or admin yet. Please wait for approval.",
                timestamp: new Date().toISOString(),
                unread: true,
              },
              ...prev,
            ]);
          }
        } else if (user.role === "doctor") {
          setDoctorLoading(true);
          const doctors = await getDoctorProfile();
          if (doctors && doctors.length > 0) {
            setDoctorData(doctors[0]);
          }
        }
      } catch (error) {
        console.error("Failed to fetch user data:", error);
        setSnackbar({
          isOpen: true,
          message: "Failed to load user information",
          kind: "error",
        });
      } finally {
        setPatientLoading(false);
        setDoctorLoading(false);
      }
    };

    fetchUserData();
  }, [user, getPatientProfile, getDoctorProfile]);

  useEffect(() => {
    const hasUnread = notifications.some((notification) => notification.unread);
    setHasUnreadNotifications(hasUnread);
  }, [notifications]);

  useEffect(() => {
    if (notificationsOpen) {
      setNotifications((prev) =>
        prev.map((notification) => ({ ...notification, unread: false }))
      );
    }
  }, [notificationsOpen]);

  useEffect(() => {
    if (snackbar.isOpen) {
      const timer = setTimeout(() => {
        setSnackbar((prev) => ({ ...prev, isOpen: false }));
      }, 6000);
      return () => clearTimeout(timer);
    }
  }, [snackbar.isOpen]);

  const handleLogout = async () => {
    try {
      const success = await logout();
      if (success) {
        setSnackbar({
          isOpen: true,
          message: t(
            "logoutSuccess",
            "You have successfully logged out! Redirecting..."
          ),
          kind: "success",
        });
        setTimeout(() => router.push("/"), 1500);
      }
    } catch (error) {
      console.error("Logout failed:", error);
      setSnackbar({
        isOpen: true,
        message: t(
          "logoutError",
          "An error occurred while logging out. Please try again."
        ),
        kind: "error",
      });
    }
  };
  const renderActiveComponent = () => {
    switch (activeComponent) {
      case "incoming-appointments":
        return <IncomingAppointments />;
      default:
        return (
          <div>Welcome to Tupange Portal! Select an option from the menu.</div>
        );
    }
  };

  if (isLoading || patientLoading || doctorLoading) {
    return <InlineLoading description="Loading..." />;
  }

  const showPendingApprovalIndicator =
    user?.role === "patient" && !patientData && !patientLoading;

  return (
    <>
      {snackbar.isOpen && (
        <div className={styles.snackbarContainer}>
          <InlineNotification
            kind={snackbar.kind}
            title={
              snackbar.kind === "error"
                ? t("error", "Error")
                : t("success", "Success")
            }
            subtitle={snackbar.message}
            onCloseButtonClick={() =>
              setSnackbar((prev) => ({ ...prev, isOpen: false }))
            }
            hideCloseButton={true}
            lowContrast={true}
          />
        </div>
      )}

      <HeaderContainer
        render={({ isSideNavExpanded, onClickSideNavExpand }) => (
          <>
            <Header aria-label="Tupange Portal Header">
              <HeaderMenuButton
                aria-label={isSideNavExpanded ? "Close menu" : "Open menu"}
                onClick={onClickSideNavExpand}
                isActive={isSideNavExpanded}
              />
              <HeaderName href="/user" prefix="">
                Tupange Portal
              </HeaderName>

              <HeaderGlobalBar>
                <HeaderGlobalAction
                  aria-label="User options"
                  isActive={userMenuOpen}
                  onClick={() => {
                    setUserMenuOpen((prev) => !prev);
                    setNotificationsOpen(false);
                  }}
                  tooltipAlignment="end"
                >
                  <UserAvatar className={styles.navUserAvatar} />
                </HeaderGlobalAction>
                <HeaderGlobalAction
                  aria-label="Notifications"
                  aria-expanded={notificationsOpen}
                  isActive={notificationsOpen}
                  onClick={() => {
                    setNotificationsOpen((prev) => !prev);
                    setUserMenuOpen(false);
                  }}
                  tooltipAlignment="end"
                >
                  {(hasUnreadNotifications || showPendingApprovalIndicator) &&
                  !notificationsOpen ? (
                    <div
                      style={{ position: "relative" }}
                      title="Unread notifications"
                    >
                      <NotificationIcon size={20} />
                      <span
                        style={{
                          position: "absolute",
                          top: "-5px",
                          right: "-5px",
                          width: "10px",
                          height: "10px",
                          borderRadius: "50%",
                          backgroundColor: "#0f62fe",
                          border: "1px solid white",
                        }}
                        aria-hidden="true"
                      />
                    </div>
                  ) : (
                    <NotificationIcon size={20} />
                  )}
                </HeaderGlobalAction>
                <HeaderGlobalAction
                  aria-label="Logout"
                  onClick={handleLogout}
                  tooltipAlignment="end"
                >
                  <Logout size={20} />
                </HeaderGlobalAction>
              </HeaderGlobalBar>

              {user && (
                <UserPanelWorkspace
                  expanded={userMenuOpen}
                  user={user}
                  patientData={patientData}
                  doctorData={doctorData}
                  onClose={() => setUserMenuOpen(false)}
                />
              )}

              <HeaderPanel
                aria-label="Notifications panel"
                expanded={notificationsOpen}
              >
                <div
                  style={{
                    padding: "1rem",
                    minWidth: "300px",
                    maxWidth: "400px",
                    marginBottom: "1rem",
                  }}
                >
                  <h4>Notifications</h4>
                  {notifications.length === 0 ? (
                    <p>No new notifications.</p>
                  ) : (
                    <ul style={{ listStyle: "none", padding: 0 }}>
                      {notifications.map((n) => (
                        <li key={n.id}>
                          {n.id === "account-pending" ? (
                            <InlineNotification
                              kind="warning"
                              title="Account Pending Approval"
                              children={
                                <div style={{ lineHeight: 1.5 }}>
                                  Your account has not been approved by an
                                  available doctor or admin yet.
                                  <div
                                    style={{
                                      marginTop: "0.5rem",
                                      fontSize: "0.875rem",
                                      color: "#697077",
                                    }}
                                  >
                                    {new Date(n.timestamp).toLocaleString()}
                                  </div>
                                </div>
                              }
                              lowContrast={true}
                              hideCloseButton={true}
                              style={{ marginBottom: "1rem" }}
                            />
                          ) : (
                            <InlineNotification
                              kind="success"
                              title={n.title}
                              children={
                                <div style={{ lineHeight: 1.5 }}>
                                  {n.message}
                                  <div
                                    style={{
                                      marginTop: "0.5rem",
                                      fontSize: "0.875rem",
                                      color: "#697077",
                                    }}
                                  >
                                    {new Date(n.timestamp).toLocaleString()}
                                  </div>
                                </div>
                              }
                              hideCloseButton={true}
                              style={{ marginBottom: "1rem" }}
                            />
                          )}
                        </li>
                      ))}
                    </ul>
                  )}
                </div>
              </HeaderPanel>

              <SideNav
                aria-label="Side navigation"
                expanded={isSideNavExpanded}
                onSideNavBlur={onClickSideNavExpand}
                href="#main-content"
              >
                <SideNavItems>
                  <SideNavMenu title="Appointments" defaultExpanded>
                    <SideNavMenuItem
                      href="#"
                      onClick={(e: React.MouseEvent<HTMLAnchorElement>) => {
                        e.preventDefault();
                        setActiveComponent("incoming-appointments");
                        if (!isSideNavExpanded) onClickSideNavExpand();
                      }}
                      isActive={activeComponent === "incoming-appointments"}
                    >
                      Incoming Appointments
                    </SideNavMenuItem>
                    <SideNavMenuItem
                      href="#"
                      onClick={(e: React.MouseEvent<HTMLAnchorElement>) => {
                        e.preventDefault();
                        setActiveComponent("past-appointments");
                        if (!isSideNavExpanded) onClickSideNavExpand();
                      }}
                      isActive={activeComponent === "past-appointments"}
                    >
                      Past Appointments
                    </SideNavMenuItem>
                    <SideNavMenuItem
                      href="#"
                      onClick={(e: React.MouseEvent<HTMLAnchorElement>) => {
                        e.preventDefault();
                        setActiveComponent("view-appointments");
                        if (!isSideNavExpanded) onClickSideNavExpand();
                      }}
                      isActive={activeComponent === "view-appointments"}
                    >
                      View Appointments
                    </SideNavMenuItem>
                  </SideNavMenu>
                  <SideNavMenuItem
                    href="#"
                    onClick={(e: React.MouseEvent<HTMLAnchorElement>) => {
                      e.preventDefault();
                      setActiveComponent("availability-slots");
                      if (!isSideNavExpanded) onClickSideNavExpand();
                    }}
                    isActive={activeComponent === "availability-slots"}
                  >
                    View Availability Slots
                  </SideNavMenuItem>
                  <SideNavMenuItem
                    href="#"
                    onClick={(e: React.MouseEvent<HTMLAnchorElement>) => {
                      e.preventDefault();
                      setActiveComponent("medical-history");
                      if (!isSideNavExpanded) onClickSideNavExpand();
                    }}
                    isActive={activeComponent === "medical-history"}
                  >
                    View Medical History
                  </SideNavMenuItem>
                  <SideNavMenuItem
                    href="#"
                    onClick={(e: React.MouseEvent<HTMLAnchorElement>) => {
                      e.preventDefault();
                      setActiveComponent("available-doctors");
                      if (!isSideNavExpanded) onClickSideNavExpand();
                    }}
                    isActive={activeComponent === "available-doctors"}
                  >
                    View Available Doctors
                  </SideNavMenuItem>
                </SideNavItems>
              </SideNav>
            </Header>

            <div className={styles.headerContainer}>
              <Content id="main-content" className={styles.container}>
                {renderActiveComponent()}
              </Content>
            </div>
          </>
        )}
      />
    </>
  );
}
