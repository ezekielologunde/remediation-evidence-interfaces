permit(principal is User, action == Action::"Edit", resource is Document) when {
resource.projectStatus == "Active" &&
principal in Role::"PrincipalInvestigator" &&
principal in Role::"GlobalAuditor" &&
!(principal in Role::"ClinicalResearcher") &&
!(principal in Role::"DataManager") &&
!(principal in Role::"SponsorRepresentative") &&
principal.department != resource.projectManagingDepartment &&
context.networkRiskScore < 20 &&
context.isCompliantDevice &&
context.hasPatientConsent
};
