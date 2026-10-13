permit(principal is User, action == Action::"View", resource is Document) when {
resource.projectStatus == "Active" &&
principal in Role::"ClinicalResearcher" &&
principal in Role::"GlobalAuditor" &&
!(principal in Role::"PrincipalInvestigator") &&
!(principal in Role::"DataManager") &&
!(principal in Role::"SponsorRepresentative") &&
principal.department != resource.projectManagingDepartment &&
principal.clearanceLevel > 3 &&
resource.classification != "HighlyRestricted" &&
context.requestTime >= resource.embargoUntil
};
