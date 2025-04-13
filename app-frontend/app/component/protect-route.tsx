// "use client";
// import { useRouter } from "next/navigation";
// import { ReactNode, useContext, useEffect, useState } from "react";
// import { AuthContext } from "../context/auth-context"; // Adjusted the path to match the likely correct location

// const ProtectRoute = ({ children }: { children: ReactNode }) => {
//   const authContext = useContext(AuthContext);

//   if (!authContext) {
//     throw new Error("AuthContext is undefined. Ensure that ProtectRoute is wrapped in an AuthProvider.");
//   }

//   const { user } = authContext;
//   const router = useRouter();
//   const [isLoading, setIsLoading] = useState(true);

//   useEffect(() => {
//     const checkAuth = () => {
//       if (!user) {
//         const currentPath = window.location.pathname;
//         router.push(`/login?redirect=${encodeURIComponent(currentPath)}`);
//       }
//       setIsLoading(false);
//     };

//     checkAuth();
//   }, [user, router]);

//   if (isLoading) {
//     return (
//       <div className={style.container}>
//         <div className={style.spinner}></div>
//       </div>
//     );
//   }

//   if (!user) {
//     return null;
//   }

//   return user ? children : null;
// };

// export default ProtectRoute;
