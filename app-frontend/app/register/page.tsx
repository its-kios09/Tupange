"use client";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
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
import { RegisterFormData, registerSchema } from "../schemas/auth";
import { useAuth } from "../context/auth-context";
import classNames from "classnames";

const RegisterPage = () => {
  const { user, register: registerUser, isLoading } = useAuth();
  const router = useRouter();
  const {
    register,
    handleSubmit,
    formState: { errors },
    watch,
  } = useForm<RegisterFormData>({
    resolver: zodResolver(registerSchema),
  });

  const [notification, setNotification] = useState({
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
    if (notification.isOpen) {
      const timer = setTimeout(() => {
        setNotification((prev) => ({ ...prev, isOpen: false }));
      }, 6000);
      return () => clearTimeout(timer);
    }
  }, [notification.isOpen]);

  const onSubmit = async (data: RegisterFormData) => {
    try {
      const success = await registerUser(data.email, data.password);
      if (success) {
        setNotification({
          isOpen: true,
          message: "Registration successful! Redirecting...",
          kind: "success",
        });
        // Redirect after showing success message
        setTimeout(() => router.push("/"), 4000);
      }
    } catch (error: any) {
      setNotification({
        isOpen: true,
        message: error.message || "Registration failed. Please try again.",
        kind: "error",
      });
    }
  };

  return (
    <div className={styles.container}>
      {notification.isOpen && (
        <div className={styles.notificationContainer}>
          <ActionableNotification
            aria-label="Registration status"
            title={notification.message}
            kind={notification.kind}
            inline
            lowContrast={notification.kind === "error"}
            onClose={() =>
              setNotification((prev) => ({ ...prev, isOpen: false }))
            }
            className={classNames(styles.notification, {
              [styles.notificationError]: notification.kind === "error",
              [styles.notificationSuccess]: notification.kind === "success",
            })}
          />
        </div>
      )}

      <Tile className={styles.loginCard}>
        <form onSubmit={handleSubmit(onSubmit)}>
          <div className={styles.inputGroup}>
            <TextInput
              id="email"
              labelText="Email"
              type="email"
              invalid={!!errors.email}
              invalidText={errors.email?.message}
              {...register("email")}
              disabled={isLoading}
            />

            <PasswordInput
              id="password"
              labelText="Password"
              invalid={!!errors.password}
              invalidText={errors.password?.message}
              {...register("password")}
              disabled={isLoading}
            />

            <PasswordInput
              id="confirmPassword"
              labelText="Confirm Password"
              invalid={!!errors.confirmPassword}
              invalidText={errors.confirmPassword?.message}
              {...register("confirmPassword")}
              disabled={isLoading}
            />

            <Button
              type="submit"
              disabled={isLoading}
              className={styles.continueButton}
            >
              {isLoading ? (
                <InlineLoading description="Registering..." />
              ) : (
                "Register"
              )}
            </Button>
          </div>
          <Link href="/">Already have an account? Login</Link>
        </form>
      </Tile>
    </div>
  );
};

export default RegisterPage;
