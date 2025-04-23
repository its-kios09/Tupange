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
import { Doctor, Patient, User } from "../types";

type AuthContextType = {
  user: User | null;
  login: (username: string, password: string) => Promise<boolean>;
  register: (
    email: string,
    password: string,
    role?: string
  ) => Promise<boolean>;
  logout: () => Promise<boolean>;
  isLoading: boolean;
  error: string | null;
  getPatientProfile: () => Promise<Patient[]>;
  getDoctorProfile: () => Promise<Doctor[]>;
};

const AuthContext = createContext<AuthContextType | undefined>(undefined);

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL;

export const AuthProvider = ({ children }: { children: React.ReactNode }) => {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const router = useRouter();

  const fetchUserInfo = useCallback(async (token: string) => {
    try {
      const userInfo = await axios.get(`${API_BASE_URL}/auth/me`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      setUser({ ...userInfo.data, access_token: token });
      axios.defaults.headers.common["Authorization"] = `Bearer ${token}`;
    } catch (err) {
      localStorage.removeItem("access_token");
      delete axios.defaults.headers.common["Authorization"];
      throw err;
    }
  }, []);

  useEffect(() => {
    const initializeAuth = async () => {
      const token = localStorage.getItem("access_token");
      if (token) {
        setIsLoading(true);
        try {
          await fetchUserInfo(token);
        } catch (err) {
          console.error("Failed to fetch user info:", err);
        } finally {
          setIsLoading(false);
        }
      }
    };

    initializeAuth();
  }, [fetchUserInfo]);

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

        await fetchUserInfo(access_token);
        return true; // Return true on success
      } catch (error: any) {
        const errorMessage =
          error.response?.data?.detail || "Login failed. Please try again.";
        setError(errorMessage);
        return false; // Return false on failure
      } finally {
        setIsLoading(false);
      }
    },
    [router, fetchUserInfo]
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
        return true;
      } catch (error: any) {
        const errorMessage =
          error.response?.data?.detail ||
          error.response?.data?.message ||
          "Registration failed. Please try again.";
        setError(errorMessage);
        console.error("Registration failed:", error);
        return false;
      } finally {
        setIsLoading(false);
      }
    },
    [login]
  );

  const logout = useCallback(async () => {
    localStorage.removeItem("access_token");
    delete axios.defaults.headers.common["Authorization"];
    setUser(null);
    return true;
  }, [router]);

  const getPatientProfile = useCallback(async () => {
    if (!user) {
      throw new Error("User must be logged in to fetch patients");
    }

    try {
      const response = await axios.get(`${API_BASE_URL}/patients/`);
      const getPatients = response.data;

      if (user.role === "patient") {
        return getPatients.filter(
          (patient: Patient) => patient.user_id === user.id
        );
      }

      return getPatients;
    } catch (error) {
      console.error("Failed to fetch patients:", error);
      throw error;
    }
  }, [user]);

  const getDoctorProfile = useCallback(async () => {
    if (!user) {
      throw new Error("User must be logged in to fetch doctors");
    }
    try {
      const response = await axios.get(`${API_BASE_URL}/doctors/`);
      const getDoctors = response.data;
      if (user.role === "doctor") {
        return getDoctors.filter(
          (doctor: Doctor) => doctor.user_id === user.id
        );
      }
      return getDoctors;
    } catch (error) {
      console.error("Failed to fetch doctors:", error);
      throw error;
    }
  }, [user]);

  return (
    <AuthContext.Provider
      value={{
        user,
        login,
        register,
        logout,
        isLoading,
        error,
        getPatientProfile,
        getDoctorProfile,
      }}
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
