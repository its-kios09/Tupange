export type Notification = {
  id: string;
  title: string;
  message: string;
  timestamp: string;
  unread: boolean;
};

export type Patient = {
  first_name: string;
  last_name: string;
  date_of_birth: string;
  gender: string;
  phone_number: string;
  address: string;
  insurance_number: string;
  insurance_provider: string;
  id: number;
  user_id: number;
};

export type ActiveComponent =
  | "incoming-appointments"
  | "past-appointments"
  | "view-appointments"
  | "availability-slots"
  | "medical-history"
  | "available-doctors";

export type User = {
  access_token: string;
  email: string;
  role: string;
  is_active: boolean;
  id: number;
};

export type Doctor = {
  first_name: string;
  last_name: string;
  specialization: string;
  phone_number: string;
  id: number;
  user_id: number;
};
