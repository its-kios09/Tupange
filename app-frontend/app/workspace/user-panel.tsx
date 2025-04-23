"use client";
import { useState } from "react";
import {
  Button,
  ButtonSet,
  HeaderPanel,
  MenuItemDivider,
  SwitcherDivider,
  Tag,
  Tile,
} from "@carbon/react";
import { UserAvatar } from "@carbon/ibm-products";
import styles from "../user/page.module.scss";
import { Patient, Doctor, User } from "../types";
import capitalize from "lodash/capitalize";

interface UserPanelWorkspaceProps {
  expanded: boolean;
  user: User;
  patientData?: Patient | null;
  doctorData?: Doctor | null;
  className?: string;
  onClose?: () => void;
}

const UserPanelWorkspace = ({
  expanded,
  user,
  patientData,
  doctorData,
  onClose,
}: UserPanelWorkspaceProps) => {
  const getUserFullName = (): string => {
    if (user.role === "patient" && patientData) {
      return `${patientData.first_name} ${patientData.last_name}` || user.email;
    }
    if (user.role === "doctor" && doctorData) {
      return `${doctorData.first_name} ${doctorData.last_name}` || user.email;
    }
    if (user.role === "admin") {
      return `Super User`;
    }
    return "Pending Approval";
  };

  const getTooltipText = (): string => {
    if (user.role === "patient" && patientData) {
      return `${patientData.first_name}'s profile`;
    }
    if (user.role === "doctor" && doctorData) {
      return `${doctorData.first_name}'s profile`;
    }
    if (user.role === "admin") {
      return `Admin profile`;
    }
    return "User profile";
  };

  const renderDemographics = (): React.ReactNode => {
    const primaryInfo =
      user.role === "patient"
        ? patientData?.gender
        : doctorData?.specialization;

    const phoneNumber =
      user.role === "patient"
        ? patientData?.phone_number
        : doctorData?.phone_number;

    if (!primaryInfo && !phoneNumber) return "+254 7xx xxx xxx";

    return (
      <>
        {primaryInfo}
        {phoneNumber && (
          <>
            <span className={styles.middot}>&middot;</span> {phoneNumber}
          </>
        )}
      </>
    );
  };

  const renderAdditionalInfo = (): React.ReactNode => {
    if (user.role === "patient") {
      const hasInsuranceInfo =
        patientData?.insurance_provider || patientData?.insurance_number;

      return (
        <>
          {hasInsuranceInfo ? (
            <>
              {patientData?.insurance_provider && (
                <span>
                  {" "}
                  <Tag type="high-contrast">
                    {patientData.insurance_provider}
                  </Tag>
                  &nbsp;&nbsp;
                </span>
              )}
              {patientData?.insurance_number && (
                <span>
                  <Tag type="high-contrast">{patientData.insurance_number}</Tag>
                  <br />
                </span>
              )}
            </>
          ) : (
            <Tag type="red">Missing insurance information</Tag>
          )}
          {patientData?.address && (
            <span className={styles.addressTitle}>
              {capitalize(patientData?.address || "")}
            </span>
          )}
        </>
      );
    }

    if (user.role === "doctor") {
      return (
        doctorData?.specialization && (
          <span>Specialization: {doctorData.specialization}</span>
        )
      );
    }
    if (user.role === "admin") {
      return (
        <div>
          <span>Specialization: System Developer </span>
          <br />
          <Tag type="high-contrast">Verified</Tag>
        </div>
      );
    }
    
    return null;
  };

  const isEditDisabled = user.role === "patient" && !patientData;

  return (
    <HeaderPanel aria-label="User panel" expanded={expanded}>
      <div className={styles.panelContent}>
        <Tile className={styles.patientInfo}>
          <div className={styles.patientAvatar} role="img">
            <UserAvatar
              name={getUserFullName()}
              size="lg"
              tooltipText={getTooltipText()}
              tooltipAlignment="bottom"
            />
          </div>

          <div className={styles.patientDetails}>
            <h4 className={styles.patientName}>{getUserFullName()}</h4>

            {renderDemographics() && (
              <div className={styles.demographics}>{renderDemographics()}</div>
            )}

            {renderAdditionalInfo() && (
              <div className={styles.causeDisplay}>
                {renderAdditionalInfo()}
              </div>
            )}
          </div>
        </Tile>
        <MenuItemDivider />

        <div
          className={`${styles.buttonContainer} ${
            isEditDisabled ? styles.disabledState :''
          }`}
        >
          <ButtonSet>
            <Button kind="danger" onClick={onClose}>
              Discard
            </Button>
            <Button kind="secondary" disabled={isEditDisabled}>
              Edit profile
            </Button>
          </ButtonSet>
        </div>
      </div>
    </HeaderPanel>
  );
};

export default UserPanelWorkspace;
