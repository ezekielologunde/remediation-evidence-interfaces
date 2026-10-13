permit (
    principal is User,
    action == Action::"View",
    resource is Document
)
when {
    principal in Role::"PrincipalInvestigator" &&
    principal in Role::"GlobalAuditor" &&
    resource.projectStatus == "Active" &&
    context.networkRiskScore < 20 &&
    context.isCompliantDevice == true &&
    resource.classification != "HighlyRestricted" &&
    resource.studyPhase != "Phase-3"
};
permit (
    principal is User,
    action == Action::"Edit",
    resource is Document
)
when {
    principal in Role::"DataManager" &&
    resource.projectStatus == "Active" &&
    principal.clearanceLevel > 5 &&
    principal.department == resource.projectManagingDepartment &&
    context.hasPatientConsent == true &&
    context.isCompliantDevice == true &&
    resource.studyPhase != "Phase-3"
};
permit (
    principal is User,
    action == Action::"View",
    resource is Document
)
when {
    principal in Role::"ClinicalResearcher" &&
    resource.projectStatus == "Active" &&
    principal.clearanceLevel > 3 &&
    resource.classification != "HighlyRestricted" &&
    resource.studyPhase != "Phase-3" &&
    principal.department == resource.projectManagingDepartment
};
permit (
    principal is User,
    action == Action::"View",
    resource is Document
)
when {
    principal in Role::"PrincipalInvestigator" &&
    resource.projectStatus == "Active" &&
    context.networkRiskScore < 20 &&
    context.isCompliantDevice == true &&
    principal.department == resource.projectManagingDepartment &&
    resource.classification != "HighlyRestricted" &&
    resource.studyPhase != "Phase-3"
};