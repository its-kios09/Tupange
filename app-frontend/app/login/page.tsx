"use client";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { ArrowRight } from "@carbon/icons-react";
import {
  Button,
  Link,
  PasswordInput,
  TextInput,
  Tile,
  InlineLoading,
  ActionableNotification,
  NotificationActionButton,
} from "@carbon/react";
import styles from "./page.module.scss";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import { useAuth } from "../context/auth-context";
import { LoginFormData, loginSchema } from "../schemas/auth";
import { useTranslation } from "react-i18next";
import classNames from "classnames";

const LoginPage = () => {
  const { user, login, isLoading } = useAuth();
  const router = useRouter();
  const { t } = useTranslation();
  const {
    register,
    handleSubmit,
    formState: { errors },
    setError,
  } = useForm<LoginFormData>({
    resolver: zodResolver(loginSchema),
  });

  const [snackbar, setSnackbar] = useState({
    isOpen: false,
    message: "",
    kind: "error" as "error" | "success" | "info" | "warning",
  });

  useEffect(() => {
    if (user) {
      router.push("/");
    }
  }, [user, router]);

  useEffect(() => {
    if (snackbar.isOpen) {
      const timer = setTimeout(() => {
        setSnackbar((prev) => ({ ...prev, isOpen: false }));
      }, 6000);
      return () => clearTimeout(timer);
    }
  }, [snackbar.isOpen]);

 const onSubmit = async (data: LoginFormData) => {
   try {
    setSnackbar({
      isOpen: true,
      message: t(
        "loginSuccess",
        "You have successfully logged in! Redirecting..."
      ),
      kind: "success",
    });
     await login(data?.email, data?.password)

     // Then redirect after a short delay
     setTimeout(() => {
       router.push("/");
     }, 4000); // 2 seconds delay
   } catch (error: any) {
     setSnackbar({
       isOpen: true,
       message: t(
         "loginError",
         "You have entered an invalid email or password. Please try again."
       ),
       kind: "error",
     });
   }
 };

  return (
    <div className={styles.container}>
      {snackbar.isOpen && (
        <div className={styles.snackbarContainer}>
          <ActionableNotification
            aria-label="Login status"
            title={snackbar.message}
            kind={snackbar.kind}
            inline
            lowContrast={snackbar.kind === "error"}
            onActionButtonClick={() =>
              setSnackbar((prev) => ({ ...prev, isOpen: false }))
            }
            onClose={() => setSnackbar((prev) => ({ ...prev, isOpen: false }))}
            className={classNames(styles.snackbar, {
              [styles.snackbarError]: snackbar.kind === "error",
              [styles.snackbarSuccess]: snackbar.kind === "success",
            })}
          />
        </div>
      )}

      <Tile className={styles.loginCard}>
        <form onSubmit={handleSubmit(onSubmit)}>
          <div className={styles.inputGroup}>
            <TextInput
              id="username"
              labelText="Email"
              invalid={!!errors.email}
              invalidText={errors.email?.message}
              {...register("email")}
              autoFocus
            />

            <PasswordInput
              id="password"
              labelText="Password"
              invalid={!!errors.password}
              invalidText={errors.password?.message}
              {...register("password")}
            />

            <Button
              type="submit"
              className={styles.continueButton}
              renderIcon={(props) => <ArrowRight size={24} {...props} />}
              disabled={isLoading}
            >
              {isLoading ? (
                <InlineLoading
                  className={styles.loader}
                  description={t("loggingIn", "Logging in") + "..."}
                />
              ) : (
                t("login", "Log in")
              )}
            </Button>
          </div>
          <Link href="/register">Don't have an account? Self Register</Link>
        </form>
      </Tile>
    </div>
  );
};

export default LoginPage;
