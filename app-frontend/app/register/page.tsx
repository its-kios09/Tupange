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
} from "@carbon/react";
import styles from "./page.module.scss";
import { useRouter } from "next/navigation";
import { useEffect } from "react";
import { RegisterFormData, registerSchema } from "../schemas/auth";
import { useAuth } from "../context/auth-context";

const RegisterPage = () => {
  const { user, register: registerUser, isLoading } = useAuth();
  const router = useRouter();
  const {
    register,
    handleSubmit,
    formState: { errors },
    setError,
    watch,
  } = useForm<RegisterFormData>({
    resolver: zodResolver(registerSchema),
  });

  useEffect(() => {
    if (user) {
      router.push("/");
    }
  }, [user, router]);

  const onSubmit = async (data: RegisterFormData) => {
    try {
      await registerUser(data?.email, data?.password);
    } catch (error: any) {
      setError("root", {
        type: "manual",
        message: error.message || "Registration failed",
      });
    }
  };

  return (
    <div className={styles.container}>
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
            />

            <PasswordInput
              id="password"
              labelText="Password"
              invalid={!!errors.password}
              invalidText={errors.password?.message}
              {...register("password")}
            />

            <PasswordInput
              id="confirmPassword"
              labelText="Confirm Password"
              invalid={!!errors.confirmPassword}
              invalidText={errors.confirmPassword?.message}
              {...register("confirmPassword")}
            />

            {errors.root && (
              <div className={styles.errorMessage}>{errors.root.message}</div>
            )}

            <Button
              type="submit"
              disabled={isLoading}
              className={styles.continueButton}
            >
              Register
              {isLoading && <InlineLoading description="Registering..." />}
            </Button>
          </div>
          <Link href="/">Already have an account? Login</Link>
        </form>
      </Tile>
    </div>
  );
};

export default RegisterPage;
