permit(principal is User, action in [Action::"View", Action::"Edit"], resource is Document) when {
resource.projectStatus == "Active" &&
    ((principal in Role::"ClinicalResearcher" && principal.clearanceLevel > 3 && resource.classification != "HighlyRestricted") ||
     (principal in Role::"PrincipalInvestigator" && context.networkRiskScore < 20 && context.isCompliantDevice)) &&
    principal in Role::"GlobalAuditor" && (action == Action::"View" || context.hasPatientConsent)
};
