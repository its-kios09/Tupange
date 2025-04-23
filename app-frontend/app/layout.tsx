"use client";
import { ReactNode } from "react";
import { Josefin_Sans } from "next/font/google";
import "./globals.css";
import { AuthProvider } from "./context/auth-context";
import Image from "next/image";
import Link from "next/link";

const josefin = Josefin_Sans({
  subsets: ["latin"],
  display: "swap",
  variable: "--font-josefin",
});

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className={josefin.variable}>
      <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
      </head>
      <body>
        <header className="header">
          <div className="header-container">
            <Link href="/">
              <Image
                src="/images/logo.png"
                alt="Company Logo"
                width={150}
                height={50}
                className="logo"
                priority
              />
            </Link>
          </div>
        </header>
        <AuthProvider>{children}</AuthProvider>
      </body>
    </html>
  );
}
