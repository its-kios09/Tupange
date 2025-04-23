"use client";
import { useEffect } from "react";
import { ActionableNotification } from "@carbon/react";

export type NotificationProps = {
  title: string;
  subtitle?: string;
  kind: "error" | "success" | "info" | "warning";
  autoClose?: boolean;
  timeout?: number;
  onClose?: () => void;
  className?: string;
};

export const Notification = ({
  title,
  subtitle,
  kind,
  autoClose = false,
  timeout = 6000,
  onClose,
  className,
}: NotificationProps) => {
  useEffect(() => {
    if (!autoClose) return;

    const timer = setTimeout(() => {
      onClose?.();
    }, timeout);

    return () => clearTimeout(timer);
  }, [autoClose, timeout, onClose]);

  return (
    <ActionableNotification
      aria-label={title}
      title={title}
      subtitle={subtitle}
      kind={kind}
      inline
      lowContrast
      onClose={onClose}
      onActionButtonClick={onClose}
      actionButtonLabel="Dismiss"
      className={className}
    />
  );
};
