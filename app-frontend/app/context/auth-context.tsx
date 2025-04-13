"use client";
import React, {
  useState,
  createContext,
  useContext,
  useCallback,
  useEffect,
} from "react";
import { useRouter } from "next/navigation";
import axios from "axios";

type User = {
  access_token: string;
  email: string;
  role: string;
  is_active: boolean;
  id: number;
};

type AuthContextType = {
  user: User | null;
  login: (username: string, password: string) => Promise<void>;
  register: (email: string, password: string, role?: string) => Promise<void>;
  logout: () => void;
  isLoading: boolean;
  error: string | null;
};

const AuthContext = createContext<AuthContextType | undefined>(undefined);

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL;

export const AuthProvider = ({ children }: { children: React.ReactNode }) => {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const router = useRouter();

  useEffect(() => {
    const initializeAuth = async () => {
      const token = localStorage.getItem("access_token");
      if (token) {
        try {
          const userInfo = await axios.get(`${API_BASE_URL}/auth/me`, {
            headers: { Authorization: `Bearer ${token}` },
          });
          setUser({ ...userInfo.data, access_token: token });
          axios.defaults.headers.common["Authorization"] = `Bearer ${token}`;
          setUser({
            access_token: token,
            email: "",
            role: "",
            is_active: true,
            id: 0,
          });
        } catch (err) {
          localStorage.removeItem("access_token");
          delete axios.defaults.headers.common["Authorization"];
        }
      }
    };

    initializeAuth();
  }, []);

  const login = useCallback(
    async (username: string, password: string) => {
      setIsLoading(true);
      setError(null);

      try {
        const formData = new FormData();
        formData.append("username", username);
        formData.append("password", password);

        const response = await axios.post(
          `${API_BASE_URL}/auth/token`,
          formData,
          {
            headers: {
              "Content-Type": "application/x-www-form-urlencoded",
            },
          }
        );

        const { access_token } = response.data;

        localStorage.setItem("access_token", access_token);

        axios.defaults.headers.common[
          "Authorization"
        ] = `Bearer ${access_token}`;

        setUser({
          access_token,
          email: username,
          role: "patient",
          is_active: true,
          id: 0,
        });

        router.push("/");
      } catch (error: any) {
        const errorMessage =
          error.response?.data?.detail || "Login failed. Please try again.";
        setError(errorMessage);
        console.error("Login failed:", error);
        throw error;
      } finally {
        setIsLoading(false);
      }
    },
    [router]
  );

  const register = useCallback(
    async (email: string, password: string, role: string = "patient") => {
      setIsLoading(true);
      setError(null);

      try {
        const response = await axios.post(`${API_BASE_URL}/auth/register`, {
          email,
          password,
          is_active: true,
          role,
        });

        await login(email, password);
      } catch (error: any) {
        const errorMessage =
          error.response?.data?.detail ||
          error.response?.data?.message ||
          "Registration failed. Please try again.";
        setError(errorMessage);
        console.error("Registration failed:", error);
        throw error;
      } finally {
        setIsLoading(false);
      }
    },
    [login]
  );

  const logout = useCallback(() => {
    localStorage.removeItem("access_token");
    delete axios.defaults.headers.common["Authorization"];
    setUser(null);
    router.push("/");
  }, [router]);

  return (
    <AuthContext.Provider
      value={{ user, login, register, logout, isLoading, error }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
};
