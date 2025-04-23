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
    formState: { errors, isSubmitting },
  } = useForm<LoginFormData>({
    resolver: zodResolver(loginSchema),
  });

  const [snackbar, setSnackbar] = useState({
    isOpen: false,
    message: "",
    kind: "error" as "error" | "success" | "info" | "warning",
  });
  const [isRedirecting, setIsRedirecting] = useState(false);

  // Handle successful login and redirect
  useEffect(() => {
    if (user && !isRedirecting) {
      setIsRedirecting(true);
      setSnackbar({
        isOpen: true,
        message: t(
          "loginSuccess",
          "You have successfully logged in! Redirecting..."
        ),
        kind: "success",
      });

      // Set a timer for the redirect
      const redirectTimer = setTimeout(() => {
        router.push("/");
      }, 2000);

      return () => clearTimeout(redirectTimer);
    }
  }, [user, router, isRedirecting, t]);

  // Auto-hide snackbar after timeout
  useEffect(() => {
    if (snackbar.isOpen) {
      const hideTimer = setTimeout(() => {
        setSnackbar((prev) => ({ ...prev, isOpen: false }));
      }, 6000);
      return () => clearTimeout(hideTimer);
    }
  }, [snackbar.isOpen]);

  const onSubmit = async (data: LoginFormData) => {
    try {
      const success = await login(data.email, data.password);
      if (!success) {
        setSnackbar({
          isOpen: true,
          message: t(
            "loginError",
            "You have entered an invalid email or password. Please try again."
          ),
          kind: "error",
        });
      }
      // Success case is handled by the user effect above
    } catch (error) {
      setSnackbar({
        isOpen: true,
        message: t(
          "loginError",
          "An unexpected error occurred. Please try again."
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
              id="email"
              labelText={t("email", "Email")}
              invalid={!!errors.email}
              invalidText={errors.email?.message}
              {...register("email")}
              autoFocus
              disabled={isSubmitting || isLoading}
            />

            <PasswordInput
              id="password"
              labelText={t("password", "Password")}
              invalid={!!errors.password}
              invalidText={errors.password?.message}
              {...register("password")}
              disabled={isSubmitting || isLoading}
            />

            <Button
              type="submit"
              className={styles.continueButton}
              renderIcon={(props) => <ArrowRight size={24} {...props} />}
              disabled={isSubmitting || isLoading}
            >
              {isSubmitting || isLoading ? (
                <InlineLoading
                  className={styles.loader}
                  description={t("loggingIn", "Logging in") + "..."}
                />
              ) : (
                t("login", "Log in")
              )}
            </Button>
          </div>
          <Link href="/register">
            {t("noAccount", "Don't have an account? Self Register")}
          </Link>
        </form>
      </Tile>
    </div>
  );
};

export default LoginPage;
