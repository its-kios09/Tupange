"use client";
import Image from "next/image";
import styles from "./page.module.css";
import { useRouter } from "next/navigation";
import { useTranslation } from "react-i18next";
import LoginPage from "./login/page";
import { useAuth } from "./context/auth-context";
import { useEffect } from "react";

export default function Home() {
  const { t } = useTranslation();
  const { user, logout, isLoading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (user) {
      router.push("/user");
    }
  }, [user, router]);
  return (
    <>
      <div className={styles.container}>
        <div className={styles.imageSection}>
          <div className={styles.imageOverlay}></div>
          <Image
            src="/images/portal-background.png"
            alt="Image portal"
            fill
            className={styles.image}
            priority
          />
        </div>

        <div className={styles.loginSection}>
          <div className={styles.loginContainer}>
            {user ? null : <LoginPage />}
          </div>
        </div>
      </div>
      <footer>
        <p>{t("footer", "Footer")}</p>
      </footer>
    </>
  );
}
