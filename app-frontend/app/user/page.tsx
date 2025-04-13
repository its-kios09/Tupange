"use client";
import {
  Logout,
  Notification as NotificationIcon,
  UserAvatar,
} from "@carbon/icons-react";
import {
  Column,
  Header,
  HeaderContainer,
  HeaderGlobalAction,
  HeaderGlobalBar,
  HeaderMenu,
  HeaderMenuButton,
  HeaderMenuItem,
  HeaderName,
  HeaderPanel,
  HeaderSideNavItems,
  InlineNotification,
  SideNav,
  SideNavItems,
  SideNavMenu,
  SideNavMenuItem,
} from "@carbon/react";
import { useRouter } from "next/navigation";
import { useEffect, useRef, useState } from "react";
import { useTranslation } from "react-i18next";
import { useAuth } from "../context/auth-context";
import styles from "./page.module.scss";
import IncomingAppointments from "./appointments-incoming/page";

// Notification type
type Notification = {
  id: string;
  title: string;
  message: string;
  timestamp: string;
  unread: boolean;
};

export default function Dashboard() {
  const { user, logout, isLoading } = useAuth();
  const router = useRouter();
  const { t } = useTranslation();

  // State for notifications
  const [notifications, setNotifications] = useState<Notification[]>([]);
  const [hasUnreadNotifications, setHasUnreadNotifications] = useState(false);
  const [notificationsOpen, setNotificationsOpen] = useState(false);
  const [userMenuOpen, setUserMenuOpen] = useState(false);

  // Refs for focus management
  const notificationActionRef = useRef(null);
  const userActionRef = useRef<HTMLButtonElement>(null);

  // Snackbar state
  const [snackbar, setSnackbar] = useState({
    isOpen: false,
    message: "",
    kind: "error" as "error" | "success" | "info" | "warning",
  });

  // Generate a sample notification
  const generateNotification = (): Notification => ({
    id: Math.random().toString(36).substring(2, 9),
    title: "New notification",
    message: "This is a sample notification message.",
    timestamp: new Date().toISOString(),
    unread: true,
  });

  // Check for unread notifications
  useEffect(() => {
    const hasUnread = notifications.some((notification) => notification.unread);
    setHasUnreadNotifications(hasUnread);
  }, [notifications]);

  // Mark all notifications as read when panel opens
  useEffect(() => {
    if (notificationsOpen) {
      setNotifications((prev) =>
        prev.map((notification) => ({ ...notification, unread: false }))
      );
    }
  }, [notificationsOpen]);

  // Snackbar timeout
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
      setSnackbar({
        isOpen: true,
        message: t(
          "loginSuccess",
          "You have successfully logged out! Redirecting..."
        ),
        kind: "success",
      });
      await logout();
      router.push("/");
    } catch (error) {
      console.error("Logout failed:", error);
      setSnackbar({
        isOpen: true,
        message: t(
          "loginoutError",
          "An error occurred while logging out. Please try again."
        ),
        kind: "error",
      });
    }
  };

  return (
    <>
      <HeaderContainer
        render={({ isSideNavExpanded, onClickSideNavExpand }) => (
          <>
            <Header>
              <HeaderMenuButton
                onClick={onClickSideNavExpand}
                isActive={isSideNavExpanded}
                aria-expanded={isSideNavExpanded}
              />
              <HeaderName href="/user" prefix="">
                Tupange Portal
              </HeaderName>
              <HeaderGlobalBar>
                <HeaderGlobalAction
                  isActive={userMenuOpen}
                  onClick={() => {
                    setUserMenuOpen((prev) => !prev);
                    setNotificationsOpen(false);
                    setTimeout(() => {
                      userActionRef.current?.focus();
                    }, 0);
                  }}
                >
                  <UserAvatar size={20} />
                </HeaderGlobalAction>
                <HeaderPanel expanded={userMenuOpen}>
                  <div style={{ padding: "1rem", minWidth: "200px" }}>
                    <p>Welcome, {typeof user === "string" ? user : "User"}!</p>
                  </div>
                </HeaderPanel>

                <HeaderGlobalAction
                  aria-expanded={notificationsOpen}
                  isActive={notificationsOpen}
                  onClick={() => {
                    setNotificationsOpen((prev) => !prev);
                    setUserMenuOpen(false);
                  }}
                >
                  {hasUnreadNotifications && !notificationsOpen ? (
                    <div style={{ position: "relative" }}>
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
                        }}
                      />
                    </div>
                  ) : (
                    <NotificationIcon size={20} />
                  )}
                </HeaderGlobalAction>
                <HeaderPanel expanded={notificationsOpen}>
                  <div style={{ padding: "1rem", minWidth: "500px" }}></div>
                </HeaderPanel>
                <HeaderGlobalAction
                  onClick={handleLogout}
                >
                  <Logout size={20} />
                </HeaderGlobalAction>
              </HeaderGlobalBar>

              <SideNav
                expanded={isSideNavExpanded}
                onSideNavBlur={onClickSideNavExpand}
                href="#main-content"
              >
                <SideNavItems>
                  <SideNavMenu title="Appointments" tabIndex={0}>
                    <SideNavMenuItem>Incoming Appointments</SideNavMenuItem>
                    <SideNavMenuItem>Past Appointments </SideNavMenuItem>
                    <SideNavMenuItem>View Appointments</SideNavMenuItem>
                  </SideNavMenu>
                  <SideNavMenuItem>View Availability Slots</SideNavMenuItem>
                  <SideNavMenuItem>View Medical History</SideNavMenuItem>
                  <SideNavMenuItem>View Available Doctors</SideNavMenuItem>
                </SideNavItems>
              </SideNav>
            </Header>
          </>
        )}
      />
    </>
  );
}
